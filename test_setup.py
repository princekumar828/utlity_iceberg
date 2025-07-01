#!/usr/bin/env python3
"""
Quick test script to verify the lakehouse explorer setup
"""

import sys
import json
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import click
        print("✅ click")
    except ImportError:
        print("❌ click - run: pip install click")
        return False
    
    try:
        import rich
        print("✅ rich")
    except ImportError:
        print("❌ rich - run: pip install rich")
        return False
    
    try:
        import pandas
        print("✅ pandas")
    except ImportError:
        print("❌ pandas - run: pip install pandas")
        return False
    
    try:
        import boto3
        print("✅ boto3")
    except ImportError:
        print("❌ boto3 - run: pip install boto3")
        return False
    
    try:
        import s3fs
        print("✅ s3fs")
    except ImportError:
        print("❌ s3fs - run: pip install s3fs")
        return False
    
    try:
        from pyiceberg.catalog import load_catalog
        print("✅ pyiceberg (includes Nessie catalog support)")
    except ImportError:
        print("❌ pyiceberg - run: pip install 'pyiceberg[s3fs]'")
        return False
    
    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests - run: pip install requests")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import LakehouseConfig
        print("✅ Configuration module imported successfully")
        
        # Test sample config loading
        if Path("sample-config.json").exists():
            config = LakehouseConfig.from_file("sample-config.json")
            print("✅ Sample configuration loaded successfully")
            print(f"   Nessie URI: {config.nessie_uri}")
            print(f"   S3 Endpoint: {config.s3_endpoint}")
            print(f"   Warehouse: {config.warehouse_path}")
        else:
            print("⚠️  sample-config.json not found")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_main_module():
    """Test main module imports"""
    print("\n🎯 Testing main module...")
    
    try:
        from main import cli
        print("✅ Main CLI module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Main module test failed: {e}")
        return False

def test_explorer_module():
    """Test explorer module imports"""
    print("\n🔍 Testing explorer module...")
    
    try:
        from lakehouse_explorer import LakehouseExplorer
        print("✅ Explorer module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Explorer module test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Lakehouse Explorer - Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_main_module,
        test_explorer_module
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 40)
    if all(results):
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Update sample-config.json with your actual values")
        print("2. Run: python main.py --config sample-config.json overview")
        print("   OR set environment variables and run: python main.py overview")
        print("3. Try: python main.py interactive")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("💡 Try running: pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
