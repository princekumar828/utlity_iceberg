# 🚀 Getting Started with Lakehouse Explorer

This guide will walk you through setting up and using the Lakehouse Table Explorer with your existing lakehouse infrastructure.

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ **Existing Lakehouse Setup**: Nessie catalog + Iceberg tables + MinIO/S3 storage
- ✅ **Python 3.8+** installed on your system
- ✅ **Network access** to your Nessie and MinIO endpoints
- ✅ **Valid credentials** for your MinIO/S3 storage

## 🛠️ Step 1: Initial Setup

### Option A: Automated Setup (Recommended)
```bash
# Clone or navigate to the utility directory
cd /path/to/utlity

# Run the automated setup
./setup.sh
```

### Option B: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Step 2: Configure Connection to Your Lakehouse

You have two configuration options:

### Option A: Environment Variables (Recommended)
```bash
# Run the interactive setup
./quick_setup.sh

# Choose option "1" for environment variables
# Provide your lakehouse details when prompted:
# - Nessie URI: http://your-nessie-host:19120/api/v1
# - S3 Endpoint: http://your-minio-host:9000
# - S3 Access Key: your-access-key
# - S3 Secret Key: your-secret-key
# - Warehouse Path: s3://your-bucket-name/
```

### Option B: Configuration File
```bash
# Run the interactive setup
./quick_setup.sh

# Choose option "2" for configuration file
# Provide your lakehouse details when prompted
# This creates a config.json file
```

## 🧪 Step 3: Test Your Connection

The setup script automatically tests your connection. You should see:
```
✅ Configuration loaded successfully
   Nessie: http://your-nessie-host:19120/api/v1
   S3: http://your-minio-host:9000
   Warehouse: s3://your-bucket/
✅ Connected to lakehouse successfully!
✅ Found X namespace(s)
```

If you see errors, check:
- Your lakehouse services are running
- Network connectivity to Nessie and MinIO
- Credentials are correct
- Firewall/security group settings

## 🎯 Step 4: Start Exploring Your Data

### Option A: Web Interface (Recommended for Beginners)

1. **Start the web server:**
   ```bash
   # If using environment variables:
   source .env && ./start_web.sh
   
   # If using config file:
   ./start_web.sh
   ```

2. **Open your browser:**
   - Navigate to: http://localhost:5000
   - You'll see a modern web interface showing your namespaces and tables

3. **Explore features:**
   - 🏠 **Browse namespaces** in the sidebar
   - 📊 **Click tables** to view schema and metadata
   - 👁️ **Preview data** with the "Preview" button
   - 🔍 **Search tables** using the search box

### Option B: Command Line Interface

1. **Activate your environment:**
   ```bash
   source venv/bin/activate
   
   # If using environment variables:
   source .env
   ```

2. **Basic commands:**
   ```bash
   # Overview of all namespaces and tables
   python main.py overview
   
   # Interactive mode (user-friendly)
   python main.py interactive
   
   # List all tables
   python main.py list-tables
   
   # Show specific table details
   python main.py show-table namespace.table_name
   
   # Preview table data
   python main.py preview-table namespace.table_name --limit 10
   ```

3. **With config file:**
   ```bash
   python main.py --config config.json overview
   python main.py --config config.json interactive
   ```

## 📖 Common Usage Patterns

### 1. Daily Data Exploration
```bash
# Quick overview
python main.py overview

# Interactive exploration
python main.py interactive
```

### 2. Table Investigation
```bash
# Find tables containing "sales"
python main.py list-tables | grep sales

# Get table schema
python main.py show-table analytics.sales_data

# Preview recent data
python main.py preview-table analytics.sales_data --limit 20
```

### 3. Web-based Exploration
```bash
# Start web interface
./start_web.sh

# Access at http://localhost:5000
# - Browse namespaces visually
# - Search across all tables
# - Preview data with pagination
```

## 🔧 Configuration Examples

### Production Environment
```bash
# .env file for production
NESSIE_URI=https://nessie.yourcompany.com/api/v1
S3_ENDPOINT=https://s3.yourcompany.com
S3_ACCESS_KEY=your_production_key
S3_SECRET_KEY=your_production_secret
WAREHOUSE_PATH=s3://data-lake-prod/warehouse/
NESSIE_REF=main
SSL_VERIFY=true
```

### Development Environment
```bash
# .env file for development
NESSIE_URI=http://localhost:19120/api/v1
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
WAREHOUSE_PATH=s3://warehouse/
SSL_VERIFY=false
```

## 🚨 Troubleshooting

### Connection Issues
```bash
# Test basic connectivity
curl http://your-nessie-host:19120/api/v1/config
curl http://your-minio-host:9000/minio/health/live

# Check configuration
python -c "from config import LakehouseConfig; print(LakehouseConfig.from_env())"
```

### Common Errors

1. **"No matching distribution found for pynessie-client"**
   - ✅ Already fixed in requirements.txt - use PyIceberg's built-in Nessie support

2. **"Connection refused"**
   - Check if Nessie/MinIO services are running
   - Verify host/port in configuration

3. **"Access denied"**
   - Verify S3 credentials
   - Check bucket permissions

4. **"SSL verification failed"**
   - Set `SSL_VERIFY=false` for self-signed certificates

## 🎯 Next Steps

Once you're comfortable with the basics:

1. **Explore Advanced Features:**
   - Table partitioning information
   - Schema evolution history
   - Data lineage (if available)

2. **Customize the Interface:**
   - Modify web templates in `templates/`
   - Adjust styling in `static/`
   - Add custom CLI commands

3. **Integration:**
   - Use as a library in your own scripts
   - Integrate with Jupyter notebooks
   - Connect to BI tools

## 📞 Need Help?

- Check the main `README.md` for detailed API documentation
- Run `python main.py --help` for CLI options
- Use `python main.py interactive` for guided exploration
- Review configuration examples in `sample-config.json`

---

**Happy exploring your lakehouse data! 🎉**
