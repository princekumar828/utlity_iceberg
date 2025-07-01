# Lakehouse Explorer - Web Application

A modern web-based tool to explore and view Apache Iceberg tables in your lakehouse setup with Nessie catalog and MinIO/S3 storage.

![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🌐 **Modern Web Interface**: Beautiful, responsive web UI for easy exploration
- 🏠 **Namespace Browser**: View all namespaces and tables in a tree structure
- 📊 **Table Information**: Get detailed schema, metadata, and properties
- 👁️ **Data Preview**: Preview table contents with configurable row limits
- 🔍 **Search**: Search for tables across all namespaces
- 📱 **Responsive Design**: Works great on desktop, tablet, and mobile
- 🚀 **RESTful API**: JSON API for programmatic access
- ⚙️ **Flexible Configuration**: Environment variables or JSON config

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Access to existing Nessie catalog and MinIO/S3 storage
- Network connectivity to your lakehouse components

### Installation & Setup

#### Windows
```cmd
# Clone the repository
git clone <your-repo-url>
cd lakehouse-explorer

# Run the startup script
start.bat
```

#### Linux/macOS
```bash
# Clone the repository
git clone <your-repo-url>
cd lakehouse-explorer

# Make script executable and run
chmod +x start.sh
./start.sh
```

### Configuration

#### Option 1: JSON Configuration File
Create a `config.json` file in the root directory:

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

#### Option 2: Environment Variables
Create a `.env` file:

```bash
NESSIE_URI=http://your-nessie-host:19120/api/v1
NESSIE_REF=main
S3_ENDPOINT=http://your-minio-host:9000
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_REGION=us-east-1
WAREHOUSE_PATH=s3://your-warehouse-bucket/
SSL_VERIFY=false
```

## 🎯 Usage

1. **Start the application**: Run `start.sh` (Linux/macOS) or `start.bat` (Windows)
2. **Open your browser**: Navigate to http://localhost:5000
3. **Explore your data**:
   - Browse namespaces in the sidebar
   - Click on tables to view schema and metadata
   - Use the preview feature to see sample data
   - Search for tables across all namespaces

## 🏗️ Project Structure

```
lakehouse-explorer/
├── 📄 README.md              # This file
├── 📄 requirements.txt       # Python dependencies
├── 📄 LICENSE               # MIT License
├── 🐍 app.py                # Main Flask application
│
├── 📁 app/                  # Application package
│   ├── 📁 core/             # Core business logic
│   │   ├── config.py        # Configuration management
│   │   └── explorer.py      # Lakehouse exploration logic
│   ├── 📁 api/              # REST API endpoints
│   │   └── routes.py        # API route definitions
│   ├── 📁 templates/        # HTML templates
│   │   ├── index.html       # Main web interface
│   │   ├── 404.html         # Error pages
│   │   └── 500.html
│   └── 📁 static/           # CSS, JS, images
│       └── app.js           # Frontend JavaScript
│
├── 📁 config/               # Configuration files
│   └── sample.json          # Sample configuration
│
├── 🔧 start.sh/.bat         # Cross-platform startup scripts
└── 📄 .env.template         # Environment variables template
```

## 🛠️ API Endpoints

The application provides a RESTful API:

- `GET /api/namespaces` - List all namespaces
- `GET /api/tables` - Get all tables organized by namespace
- `GET /api/tables/{namespace}` - Get tables in a specific namespace
- `GET /api/table/{namespace}/{table}/schema` - Get table schema
- `GET /api/table/{namespace}/{table}/metadata` - Get table metadata
- `GET /api/table/{namespace}/{table}/preview?limit=N` - Preview table data
- `GET /api/search?q=term` - Search for tables
- `GET /api/connection` - Get connection information

## 🔧 Development

### Local Development Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration (see above)

# Run in development mode
python app.py
```

### Production Deployment
```bash
# Using Gunicorn (recommended)
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()

# Or with custom configuration
gunicorn -c gunicorn.conf.py app:create_app()
```

## 🎨 Technology Stack

- **Backend**: Python Flask with PyIceberg
- **Frontend**: Vanilla JavaScript with modern CSS
- **Data Processing**: Pandas for data manipulation
- **Storage**: Apache Iceberg tables via Nessie catalog
- **Infrastructure**: MinIO/S3 compatible storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 🐛 Report bugs via GitHub Issues
- 💡 Feature requests welcome via GitHub Issues
- 📧 Contact maintainers for questions

## 🙏 Acknowledgments

- [Apache Iceberg](https://iceberg.apache.org/) - Table format
- [Project Nessie](https://projectnessie.org/) - Catalog and versioning
- [MinIO](https://min.io/) - S3-compatible storage
- [PyIceberg](https://py.iceberg.apache.org/) - Python integration
- [Flask](https://flask.palletsprojects.com/) - Web framework
