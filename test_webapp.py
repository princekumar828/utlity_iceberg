#!/usr/bin/env python3
"""
Quick test script to verify the Lakehouse Explorer web app structure
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing web app structure...")
    
    try:
        import flask
        print("✅ Flask")
    except ImportError:
        print("❌ Flask - run: pip install flask")
        return False
    
    try:
        import flask_cors
        print("✅ Flask-CORS")
    except ImportError:
        print("❌ Flask-CORS - run: pip install flask-cors")
        return False
    
    try:
        import pandas
        print("✅ Pandas")
    except ImportError:
        print("❌ Pandas - run: pip install pandas")
        return False
    
    try:
        from pyiceberg.catalog import load_catalog
        print("✅ PyIceberg")
    except ImportError:
        print("❌ PyIceberg - run: pip install 'pyiceberg[s3fs]'")
        return False
    
    try:
        import duckdb
        print("✅ DuckDB")
    except ImportError:
        print("❌ DuckDB - run: pip install duckdb")
        return False
    
    return True

def test_structure():
    """Test if the app structure is correct"""
    print("\n🔧 Testing app structure...")
    
    required_files = [
        'app.py',
        'app/__init__.py',
        'app/core/__init__.py',
        'app/core/config.py',
        'app/core/explorer.py',
        'app/api/__init__.py',
        'app/api/routes.py',
        'app/templates',
        'app/static',
        'config/sample.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        sys.path.append('.')
        from app.core.config import LakehouseConfig, get_config
        print("✅ Configuration module imported successfully")
        
        # Test sample config loading
        if os.path.exists("config/sample.json"):
            config = LakehouseConfig.from_file("config/sample.json")
            print("✅ Sample configuration loaded successfully")
            print(f"   Nessie URI: {config.nessie_uri}")
        else:
            print("⚠️  config/sample.json not found")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Lakehouse Explorer Web App - Structure Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_structure,
        test_config
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All tests passed! Your web app is ready.")
        print("\n🚀 Next steps:")
        print("1. Create config.json with your lakehouse settings")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("💡 Try running: pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
