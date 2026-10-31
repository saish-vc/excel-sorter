# SheetSort - Deployment Guide

## Local Windows Installation

### Prerequisites
- Windows 10 or later
- Python 3.11+ installed
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```powershell
   git clone <repository-url>
   cd sheetSort
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Generate sample data (optional but recommended for testing)**
   ```powershell
   python generate_sample_data.py
   ```

4. **Run the application**
   ```powershell
   streamlit run app\main.py
   ```

5. **Access the app**
   Open your browser and navigate to `http://localhost:8501`

### Troubleshooting Windows
- **Permission errors**: Run PowerShell/Git Bash as Administrator
- **Port already in use**: Change the port in `app/utils/config.py` or use `streamlit run --server.port 8502 app\main.py`
- **Module not found**: Ensure Python PATH includes the Scripts folder

---

## College Server Installation

### Prerequisites
- Windows Server or Linux server
- Python 3.11+ installed
- Minimum 4GB RAM recommended for processing 50K-row files
- 100MB disk space for database and temporary files

### Installation Steps

1. **Transfer the project files** to the college server
   ```bash
   scp -r sheetsort/ user@college-server:/opt/sheetsort/
   ```

2. **Install dependencies on the server**
   ```bash
   cd /opt/sheetsort
   pip install -r requirements.txt
   ```

3. **Create data directory** (for sample files and exports)
   ```bash
   mkdir -p data sample_data
   ```

4. **Set up environment variables**
   Create a `.env` file:
   ```
   SHEETSORT_LOG_LEVEL=INFO
   SHEETSORT_RECIPE_DB=recipes.db
   ```

5. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

6. **For production use, consider**:
   - Running behind a reverse proxy (nginx, Apache)
   - Using a process manager (systemd, PM2) to keep the app running
   - Setting up HTTPS via a reverse proxy

### Docker Deployment (Recommended for College Servers)

#### Build the Image
```bash
docker build -t sheetsort .
```

#### Run the Container
```bash
docker run -p 8501:8501 \
  -v $(pwd)/data:/home/appuser/data \
  -v $(pwd)/sample_data:/home/appuser/sample_data \
  -e SHEETSORT_LOG_LEVEL=INFO \
  sheetsort
```

#### Access the App
Open your browser to `http://localhost:8501` or access via the server's IP address.

### Docker Compose (Production Setup)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  sheetsort:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/home/appuser/data
      - ./sample_data:/home/appuser/sample_data
      - ./logs:/home/appuser/logs
    environment:
      - SHEETSORT_LOG_LEVEL=INFO
    restart: unless-stopped
```

Start with:
```bash
docker-compose up -d
```

Stop with:
```bash
docker-compose down
```

---

## Environment Variable Configuration

Copy `.env.example` to `.env` and adjust as needed:

```bash
copy .env.example .env
```

### Available Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SHEETSORT_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `SHEETSORT_RECIPE_DB` | `recipes.db` | Path to SQLite database for recipe storage |
| `SHEETSORT_MAX_UPLOAD_ROWS` | `100000` | Maximum rows per upload (safety limit) |
| `SHEETSORT_MAX_UPLOAD_SIZE_MB` | `50` | Maximum upload size in MB |

### Sample .env File
```env
# SheetSort Configuration
SHEETSORT_LOG_LEVEL=INFO
SHEETSORT_RECIPE_DB=recipes.db
SHEETSORT_MAX_UPLOAD_ROWS=100000
SHEETSORT_MAX_UPLOAD_SIZE_MB=50
```

---

## Backup and Restore Instructions

### Backup the Application

1. **Recipes and Audit Log** (SQLite database)
   ```bash
   # If using default recipes.db
   copy recipes.db backup_recipes_$(date +%Y%m%d).db
   
   # Or if using custom path from .env
   copy %SHEETSORT_RECIPE_DB% backup_recipes_$(date +%Y%m%d).db
   ```

2. **Sample Data**
   ```bash
   copy sample_data\*.xlsx backup_samples_%DATE%.xlsx
   copy sample_data\*.csv backup_samples_%DATE%.csv
   ```

3. **Logs (if enabled)**
   ```bash
   xcopy logs\*.log backup_logs_%DATE%.log
   ```

### Restore the Application

1. **Stop the application** if running
2. **Restore the recipes database**
   ```bash
   copy backup_recipes_20240101.db recipes.db
   ```
3. **Restore sample data**
   ```bash
   copy backup_samples_20240101.xlsx sample_data\
   copy backup_samples_20240101.csv sample_data\
   ```
4. **Start the application**
   ```bash
   streamlit run app\main.py
   ```

### Automatic Backup (Recommended)

Set up a Windows Task Scheduler cron job to automatically backup the recipes database daily:
- **Action**: `cmd /c copy recipes.db backup_recipes_%DATE%.db`
- **Trigger**: Daily at 23:00