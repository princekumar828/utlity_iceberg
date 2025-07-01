# 🚀 Cross-Platform Installation Guide

This guide provides step-by-step instructions for setting up the Lakehouse Explorer on different operating systems.

## 📋 Prerequisites

- **Python 3.8 or higher** installed on your system
- **Git** (for cloning the repository)
- **Access to existing lakehouse infrastructure**:
  - Nessie catalog server
  - MinIO or S3-compatible storage
  - Network connectivity to both services

## 🖥️ Platform-Specific Setup

### 🪟 Windows Setup

#### Option 1: Automated Setup (Recommended)
```cmd
# Clone the repository
git clone <your-repo-url>
cd lakehouse-explorer

# Run automated setup
setup.bat

# Configure your connection
quick_setup.bat

# Start web interface
start_web.bat
```

#### Option 2: Manual Setup
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test setup
python test_setup.py
```

#### PowerShell Users
If you prefer PowerShell, you can use these commands:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 🐧 Linux Setup

#### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd lakehouse-explorer

# Make scripts executable
chmod +x *.sh

# Run automated setup
./setup.sh

# Configure your connection
./quick_setup.sh

# Start web interface
./start_web.sh
```

#### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test setup
python test_setup.py
```

#### Ubuntu/Debian Specific
```bash
# Install Python and pip if not already installed
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Clone and setup
git clone <your-repo-url>
cd lakehouse-explorer
./setup.sh
```

#### CentOS/RHEL/Fedora Specific
```bash
# Install Python and pip if not already installed
sudo yum install python3 python3-pip git  # CentOS/RHEL
# OR
sudo dnf install python3 python3-pip git  # Fedora

# Clone and setup
git clone <your-repo-url>
cd lakehouse-explorer
./setup.sh
```

### 🍎 macOS Setup

#### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone <your-repo-url>
cd lakehouse-explorer

# Make scripts executable
chmod +x *.sh

# Run automated setup
./setup.sh

# Configure your connection
./quick_setup.sh

# Start web interface
./start_web.sh
```

#### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test setup
python test_setup.py
```

#### Using Homebrew
```bash
# Install Python if not already installed
brew install python3 git

# Clone and setup
git clone <your-repo-url>
cd lakehouse-explorer
./setup.sh
```

## ⚙️ Configuration

After installation, you need to configure the connection to your lakehouse:

### Option 1: Environment Variables (Recommended)

#### Windows
```cmd
# Run the configuration wizard
quick_setup.bat
```

#### Linux/macOS
```bash
# Run the configuration wizard
./quick_setup.sh
```

### Option 2: Manual Configuration

Create a `.env` file with your connection details:
```bash
NESSIE_URI=http://your-nessie-host:19120/api/v1
S3_ENDPOINT=http://your-minio-host:9000
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
WAREHOUSE_PATH=s3://your-warehouse-bucket/
NESSIE_REF=main
S3_REGION=us-east-1
SSL_VERIFY=false
```

Or create a `config.json` file:
```json
{
  "nessie_uri": "http://your-nessie-host:19120/api/v1",
  "nessie_ref": "main",
  "s3_endpoint": "http://your-minio-host:9000",
  "s3_access_key": "your-access-key",
  "s3_secret_key": "your-secret-key",
  "s3_region": "us-east-1",
  "warehouse_path": "s3://your-warehouse-bucket/",
  "ssl_verify": false
}
```

## 🧪 Testing Your Setup

### Test Installation
```bash
# Windows
python test_setup.py

# Linux/macOS
python test_setup.py
```

### Test Connection
```bash
# Windows (with environment variables)
python main.py overview

# Windows (with config file)
python main.py --config config.json overview

# Linux/macOS (with environment variables)
python main.py overview

# Linux/macOS (with config file)
python main.py --config config.json overview
```

## 🚀 Running the Application

### Web Interface

#### Windows
```cmd
start_web.bat
```

#### Linux/macOS
```bash
./start_web.sh
```

#### Manual Start (All Platforms)
```bash
# Activate virtual environment first
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

python web_app.py
```

### Command Line Interface

```bash
# Interactive mode
python main.py interactive

# Get overview
python main.py overview

# List all tables
python main.py list-tables

# Show table details
python main.py show-table namespace.table_name

# Preview table data
python main.py preview-table namespace.table_name --limit 10
```

## 🐳 Docker Alternative (All Platforms)

If you prefer using Docker:

```bash
# Build the image
docker build -t lakehouse-explorer .

# Run with environment variables
docker run -p 5000:5000 \
  -e NESSIE_URI=http://your-nessie:19120/api/v1 \
  -e S3_ENDPOINT=http://your-minio:9000 \
  -e S3_ACCESS_KEY=your-key \
  -e S3_SECRET_KEY=your-secret \
  -e WAREHOUSE_PATH=s3://warehouse/ \
  lakehouse-explorer

# Or use docker-compose
docker-compose up
```

## 🔧 Troubleshooting

### Common Issues

#### Python Not Found
- **Windows**: Install Python from [python.org](https://python.org) and ensure "Add to PATH" is checked
- **Linux**: Install using your package manager (`apt`, `yum`, `dnf`)
- **macOS**: Install using Homebrew or from [python.org](https://python.org)

#### Permission Denied (Linux/macOS)
```bash
chmod +x *.sh
```

#### Virtual Environment Issues
```bash
# Remove and recreate
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Recreate
python -m venv venv
```

#### Connection Issues
- Verify your lakehouse services are running
- Check firewall/network connectivity
- Validate credentials and endpoints
- Review SSL/TLS settings

#### Port Already in Use
```bash
# Find process using port 5000
# Linux/macOS:
lsof -i :5000

# Windows:
netstat -ano | findstr :5000

# Kill the process or use a different port
python web_app.py --port 5001
```

## 📖 Next Steps

After successful installation:

1. **Explore the Web Interface**: Navigate to http://localhost:5000
2. **Try the CLI**: Run `python main.py interactive`
3. **Read the Documentation**: Check `README.md` for detailed usage
4. **Customize**: Modify templates and styles as needed

## 🤝 Contributing

For development setup:
1. Fork the repository
2. Follow the installation guide for your platform
3. Make your changes
4. Submit a pull request
