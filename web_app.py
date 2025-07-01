#!/usr/bin/env python3
"""
Flask Web Interface for Lakehouse Explorer
A modern web UI to explore Iceberg tables in your lakehouse setup.
"""

import os
import json
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from config import LakehouseConfig
from lakehouse_explorer import LakehouseExplorer

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Global variables
explorer = None
config = None

def init_explorer():
    """Initialize the lakehouse explorer"""
    global explorer, config
    
    try:
        # Try to load configuration
        config_file = os.environ.get('LAKEHOUSE_CONFIG_FILE', 'sample-config.json')
        
        if os.path.exists(config_file):
            config = LakehouseConfig.from_file(config_file)
        else:
            # Try environment variables
            config = LakehouseConfig.from_env()
        
        explorer = LakehouseExplorer(config)
        return True, "Connected successfully"
        
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Check connection status"""
    global explorer
    
    if explorer is None:
        success, message = init_explorer()
        if not success:
            return jsonify({
                'status': 'error',
                'message': f'Connection failed: {message}',
                'connected': False
            })
    
    return jsonify({
        'status': 'success',
        'message': 'Connected to lakehouse',
        'connected': True,
        'config': {
            'nessie_uri': config.nessie_uri if config else None,
            's3_endpoint': config.s3_endpoint if config else None,
            'warehouse_path': config.warehouse_path if config else None
        }
    })

@app.route('/api/namespaces')
def api_namespaces():
    """Get all namespaces"""
    global explorer
    
    if explorer is None:
        return jsonify({'status': 'error', 'message': 'Not connected'})
    
    try:
        namespaces = explorer.list_namespaces()
        return jsonify({
            'status': 'success',
            'namespaces': ['.'.join(ns) if ns else 'default' for ns in namespaces]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/tables')
def api_tables():
    """Get all tables, optionally filtered by namespace"""
    global explorer
    
    if explorer is None:
        return jsonify({'status': 'error', 'message': 'Not connected'})
    
    namespace_filter = request.args.get('namespace')
    
    try:
        if namespace_filter:
            # Get tables for specific namespace
            namespace_tuple = tuple(namespace_filter.split('.')) if namespace_filter != 'default' else ()
            tables = explorer.list_tables_in_namespace(namespace_tuple)
            return jsonify({
                'status': 'success',
                'tables': [{'namespace': namespace_filter, 'name': table} for table in tables]
            })
        else:
            # Get all tables
            all_tables = explorer.get_all_tables()
            tables_list = []
            
            for namespace, tables in all_tables.items():
                namespace_str = '.'.join(namespace) if namespace else 'default'
                for table in tables:
                    tables_list.append({
                        'namespace': namespace_str,
                        'name': table,
                        'full_name': f"{namespace_str}.{table}"
                    })
            
            return jsonify({
                'status': 'success',
                'tables': tables_list
            })
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/table/info')
def api_table_info():
    """Get detailed table information"""
    global explorer
    
    if explorer is None:
        return jsonify({'status': 'error', 'message': 'Not connected'})
    
    namespace = request.args.get('namespace', '')
    table_name = request.args.get('table')
    
    if not table_name:
        return jsonify({'status': 'error', 'message': 'Table name is required'})
    
    try:
        namespace_tuple = tuple(namespace.split('.')) if namespace and namespace != 'default' else ()
        info = explorer.get_table_info(namespace_tuple, table_name)
        
        if info:
            # Convert datetime to string for JSON serialization
            if info.get('created_at'):
                info['created_at'] = info['created_at'].isoformat()
            
            return jsonify({
                'status': 'success',
                'table_info': info
            })
        else:
            return jsonify({'status': 'error', 'message': 'Table not found or error occurred'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/table/preview')
def api_table_preview():
    """Preview table data"""
    global explorer
    
    if explorer is None:
        return jsonify({'status': 'error', 'message': 'Not connected'})
    
    namespace = request.args.get('namespace', '')
    table_name = request.args.get('table')
    limit = int(request.args.get('limit', 10))
    
    if not table_name:
        return jsonify({'status': 'error', 'message': 'Table name is required'})
    
    try:
        namespace_tuple = tuple(namespace.split('.')) if namespace and namespace != 'default' else ()
        df = explorer.preview_table_data(namespace_tuple, table_name, limit)
        
        if df is not None and not df.empty:
            # Convert DataFrame to JSON-friendly format
            data = {
                'columns': df.columns.tolist(),
                'rows': df.values.tolist(),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                'shape': df.shape
            }
            
            return jsonify({
                'status': 'success',
                'data': data
            })
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'columns': [],
                    'rows': [],
                    'dtypes': {},
                    'shape': [0, 0]
                },
                'message': 'No data found'
            })
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/search')
def api_search():
    """Search for tables"""
    global explorer
    
    if explorer is None:
        return jsonify({'status': 'error', 'message': 'Not connected'})
    
    search_term = request.args.get('q', '')
    
    if not search_term:
        return jsonify({'status': 'error', 'message': 'Search term is required'})
    
    try:
        matches = explorer.search_tables(search_term)
        results = []
        
        for namespace, table_name in matches:
            namespace_str = '.'.join(namespace) if namespace else 'default'
            results.append({
                'namespace': namespace_str,
                'name': table_name,
                'full_name': f"{namespace_str}.{table_name}"
            })
        
        return jsonify({
            'status': 'success',
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/overview')
def api_overview():
    """Get overview data for dashboard"""
    global explorer
    
    if explorer is None:
        return jsonify({'status': 'error', 'message': 'Not connected'})
    
    try:
        all_tables = explorer.get_all_tables()
        
        # Calculate statistics
        total_namespaces = len(all_tables)
        total_tables = sum(len(tables) for tables in all_tables.values())
        
        # Prepare namespace data
        namespace_data = []
        for namespace, tables in all_tables.items():
            namespace_str = '.'.join(namespace) if namespace else 'default'
            namespace_data.append({
                'name': namespace_str,
                'table_count': len(tables),
                'tables': tables
            })
        
        return jsonify({
            'status': 'success',
            'overview': {
                'total_namespaces': total_namespaces,
                'total_tables': total_tables,
                'namespaces': namespace_data
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Initialize explorer on startup
    success, message = init_explorer()
    if success:
        print(f"✅ Connected to lakehouse: {message}")
    else:
        print(f"⚠️  Warning: {message}")
        print("You can still start the web interface and configure connection later.")
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Lakehouse Explorer Web Interface on port {port}")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
