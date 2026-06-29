# Patient Health Analyzer - Streamlit Web Application

A modern, interactive web dashboard for analyzing patient health data and risk categorization. Built with Streamlit, leveraging the core business logic from the console application while providing a professional user interface.

## 🌟 Features

- **📁 Data Upload**: Upload patient health data from CSV files
- **📊 Interactive Dashboard**: View health metrics and statistics
- **📈 Advanced Visualizations**: Multiple chart types for analysis
- **💾 Data Export**: Download analysis results in CSV or Excel format
- **✅ Input Validation**: Comprehensive error handling and user feedback
- **🔍 Filtering & Sorting**: Filter patients by health status and metrics

## 🏗️ Project Structure

```
Patient_health_analyser/
├── streamlit_app.py              # Main application entry point
├── requirements_web.txt           # Python dependencies
│
├── pages/                         # Multi-page Streamlit structure
│   ├── 01_upload.py              # File upload and data processing
│   ├── 02_analysis.py            # Detailed analysis and metrics
│   └── 03_visualize.py           # Charts and visualizations
│
├── read_patients_web.py          # Web-compatible wrapper functions
├── web_utils.py                  # Utility functions for UI
│
├── # Business logic (from console app)
├── read_patients.py              # Core categorization logic
├── models.py                     # Data models (Patient, HealthStatus)
├── constants.py                  # Configuration constants
├── exceptions.py                 # Custom exception types
├── logging_config.py             # Logging setup
│
├── .streamlit/
│   └── config.toml              # Streamlit configuration
│
└── test_read_patients.py         # Unit tests (unchanged)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Patient_health_analyser
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements_web.txt
   ```

### Running the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload Data

- Navigate to the **Upload Data** page
- Click "Choose a CSV file" to select your patient data
- The application will validate the file and display a preview
- Click **"Process Patient Data"** to categorize health status

**Required CSV Columns:**
- `Paitentid`: Unique patient identifier
- `name`: Patient name
- `BMI`: Body Mass Index (numeric)
- `Blood_pressure`: In format "systolic/diastolic" (e.g., "130/85")
- `Glucose_level`: Glucose level in mg/dL (numeric)

**Example CSV:**
```
Paitentid,name,BMI,Blood_pressure,Glucose_level
P001,John Smith,26.5,130/85,105
P002,Jane Doe,23.2,118/76,92
P003,Bob Wilson,29.8,145/92,148
```

### 2. Analysis

- View overall statistics (total patients, average BMI, average glucose)
- See health status distribution (Healthy, At Risk, Critical)
- Browse detailed patient table with color-coded health status
- Use sidebar filters to narrow down by status or metrics
- Export filtered data to CSV or Excel

### 3. Visualizations

- **Distribution**: Bar chart of patient health status distribution
- **BMI Analysis**: Histogram and box plots of BMI data
- **Glucose Analysis**: Histogram and distribution by health status
- **Blood Pressure**: Summary by health status

## ⚙️ Configuration

### Modifying Health Thresholds

Edit `constants.py` to adjust health categorization thresholds:

```python
# Health Status Thresholds
BMI_CRITICAL_THRESHOLD = 30          # BMI >= 30 is Critical
BMI_AT_RISK_THRESHOLD = 25           # BMI >= 25 is At Risk

BP_CRITICAL_SYSTOLIC = 180           # Systolic >= 180 is Critical
BP_CRITICAL_DIASTOLIC = 120          # Diastolic >= 120 is Critical
BP_AT_RISK_SYSTOLIC = 130            # Systolic >= 130 is At Risk
BP_AT_RISK_DIASTOLIC = 80            # Diastolic >= 80 is At Risk

GLUCOSE_CRITICAL_THRESHOLD = 126     # Glucose >= 126 is Critical
GLUCOSE_AT_RISK_THRESHOLD = 100      # Glucose >= 100 is At Risk
```

### Customizing Colors

Edit color mappings in `constants.py`:

```python
HEALTH_STATUS_COLORS = {
    "Healthy": "#2ecc71",    # Green
    "AtRisk": "#f39c12",     # Orange
    "Critical": "#e74c3c",   # Red
}
```

### Streamlit Settings

Edit `.streamlit/config.toml` for application appearance and behavior.

## 🧪 Testing

Run the existing test suite to verify business logic:

```bash
pytest test_read_patients.py -v
```

All 33 existing tests should pass. The web interface does not modify business logic.

## 🛠️ Architecture

### Separation of Concerns

**Business Logic** (Unchanged from console app):
- `read_patients.py`: Health categorization functions
- `models.py`: Patient dataclass and HealthStatus enum
- `constants.py`: Configuration thresholds
- `exceptions.py`: Custom exception hierarchy

**Web Layer** (New for Streamlit):
- `streamlit_app.py`: Main entry point and navigation
- `pages/`: Multi-page UI components
- `read_patients_web.py`: Web-compatible wrappers
- `web_utils.py`: UI utility functions

### Data Flow

```
CSV Upload → Validation → Process (add_health_category) → Store in session
                                                              ↓
                                            ┌─────────────────┼─────────────────┐
                                            ↓                 ↓                 ↓
                                      Analysis Page    Visualize Page      Export
```

## 📊 Health Status Categories

The application categorizes patients into three health status groups:

- **🟢 Healthy**: All metrics within normal range
- **🟡 At Risk**: One or more metrics in elevated range
- **🔴 Critical**: One or more metrics in critical range

Categorization is based on composite evaluation of:
- Body Mass Index (BMI)
- Blood Pressure
- Glucose Level

## 🔐 Error Handling

The application provides comprehensive error handling:

- **File Upload Errors**: Invalid CSV format, missing columns
- **Data Validation Errors**: Missing required fields, invalid data types
- **Processing Errors**: Blood pressure format issues, invalid metrics
- **Visualization Errors**: Chart generation failures

All errors display user-friendly messages with guidance for correction.

## 📈 Performance

- Optimized for datasets up to 10,000 patients
- Lazy loading of visualizations
- Cached computations where possible
- Responsive UI with Streamlit's reactive programming model

## 🐛 Troubleshooting

### "No file uploaded" message
**Solution**: Upload a CSV file on the Upload Data page first

### "Missing required columns" error
**Solution**: Ensure your CSV has all required columns (Paitentid, name, BMI, Blood_pressure, Glucose_level)

### "Invalid blood pressure format" error
**Solution**: Blood pressure must be in "systolic/diastolic" format (e.g., "130/85")

### Port already in use (8501)
**Solution**: Change port with `streamlit run streamlit_app.py --server.port 8502`

### Performance issues with large files
**Solution**: Upload files with fewer than 10,000 rows for optimal performance

## 🔄 Relationship with Console App

This Streamlit application **reuses 100% of the business logic** from the console application:

- ✅ Same health categorization algorithm
- ✅ Same thresholds and constants
- ✅ Same exception handling
- ✅ Same data models
- ✅ All existing tests pass unchanged

**What changed:**
- ❌ Removed: Console I/O and file operations
- ✅ Added: Streamlit UI components
- ✅ Added: Form-based input and validation
- ✅ Added: Interactive visualizations
- ✅ Added: Data export functionality

## 📝 Sample CSV Format

Download or use this sample CSV structure:

```csv
Paitentid,name,age,gender,BMI,Blood_pressure,Glucose_level
P001,John Smith,45,Male,26.5,130/85,105
P002,Sarah Johnson,38,Female,23.2,118/76,92
P003,Michael Brown,52,Male,29.8,145/92,148
P004,Emily Davis,41,Female,24.1,120/78,98
P005,Robert Wilson,58,Male,31.5,155/98,165
```

## 🎯 Key Improvements Over Console App

1. **User Interface**: Interactive web dashboard vs. text console
2. **Data Exploration**: Filters, sorting, and visualizations
3. **Real-time Feedback**: Immediate validation and error messages
4. **Export Options**: CSV and Excel export capabilities
5. **Responsive Design**: Multi-page layout adapts to window size
6. **Accessibility**: Sidebar navigation and intuitive controls

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_app.py
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements_web.txt .
RUN pip install -r requirements_web.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Cloud Deployment
- **Streamlit Cloud**: Connect GitHub repo, auto-deploys on push
- **Heroku**: Use Streamlit Heroku buildpack
- **AWS/Azure**: Deploy Docker container to container service

## 📞 Support

For issues or questions:
1. Check the Help section in the sidebar
2. Review error messages for guidance
3. Verify CSV format matches requirements
4. Run unit tests to verify business logic

## 📄 License

Same license as the original Patient Health Analyzer console application.

## 🙏 Credits

Built on the modernized Patient Health Analyzer console application with professional Python best practices including type hints, custom exceptions, dataclasses, and comprehensive logging.

