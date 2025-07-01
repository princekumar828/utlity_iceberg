"""
Configuration management for Lakehouse Explorer Web App
"""

import os
import json
from typing import Optional
from dataclasses import dataclass

@dataclass
class LakehouseConfig:
    """Configuration for lakehouse connections"""
    # Required Nessie configuration
    nessie_uri: str
    
    # Required MinIO/S3 configuration
    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    warehouse_path: str
    
    # Optional Nessie configuration
    nessie_ref: str = "main"
    nessie_auth_type: Optional[str] = None
    nessie_username: Optional[str] = None
    nessie_password: Optional[str] = None
    
    # Optional S3 configuration
    s3_region: str = "us-east-1"
    
    # Additional settings
    ssl_verify: bool = False
    
    @classmethod
    def from_file(cls, config_path: str) -> 'LakehouseConfig':
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return cls(**config_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    @classmethod
    def from_env(cls) -> 'LakehouseConfig':
        """Load configuration from environment variables"""
        required_vars = {
            'NESSIE_URI': 'nessie_uri',
            'S3_ENDPOINT': 's3_endpoint',
            'S3_ACCESS_KEY': 's3_access_key',
            'S3_SECRET_KEY': 's3_secret_key',
            'WAREHOUSE_PATH': 'warehouse_path'
        }
        
        config_data = {}
        missing_vars = []
        
        for env_var, config_key in required_vars.items():
            value = os.getenv(env_var)
            if value is None:
                missing_vars.append(env_var)
            else:
                config_data[config_key] = value
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Optional environment variables
        optional_vars = {
            'NESSIE_REF': 'nessie_ref',
            'NESSIE_AUTH_TYPE': 'nessie_auth_type',
            'NESSIE_USERNAME': 'nessie_username',
            'NESSIE_PASSWORD': 'nessie_password',
            'S3_REGION': 's3_region',
            'SSL_VERIFY': 'ssl_verify'
        }
        
        for env_var, config_key in optional_vars.items():
            value = os.getenv(env_var)
            if value is not None:
                if config_key == 'ssl_verify':
                    config_data[config_key] = value.lower() in ('true', '1', 'yes')
                else:
                    config_data[config_key] = value
        
        return cls(**config_data)
    
    def to_pyiceberg_catalog_config(self):
        """Convert to PyIceberg catalog configuration"""
        config = {
            "type": "rest",
            "uri": self.nessie_uri,
            "ref": self.nessie_ref,
            "s3.endpoint": self.s3_endpoint,
            "s3.access-key-id": self.s3_access_key,
            "s3.secret-access-key": self.s3_secret_key,
            "s3.region": self.s3_region,
            "warehouse": self.warehouse_path,
            "s3.path-style-access": "true"
        }
        
        if not self.ssl_verify:
            config["s3.ssl.enabled"] = "false"
        
        if self.nessie_auth_type:
            config["auth_type"] = self.nessie_auth_type
            if self.nessie_username:
                config["username"] = self.nessie_username
            if self.nessie_password:
                config["password"] = self.nessie_password
        
        return config

def get_config() -> LakehouseConfig:
    """Get configuration from environment or config file"""
    # Try config file first
    if os.path.exists('config.json'):
        return LakehouseConfig.from_file('config.json')
    
    # Try sample config
    if os.path.exists('sample-config.json'):
        return LakehouseConfig.from_file('sample-config.json')
    
    # Try environment variables
    try:
        return LakehouseConfig.from_env()
    except ValueError:
        pass
    
    # Last resort - try config in config directory
    if os.path.exists('config/lakehouse.json'):
        return LakehouseConfig.from_file('config/lakehouse.json')
    
    raise ValueError(
        "No configuration found. Please provide either:\n"
        "1. config.json file in the root directory\n"
        "2. Environment variables (NESSIE_URI, S3_ENDPOINT, etc.)\n"
        "3. config/lakehouse.json file"
    )
