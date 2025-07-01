"""
API routes for Lakehouse Explorer Web Application
"""

from flask import Blueprint, jsonify, request, current_app
import traceback

api_bp = Blueprint('api', __name__)

def get_explorer():
    """Get the explorer instance from app config"""
    return current_app.config.get('EXPLORER')

@api_bp.route('/namespaces')
def get_namespaces():
    """Get all namespaces"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        namespaces = explorer.list_namespaces()
        # Convert tuples to strings for JSON serialization
        namespace_list = [".".join(ns) if ns else "default" for ns in namespaces]
        
        return jsonify({
            'namespaces': namespace_list,
            'count': len(namespace_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tables')
def get_all_tables():
    """Get all tables organized by namespace"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        all_tables = explorer.get_all_tables()
        
        # Convert to JSON-serializable format
        result = {}
        total_tables = 0
        
        for namespace, tables in all_tables.items():
            namespace_str = ".".join(namespace) if namespace else "default"
            result[namespace_str] = {
                'tables': tables,
                'count': len(tables)
            }
            total_tables += len(tables)
        
        return jsonify({
            'namespaces': result,
            'total_namespaces': len(result),
            'total_tables': total_tables
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tables/<namespace>')
def get_tables_in_namespace(namespace):
    """Get tables in a specific namespace"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        # Convert namespace string back to tuple
        if namespace == "default":
            namespace_tuple = ()
        else:
            namespace_tuple = tuple(namespace.split('.'))
        
        tables = explorer.list_tables_in_namespace(namespace_tuple)
        
        return jsonify({
            'namespace': namespace,
            'tables': tables,
            'count': len(tables)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/table/<namespace>/<table_name>/schema')
def get_table_schema(namespace, table_name):
    """Get table schema"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        # Convert namespace string back to tuple
        if namespace == "default":
            namespace_tuple = ()
        else:
            namespace_tuple = tuple(namespace.split('.'))
        
        schema = explorer.get_table_schema(namespace_tuple, table_name)
        
        if schema is None:
            return jsonify({'error': 'Table not found or error occurred'}), 404
        
        return jsonify({
            'namespace': namespace,
            'table_name': table_name,
            'schema': schema
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/table/<namespace>/<table_name>/metadata')
def get_table_metadata(namespace, table_name):
    """Get table metadata"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        # Convert namespace string back to tuple
        if namespace == "default":
            namespace_tuple = ()
        else:
            namespace_tuple = tuple(namespace.split('.'))
        
        metadata = explorer.get_table_metadata(namespace_tuple, table_name)
        
        if metadata is None:
            return jsonify({'error': 'Table not found or error occurred'}), 404
        
        return jsonify({
            'namespace': namespace,
            'table_name': table_name,
            'metadata': metadata
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/table/<namespace>/<table_name>/preview')
def preview_table(namespace, table_name):
    """Preview table data"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        # Get limit from query parameters
        limit = request.args.get('limit', 10, type=int)
        if limit > 1000:  # Prevent excessive data loading
            limit = 1000
        
        # Convert namespace string back to tuple
        if namespace == "default":
            namespace_tuple = ()
        else:
            namespace_tuple = tuple(namespace.split('.'))
        
        preview_data = explorer.preview_table_data(namespace_tuple, table_name, limit)
        
        if preview_data is None:
            return jsonify({'error': 'Table not found or error occurred'}), 404
        
        return jsonify({
            'namespace': namespace,
            'table_name': table_name,
            'preview': preview_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/search')
def search_tables():
    """Search for tables by name"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({'error': 'Search term is required'}), 400
        
        results = explorer.search_tables(search_term)
        
        return jsonify({
            'search_term': search_term,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/table/<namespace>/<table_name>/query', methods=['POST'])
def query_table():
    """Execute SQL query on table using DuckDB"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'SQL query is required in request body'}), 400
        
        namespace = request.view_args['namespace']
        table_name = request.view_args['table_name']
        sql_query = data['query']
        limit = data.get('limit', 100)
        
        # Convert namespace string back to tuple
        if namespace == "default":
            namespace_tuple = ()
        else:
            namespace_tuple = tuple(namespace.split('.'))
        
        result = explorer.execute_sql_query(namespace_tuple, table_name, sql_query, limit)
        
        return jsonify({
            'namespace': namespace,
            'table_name': table_name,
            'query_result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/table/<namespace>/<table_name>/statistics')
def get_table_statistics(namespace, table_name):
    """Get table statistics using DuckDB"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        # Convert namespace string back to tuple
        if namespace == "default":
            namespace_tuple = ()
        else:
            namespace_tuple = tuple(namespace.split('.'))
        
        statistics = explorer.get_table_statistics(namespace_tuple, table_name)
        
        if statistics is None:
            return jsonify({'error': 'Table not found or error occurred'}), 404
        
        return jsonify({
            'namespace': namespace,
            'table_name': table_name,
            'statistics': statistics
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/connection')
def get_connection_info():
    """Get connection information"""
    try:
        explorer = get_explorer()
        if not explorer:
            return jsonify({'error': 'Explorer not initialized'}), 500
        
        connection_info = explorer.get_connection_info()
        
        return jsonify({
            'connection': connection_info,
            'status': 'connected'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.errorhandler(404)
def api_not_found(error):
    return jsonify({'error': 'API endpoint not found'}), 404

@api_bp.errorhandler(500)
def api_internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
