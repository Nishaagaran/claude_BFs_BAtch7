"""Configuration constants for Patient Health Analyzer."""

# Health status thresholds
BMI_CRITICAL_THRESHOLD = 30
BMI_AT_RISK_THRESHOLD = 25

BP_CRITICAL_SYSTOLIC = 180
BP_CRITICAL_DIASTOLIC = 120
BP_AT_RISK_SYSTOLIC = 130
BP_AT_RISK_DIASTOLIC = 80

GLUCOSE_CRITICAL_THRESHOLD = 126
GLUCOSE_AT_RISK_THRESHOLD = 100

# Status category constants
STATUS_HEALTHY = "Healthy"
STATUS_AT_RISK = "AtRisk"
STATUS_CRITICAL = "Critical"

# Visualization constants
HEALTH_STATUS_COLORS = {
    STATUS_HEALTHY: '#2ecc71',
    STATUS_AT_RISK: '#f39c12',
    STATUS_CRITICAL: '#e74c3c'
}

# Chart styling
CHART_FIGURE_SIZE = (10, 6)
CHART_DPI = 300
CHART_OUTPUT_FILE = 'health_status_distribution.png'

# CSV column names
CSV_PATIENT_ID_COLUMN = 'Paitentid'
CSV_NAME_COLUMN = 'name'
CSV_BMI_COLUMN = 'BMI'
CSV_BLOOD_PRESSURE_COLUMN = 'Blood_pressure'
CSV_GLUCOSE_COLUMN = 'Glucose_level'
CSV_HEALTH_STATUS_COLUMN = 'health_status'

# Default file
DEFAULT_CSV_FILE = 'sample_paitents.csv'

# Logging
LOG_FILE = 'patient_analyzer.log'
