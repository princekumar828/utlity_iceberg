# 📋 Quick Start Checklist

## ✅ Before You Begin
- [ ] Nessie catalog is running and accessible
- [ ] MinIO/S3 storage is running and accessible  
- [ ] You have valid credentials for your storage
- [ ] Python 3.8+ is installed

## 🚀 Setup (5 minutes)

### 1. Environment Setup
```bash
cd /path/to/utlity
./setup.sh
```

### 2. Configure Connection
```bash
./quick_setup.sh
# Choose option 1 (environment variables) or 2 (config file)
# Enter your lakehouse connection details
```

### 3. Verify Setup
The script will automatically test your connection. Look for:
```
✅ Connected to lakehouse successfully!
✅ Found X namespace(s)
```

## 🎯 Start Exploring

### Web Interface (Easiest)
```bash
./start_web.sh
# Open: http://localhost:5000
```

### Command Line
```bash
source venv/bin/activate
source .env  # if using environment variables
python main.py interactive
```

## 📊 Common Commands

| Task | Command |
|------|---------|
| See all tables | `python main.py overview` |
| Interactive mode | `python main.py interactive` |
| Table details | `python main.py show-table namespace.table` |
| Preview data | `python main.py preview-table namespace.table` |
| Web interface | `./start_web.sh` |

## 🔧 Your Connection Details Template

Fill this out for your setup:

```
Nessie URI: http://your-nessie-host:19120/api/v1
S3 Endpoint: http://your-minio-host:9000  
S3 Access Key: your-access-key
S3 Secret Key: your-secret-key
Warehouse Path: s3://your-bucket-name/
```

## 🚨 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Check if services are running |
| Access denied | Verify credentials |
| SSL errors | Set `SSL_VERIFY=false` |
| Import errors | Run `./setup.sh` again |

**🎉 You're ready to explore your lakehouse!**
