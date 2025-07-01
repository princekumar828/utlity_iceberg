# Lakehouse Table Explorer

A powerful utility tool to explore and view Apache Iceberg tables in your lakehouse setup with Nessie catalog and MinIO/S3 storage. Available as both a **modern web interface** and a **command-line tool**.

![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🌐 **Modern Web Interface**: Beautiful, responsive web UI for easy exploration
- 🏠 **Namespace Overview**: View all namespaces and tables in a tree structure
- 📊 **Table Information**: Get detailed schema, metadata, and properties for any table
- 👁️ **Data Preview**: Preview table contents with configurable row limits
- 🔍 **Search**: Search for tables across all namespaces
- 🖥️ **Interactive CLI Mode**: User-friendly interactive command-line interface
- ⚙️ **Flexible Configuration**: Support for config files and environment variables
- 📱 **Responsive Design**: Works great on desktop, tablet, and mobile devices
- 🐳 **Docker Support**: Optional containerized deployment
- 🔄 **Cross-Platform**: Works on Windows, Linux, and macOS

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Access to existing Nessie catalog and MinIO/S3 storage
- Network connectivity to your lakehouse components

### Installation

#### Option 1: Quick Setup (All Platforms)
```bash
# Clone the repository
git clone <your-repo-url>
cd lakehouse-explorer

# Run platform-specific setup
# On Windows:
setup.bat

# On Linux/macOS:
./setup.sh
```

#### Option 2: Manual Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a configuration file using the setup command:

```bash
python main.py setup --output config.json
```

Then edit the file with your lakehouse details:

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

## 🚀 Usage

### Web Interface (Recommended)

Start the web server:

```bash
# Windows
start_web.bat

# Linux/macOS
./start_web.sh

# Manual (all platforms)
python web_app.py
```

Open your browser to http://localhost:5000 and explore your lakehouse visually.

### Command Line Interface

```bash
# Interactive mode (guided exploration)
python main.py interactive

# Get overview of all namespaces and tables
python main.py overview

# List all tables
python main.py list-tables

# Show table schema and metadata
python main.py show-table namespace.table_name

# Preview table data
python main.py preview-table namespace.table_name --limit 10

# Using configuration file
python main.py --config config.json overview
```

## 📚 Documentation

- **[Installation Guide](INSTALLATION.md)** - Detailed setup for Windows, Linux, and macOS
- **[Quick Start](QUICK_START.md)** - 5-minute setup checklist
- **[Getting Started](GETTING_STARTED.md)** - Comprehensive usage guide

## 🐳 Docker Support

For containerized deployment:

```bash
# Build and run
docker build -t lakehouse-explorer .
docker run -p 5000:5000 lakehouse-explorer

# Or use docker-compose
docker-compose up
```

## 🛠️ Development

### Prerequisites
- Python 3.8+
- Virtual environment
- Access to Nessie + MinIO/S3

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd lakehouse-explorer

# Platform-specific setup
# Windows: setup.bat
# Linux/macOS: ./setup.sh

# Configure connection
# Windows: quick_setup.bat  
# Linux/macOS: ./quick_setup.sh
```

### Testing
```bash
python test_setup.py
```

## 📁 Project Structure

```
lakehouse-explorer/
├── 📄 README.md              # This file
├── 📄 INSTALLATION.md        # Cross-platform setup guide
├── 📄 requirements.txt       # Python dependencies
├── 🐍 main.py               # CLI entry point
├── 🐍 config.py             # Configuration management
├── 🐍 lakehouse_explorer.py # Core exploration logic
├── 🐍 web_app.py            # Web interface
├── 🐍 test_setup.py         # Setup verification
├── 📁 templates/            # Web UI templates
├── 📁 static/              # CSS, JS, images
├── 🔧 setup.sh/.bat        # Platform setup scripts
├── 🔧 quick_setup.sh/.bat   # Configuration wizards
├── 🔧 start_web.sh/.bat     # Web server launchers
├── 🐳 Dockerfile           # Container definition
├── 🐳 docker-compose.yml   # Multi-container setup
└── 📄 .env.template        # Environment variables template
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 Check the [Installation Guide](INSTALLATION.md) for setup issues
- 🐛 Report bugs via GitHub Issues
- 💡 Feature requests welcome via GitHub Issues
- 📧 Contact maintainers for questions

## 🙏 Acknowledgments

- [Apache Iceberg](https://iceberg.apache.org/) - Table format
- [Project Nessie](https://projectnessie.org/) - Catalog and versioning
- [MinIO](https://min.io/) - S3-compatible storage
- [PyIceberg](https://py.iceberg.apache.org/) - Python integration
