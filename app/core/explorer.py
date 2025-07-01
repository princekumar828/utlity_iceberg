"""
Core lakehouse exploration functionality for web interface with DuckDB integration
"""

from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import duckdb
from pyiceberg.catalog import load_catalog
from pyiceberg.table import Table
from pyiceberg.schema import Schema
import json
import traceback
from datetime import datetime
import tempfile
import os

from app.core.config import LakehouseConfig

class LakehouseExplorer:
    """Main class for exploring lakehouse tables via web interface with DuckDB integration"""
    
    def __init__(self, config: LakehouseConfig):
        self.config = config
        self.catalog = None
        self.duckdb_conn = None
        self._connect_to_catalog()
        self._setup_duckdb()
    
    def _connect_to_catalog(self):
        """Initialize connection to Nessie catalog"""
        try:
            catalog_config = self.config.to_pyiceberg_catalog_config()
            self.catalog = load_catalog("lakehouse", **catalog_config)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to catalog: {str(e)}")
    
    def _setup_duckdb(self):
        """Initialize DuckDB connection with Iceberg extension"""
        try:
            self.duckdb_conn = duckdb.connect()
            
            # Install and load Iceberg extension if available
            try:
                self.duckdb_conn.execute("INSTALL iceberg")
                self.duckdb_conn.execute("LOAD iceberg")
                print("✅ DuckDB Iceberg extension loaded")
            except Exception as e:
                print(f"⚠️  DuckDB Iceberg extension not available: {e}")
                print("   Falling back to PyIceberg for data access")
            
            # Configure DuckDB for better performance
            self.duckdb_conn.execute("SET memory_limit='2GB'")
            self.duckdb_conn.execute("SET max_memory='4GB'")
            
        except Exception as e:
            print(f"Warning: Failed to initialize DuckDB: {e}")
            self.duckdb_conn = None
    
    def list_namespaces(self) -> List[Tuple[str, ...]]:
        """List all available namespaces"""
        try:
            namespaces = list(self.catalog.list_namespaces())
            return namespaces
        except Exception as e:
            raise RuntimeError(f"Error listing namespaces: {str(e)}")
    
    def list_tables_in_namespace(self, namespace: Tuple[str, ...]) -> List[str]:
        """List all tables in a given namespace"""
        try:
            tables = list(self.catalog.list_tables(namespace))
            # Extract just the table names
            return [table[-1] for table in tables]
        except Exception as e:
            raise RuntimeError(f"Error listing tables in namespace {namespace}: {str(e)}")
    
    def get_all_tables(self) -> Dict[Tuple[str, ...], List[str]]:
        """Get all tables organized by namespace"""
        try:
            namespaces = self.list_namespaces()
            all_tables = {}
            
            for namespace in namespaces:
                try:
                    tables = self.list_tables_in_namespace(namespace)
                    all_tables[namespace] = tables
                except Exception as e:
                    print(f"Warning: Could not list tables in namespace {namespace}: {str(e)}")
                    all_tables[namespace] = []
            
            return all_tables
        except Exception as e:
            raise RuntimeError(f"Error getting all tables: {str(e)}")
    
    def get_table_schema(self, namespace: Tuple[str, ...], table_name: str) -> Optional[Dict[str, Any]]:
        """Get table schema information"""
        try:
            table = self.catalog.load_table((*namespace, table_name))
            schema = table.schema()
            
            # Convert schema to JSON-serializable format
            schema_info = {
                "schema_id": schema.schema_id,
                "fields": []
            }
            
            for field in schema.fields:
                field_info = {
                    "id": field.field_id,
                    "name": field.name,
                    "type": str(field.field_type),
                    "required": field.required,
                    "doc": field.doc
                }
                schema_info["fields"].append(field_info)
            
            return schema_info
            
        except Exception as e:
            print(f"Error getting schema for table {namespace}.{table_name}: {str(e)}")
            return None
    
    def get_table_metadata(self, namespace: Tuple[str, ...], table_name: str) -> Optional[Dict[str, Any]]:
        """Get table metadata and properties"""
        try:
            table = self.catalog.load_table((*namespace, table_name))
            
            metadata = {
                "location": table.location(),
                "schema": self.get_table_schema(namespace, table_name),
                "properties": dict(table.properties()),
                "current_snapshot_id": table.current_snapshot().snapshot_id if table.current_snapshot() else None,
                "format_version": table.format_version,
                "table_uuid": str(table.metadata.table_uuid)
            }
            
            # Add partition information if available
            if table.spec().fields:
                metadata["partitions"] = [
                    {
                        "field_id": field.source_id,
                        "name": field.name,
                        "transform": str(field.transform)
                    }
                    for field in table.spec().fields
                ]
            else:
                metadata["partitions"] = []
            
            return metadata
            
        except Exception as e:
            print(f"Error getting metadata for table {namespace}.{table_name}: {str(e)}")
            return None
    
    def preview_table_data(self, namespace: Tuple[str, ...], table_name: str, limit: int = 10) -> Optional[Dict[str, Any]]:
        """Preview table data using DuckDB for better performance"""
        try:
            table = self.catalog.load_table((*namespace, table_name))
            
            # Try DuckDB first for better performance
            if self.duckdb_conn:
                try:
                    return self._preview_with_duckdb(table, limit)
                except Exception as e:
                    print(f"DuckDB preview failed, falling back to PyIceberg: {e}")
            
            # Fallback to PyIceberg method
            return self._preview_with_pyiceberg(table, limit)
            
        except Exception as e:
            print(f"Error previewing table {namespace}.{table_name}: {str(e)}")
            return None
    
    def _preview_with_duckdb(self, table: Table, limit: int) -> Dict[str, Any]:
        """Preview table data using DuckDB"""
        # Get table files from Iceberg
        scan = table.scan()
        arrow_table = scan.to_arrow()
        
        # Register Arrow table with DuckDB
        table_name = "temp_iceberg_table"
        self.duckdb_conn.register(table_name, arrow_table)
        
        # Query with DuckDB for better performance
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        result = self.duckdb_conn.execute(query).fetchdf()
        
        # Clean up
        self.duckdb_conn.unregister(table_name)
        
        return self._format_dataframe_result(result, limit)
    
    def _preview_with_pyiceberg(self, table: Table, limit: int) -> Dict[str, Any]:
        """Preview table data using PyIceberg (fallback method)"""
        scan = table.scan(limit=limit)
        df = scan.to_pandas()
        return self._format_dataframe_result(df, limit)
    
    def _format_dataframe_result(self, df: pd.DataFrame, limit: int) -> Dict[str, Any]:
        """Format DataFrame result for JSON serialization"""
        result = {
            "columns": df.columns.tolist(),
            "data": df.values.tolist(),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "row_count": len(df),
            "preview_limit": limit,
            "engine": "duckdb" if hasattr(self, '_last_engine_used') and self._last_engine_used == "duckdb" else "pyiceberg"
        }
        
        # Handle any datetime or special types
        for i, row in enumerate(result["data"]):
            for j, value in enumerate(row):
                if pd.isna(value):
                    result["data"][i][j] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    result["data"][i][j] = value.isoformat()
                elif hasattr(value, 'item'):  # numpy types
                    result["data"][i][j] = value.item()
        
        return result
    
    def execute_sql_query(self, namespace: Tuple[str, ...], table_name: str, sql_query: str, limit: int = 100) -> Optional[Dict[str, Any]]:
        """Execute SQL query on table using DuckDB"""
        try:
            if not self.duckdb_conn:
                return {"error": "DuckDB not available for SQL queries"}
            
            table = self.catalog.load_table((*namespace, table_name))
            
            # Get table data as Arrow
            scan = table.scan()
            arrow_table = scan.to_arrow()
            
            # Register with DuckDB
            temp_table_name = f"table_{table_name}"
            self.duckdb_conn.register(temp_table_name, arrow_table)
            
            # Replace table references in SQL
            processed_query = sql_query.replace(f"{'.'.join(namespace)}.{table_name}", temp_table_name)
            processed_query = processed_query.replace(table_name, temp_table_name)
            
            # Add limit if not present
            if "LIMIT" not in processed_query.upper():
                processed_query += f" LIMIT {limit}"
            
            # Execute query
            result_df = self.duckdb_conn.execute(processed_query).fetchdf()
            
            # Clean up
            self.duckdb_conn.unregister(temp_table_name)
            
            return {
                "query": sql_query,
                "processed_query": processed_query,
                "result": self._format_dataframe_result(result_df, limit),
                "success": True
            }
            
        except Exception as e:
            return {
                "query": sql_query,
                "error": str(e),
                "success": False
            }
    
    def get_table_statistics(self, namespace: Tuple[str, ...], table_name: str) -> Optional[Dict[str, Any]]:
        """Get table statistics using DuckDB for better performance"""
        try:
            if not self.duckdb_conn:
                return self._get_basic_statistics(namespace, table_name)
            
            table = self.catalog.load_table((*namespace, table_name))
            scan = table.scan()
            arrow_table = scan.to_arrow()
            
            # Register with DuckDB
            temp_table_name = f"stats_table_{table_name}"
            self.duckdb_conn.register(temp_table_name, arrow_table)
            
            # Get basic statistics
            stats_query = f"""
            SELECT 
                COUNT(*) as row_count,
                COUNT(DISTINCT *) as distinct_rows
            FROM {temp_table_name}
            """
            
            basic_stats = self.duckdb_conn.execute(stats_query).fetchdf().iloc[0]
            
            # Get column statistics
            columns = arrow_table.column_names
            column_stats = {}
            
            for col in columns:
                try:
                    col_query = f"""
                    SELECT 
                        COUNT(*) as count,
                        COUNT(DISTINCT "{col}") as distinct_count,
                        COUNT(*) - COUNT("{col}") as null_count
                    FROM {temp_table_name}
                    """
                    col_result = self.duckdb_conn.execute(col_query).fetchdf().iloc[0]
                    column_stats[col] = {
                        "count": int(col_result['count']),
                        "distinct_count": int(col_result['distinct_count']),
                        "null_count": int(col_result['null_count']),
                        "null_percentage": round((col_result['null_count'] / col_result['count']) * 100, 2) if col_result['count'] > 0 else 0
                    }
                except Exception as e:
                    column_stats[col] = {"error": str(e)}
            
            # Clean up
            self.duckdb_conn.unregister(temp_table_name)
            
            return {
                "total_rows": int(basic_stats['row_count']),
                "distinct_rows": int(basic_stats['distinct_rows']),
                "column_statistics": column_stats,
                "engine": "duckdb"
            }
            
        except Exception as e:
            print(f"Error getting statistics for table {namespace}.{table_name}: {str(e)}")
            return self._get_basic_statistics(namespace, table_name)
    
    def _get_basic_statistics(self, namespace: Tuple[str, ...], table_name: str) -> Dict[str, Any]:
        """Get basic statistics using PyIceberg (fallback)"""
        try:
            table = self.catalog.load_table((*namespace, table_name))
            scan = table.scan(limit=10000)  # Sample for stats
            df = scan.to_pandas()
            
            return {
                "total_rows": len(df),
                "distinct_rows": len(df.drop_duplicates()),
                "column_statistics": {
                    col: {
                        "count": len(df[col]),
                        "distinct_count": df[col].nunique(),
                        "null_count": df[col].isnull().sum(),
                        "null_percentage": round((df[col].isnull().sum() / len(df)) * 100, 2)
                    }
                    for col in df.columns
                },
                "engine": "pyiceberg",
                "note": "Statistics based on sample of 10,000 rows"
            }
        except Exception as e:
            return {"error": str(e)}
        """Search for tables by name across all namespaces"""
        try:
            all_tables = self.get_all_tables()
            results = []
            
            search_term = search_term.lower()
            
            for namespace, tables in all_tables.items():
                for table_name in tables:
                    if search_term in table_name.lower():
                        results.append({
                            "namespace": ".".join(namespace) if namespace else "default",
                            "table_name": table_name,
                            "full_name": f"{'.'.join(namespace)}.{table_name}" if namespace else table_name
                        })
            
            return results
            
        except Exception as e:
            print(f"Error searching tables: {str(e)}")
            return []
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information for display"""
        return {
            "nessie_uri": self.config.nessie_uri,
            "nessie_ref": self.config.nessie_ref,
            "s3_endpoint": self.config.s3_endpoint,
            "warehouse_path": self.config.warehouse_path,
            "s3_region": self.config.s3_region,
            "duckdb_available": self.duckdb_conn is not None,
            "engines": {
                "pyiceberg": "Available",
                "duckdb": "Available" if self.duckdb_conn else "Not available"
            }
        }
