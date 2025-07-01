"""
Lakehouse Explorer Web Application
A web-based tool to explore Apache Iceberg tables in your lakehouse setup.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
from app.core.config import get_config
from app.core.explorer import LakehouseExplorer
from app.api.routes import api_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Load configuration
    try:
        config = get_config()
        app.config['LAKEHOUSE_CONFIG'] = config
        
        # Initialize explorer
        explorer = LakehouseExplorer(config)
        app.config['EXPLORER'] = explorer
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your configuration and ensure your lakehouse is accessible.")
        return None
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Main routes
    @app.route('/')
    def index():
        """Main application page"""
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'service': 'lakehouse-explorer'})
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    if app:
        print("🌐 Starting Lakehouse Explorer Web Application...")
        print("📍 Open your browser to: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to start application. Please check your configuration.")
        exit(1)
