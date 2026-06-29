# Patient Health Database Setup Guide

## Overview
This guide explains how to export patient data from CSV to MySQL database and read it back.

## Prerequisites

1. **MySQL Server** - Must be installed and running
   ```bash
   # macOS (using Homebrew)
   brew install mysql
   brew services start mysql

   # Ubuntu/Debian
   sudo apt-get install mysql-server
   sudo systemctl start mysql

   # Windows
   # Download from https://dev.mysql.com/downloads/mysql/
   ```

2. **Python Dependencies**
   ```bash
   pip install pandas mysql-connector-python
   ```

## Setup Instructions

### Step 1: Verify MySQL Connection
```bash
mysql -u root -p
# Or if no password
mysql -u root
```

### Step 2: Update Database Credentials
Edit both Python scripts and update the connection parameters:

**In `export_to_database.py` and `read_from_database.py`:**
```python
db_manager = PatientDatabaseManager(
    host='localhost',      # Your MySQL host
    user='root',           # Your MySQL username
    password='',           # Your MySQL password (empty if none)
    database='patient_health'  # Database name
)
```

### Step 3: Export CSV Data to Database
Run the export script to create the database, table, and import data:

```bash
python export_to_database.py
```

This will:
- Create `patient_health` database (if not exists)
- Create `sampledata` table with the following schema:
  - `id` (Primary Key, Auto-increment)
  - `PatientID` (Unique identifier from CSV)
  - `name` (Patient name)
  - `age` (Patient age)
  - `gender` (Male/Female)
  - `BMI` (Body Mass Index)
  - `Blood_pressure` (Format: systolic/diastolic)
  - `Glucose_level` (Fasting glucose level)
  - `created_at` (Timestamp)

### Step 4: Read Data from Database
After export, you can read the data using:

```bash
python read_from_database.py
```

This script provides multiple functions:
- **Read all patients** - Retrieves all records
- **Read specific patient** - Find by PatientID
- **Read as DataFrame** - Convert to pandas DataFrame
- **Get statistics** - Gender distribution and health metrics
- **Search patients** - Filter by multiple criteria
- **Export to CSV** - Save database data back to CSV

## Database Schema

```sql
CREATE TABLE sampledata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    PatientID VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    BMI FLOAT NOT NULL,
    Blood_pressure VARCHAR(20) NOT NULL,
    Glucose_level INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage Examples

### Using export_to_database.py
```python
from export_to_database import PatientDatabaseManager

db = PatientDatabaseManager(host='localhost', user='root', password='', database='patient_health')
db.connect()
db.create_database()
db.create_table()
db.export_csv_to_database('sample_paitents.csv')

# Read all data
data = db.read_all_data()
print(data)

db.close_connection()
```

### Using read_from_database.py
```python
from read_from_database import PatientDataReader

reader = PatientDataReader(host='localhost', user='root', password='', database='patient_health')
reader.connect()

# Get all patients
all_patients = reader.read_all_patients()

# Get specific patient
patient = reader.read_patient_by_id('P001')

# Get as DataFrame
df = reader.read_patients_as_dataframe()

# Search with criteria
males = reader.search_patients(gender='Male')
young_patients = reader.search_patients(age_max=40)
overweight = reader.search_patients(bmi_min=25, bmi_max=29.9)

# Get statistics
stats = reader.get_statistics()

# Export to CSV
reader.export_to_csv('patient_data_from_db.csv')

reader.close_connection()
```

## MySQL MCP Server Integration

The MySQL MCP server is configured in `.mcp.json` and enabled in `.claude/settings.json`.

To use it:
1. Install the package: `npm install @modelcontextprotocol/server-mysql`
2. Update `.mcp.json` with your MySQL credentials
3. Restart Claude Code or reload settings with `/hooks`

Then in Claude Code, you can query the database using the MCP tools.

## Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"
- Check MySQL is running: `mysql -u root -p`
- Update password in scripts if it's not empty
- Reset MySQL password if needed

### Error: "Unknown database 'patient_health'"
- Run `export_to_database.py` first to create database
- Or manually create: `CREATE DATABASE patient_health;`

### Error: "Table 'sampledata' doesn't exist"
- Run `export_to_database.py` to create table
- Or manually run the SQL schema provided above

### Data not inserting into database
- Verify CSV file path is correct
- Check CSV column names match schema (case-sensitive)
- Verify data types (age and glucose should be numeric, etc.)

## File Listings

- `export_to_database.py` - Script to export CSV to MySQL
- `read_from_database.py` - Script to read from MySQL
- `.mcp.json` - MCP server configuration
- `.claude/settings.json` - Claude Code settings with MCP enabled
- `sample_paitents.csv` - Source patient data

## Next Steps

1. Set up MySQL server if not already installed
2. Update credentials in Python scripts
3. Run `python export_to_database.py` to load data
4. Use `read_from_database.py` to query and analyze data
5. Configure MySQL MCP server for Claude Code integration
