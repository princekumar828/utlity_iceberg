from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from pyiceberg.catalog import load_catalog
from pyiceberg.table import Table
from pyiceberg.schema import Schema
from rich.console import Console
from rich.table import Table as RichTable
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
import json
import traceback
from datetime import datetime

from config import LakehouseConfig

class LakehouseExplorer:
    """Main class for exploring lakehouse tables"""
    
    def __init__(self, config: LakehouseConfig):
        self.config = config
        self.console = Console()
        self.catalog = None
        self._connect_to_catalog()
    
    def _connect_to_catalog(self):
        """Initialize connection to Nessie catalog"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Connecting to Nessie catalog...", total=None)
                
                catalog_config = self.config.to_pyiceberg_catalog_config()
                self.catalog = load_catalog("lakehouse", **catalog_config)
                
                progress.update(task, description="✅ Connected to catalog successfully!")
                
        except Exception as e:
            self.console.print(f"[red]Failed to connect to catalog: {str(e)}[/red]")
            self.console.print(f"[yellow]Config used: {json.dumps(self.config.to_pyiceberg_catalog_config(), indent=2)}[/yellow]")
            raise
    
    def list_namespaces(self) -> List[Tuple[str, ...]]:
        """List all available namespaces"""
        try:
            namespaces = list(self.catalog.list_namespaces())
            return namespaces
        except Exception as e:
            self.console.print(f"[red]Error listing namespaces: {str(e)}[/red]")
            return []
    
    def list_tables_in_namespace(self, namespace: Tuple[str, ...]) -> List[str]:
        """List all tables in a given namespace"""
        try:
            tables = list(self.catalog.list_tables(namespace))
            return [table[1] for table in tables]  # Extract table names
        except Exception as e:
            self.console.print(f"[red]Error listing tables in namespace {namespace}: {str(e)}[/red]")
            return []
    
    def get_all_tables(self) -> Dict[Tuple[str, ...], List[str]]:
        """Get all tables across all namespaces"""
        all_tables = {}
        namespaces = self.list_namespaces()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Scanning namespaces...", total=len(namespaces))
            
            for namespace in namespaces:
                tables = self.list_tables_in_namespace(namespace)
                all_tables[namespace] = tables
                progress.advance(task)
        
        return all_tables
    
    def get_table_info(self, namespace: Tuple[str, ...], table_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a table"""
        try:
            table = self.catalog.load_table((*namespace, table_name))
            
            # Get schema information
            schema = table.schema()
            columns = []
            for field in schema.fields:
                columns.append({
                    "name": field.name,
                    "type": str(field.field_type),
                    "required": field.required,
                    "doc": field.doc
                })
            
            # Get table metadata
            metadata = table.metadata
            
            info = {
                "namespace": namespace,
                "name": table_name,
                "location": metadata.location,
                "schema_id": metadata.current_schema_id,
                "columns": columns,
                "partition_spec": str(table.spec()),
                "sort_orders": [str(order) for order in metadata.sort_orders],
                "properties": metadata.properties,
                "snapshots_count": len(metadata.snapshots) if metadata.snapshots else 0,
                "current_snapshot_id": metadata.current_snapshot_id,
                "created_at": datetime.fromtimestamp(metadata.snapshots[0].timestamp_ms / 1000) if metadata.snapshots else None
            }
            
            return info
            
        except Exception as e:
            self.console.print(f"[red]Error getting table info for {namespace}.{table_name}: {str(e)}[/red]")
            return None
    
    def preview_table_data(self, namespace: Tuple[str, ...], table_name: str, limit: int = 10) -> Optional[pd.DataFrame]:
        """Preview table data"""
        try:
            table = self.catalog.load_table((*namespace, table_name))
            
            # Use PyIceberg to scan the table
            scan = table.scan(limit=limit)
            df = scan.to_pandas()
            
            return df
            
        except Exception as e:
            self.console.print(f"[red]Error previewing table {namespace}.{table_name}: {str(e)}[/red]")
            self.console.print(f"[yellow]Details: {traceback.format_exc()}[/yellow]")
            return None
    
    def display_namespace_tree(self):
        """Display all namespaces and tables in a tree format"""
        all_tables = self.get_all_tables()
        
        if not all_tables:
            self.console.print("[yellow]No namespaces found or error occurred[/yellow]")
            return
        
        tree = Tree("🏠 Lakehouse Tables")
        
        total_tables = 0
        for namespace, tables in all_tables.items():
            namespace_str = ".".join(namespace) if namespace else "default"
            namespace_node = tree.add(f"📁 {namespace_str} ({len(tables)} tables)")
            
            for table in tables:
                namespace_node.add(f"📊 {table}")
                total_tables += 1
        
        self.console.print(Panel(tree, title=f"Lakehouse Overview - {len(all_tables)} namespaces, {total_tables} tables"))
    
    def display_table_info(self, namespace: Tuple[str, ...], table_name: str):
        """Display detailed table information"""
        info = self.get_table_info(namespace, table_name)
        
        if not info:
            return
        
        namespace_str = ".".join(namespace) if namespace else "default"
        
        # Create main info panel
        main_info = f"""
[bold]Namespace:[/bold] {namespace_str}
[bold]Table:[/bold] {table_name}
[bold]Location:[/bold] {info['location']}
[bold]Schema ID:[/bold] {info['schema_id']}
[bold]Snapshots:[/bold] {info['snapshots_count']}
[bold]Current Snapshot:[/bold] {info['current_snapshot_id']}
[bold]Created:[/bold] {info['created_at']}
        """
        
        self.console.print(Panel(main_info.strip(), title="📊 Table Information"))
        
        # Display schema
        schema_table = RichTable(title="Schema")
        schema_table.add_column("Column", style="cyan", no_wrap=True)
        schema_table.add_column("Type", style="magenta")
        schema_table.add_column("Required", style="green")
        schema_table.add_column("Description", style="yellow")
        
        for col in info['columns']:
            schema_table.add_row(
                col['name'],
                col['type'],
                "✅" if col['required'] else "❌",
                col['doc'] or ""
            )
        
        self.console.print(schema_table)
        
        # Display partition info if available
        if info['partition_spec'] and info['partition_spec'] != "[]":
            self.console.print(Panel(f"[bold]Partition Spec:[/bold] {info['partition_spec']}", title="🔀 Partitioning"))
        
        # Display properties if available
        if info['properties']:
            props_text = "\n".join([f"[bold]{k}:[/bold] {v}" for k, v in info['properties'].items()])
            self.console.print(Panel(props_text, title="⚙️ Properties"))
    
    def display_table_preview(self, namespace: Tuple[str, ...], table_name: str, limit: int = 10):
        """Display table data preview"""
        namespace_str = ".".join(namespace) if namespace else "default"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(f"Loading data from {namespace_str}.{table_name}...", total=None)
            
            df = self.preview_table_data(namespace, table_name, limit)
            
            if df is not None and not df.empty:
                progress.update(task, description=f"✅ Loaded {len(df)} rows")
                
                # Create rich table for display
                data_table = RichTable(title=f"Data Preview - {namespace_str}.{table_name} (showing {len(df)} rows)")
                
                # Add columns
                for col in df.columns:
                    data_table.add_column(str(col), overflow="fold")
                
                # Add rows
                for _, row in df.iterrows():
                    data_table.add_row(*[str(val) for val in row])
                
                self.console.print(data_table)
                
                # Show data types
                types_info = "\n".join([f"[bold]{col}:[/bold] {dtype}" for col, dtype in df.dtypes.items()])
                self.console.print(Panel(types_info, title="📋 Data Types"))
                
            else:
                progress.update(task, description="❌ No data found or error occurred")
    
    def search_tables(self, search_term: str) -> List[Tuple[Tuple[str, ...], str]]:
        """Search for tables by name across all namespaces"""
        all_tables = self.get_all_tables()
        matches = []
        
        for namespace, tables in all_tables.items():
            for table in tables:
                if search_term.lower() in table.lower():
                    matches.append((namespace, table))
        
        return matches
