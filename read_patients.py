import pandas as pd
import matplotlib.pyplot as plt
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('patient_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_patient_data(filepath):
    """Read CSV file and apply health categorization to every row"""
    try:
        logger.info(f"Starting data load from: {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"✓ Data loaded successfully. Total records: {len(df)}")
        logger.debug(f"Columns loaded: {list(df.columns)}")

        logger.info("Starting health categorization...")
        df['health_status'] = df.apply(
            lambda row: categorize_patient_health(
                row['BMI'],
                row['Blood_pressure'],
                row['Glucose_level']
            ),
            axis=1
        )
        logger.info("✓ Health categorization completed for all records")

        print("Patient data loaded with health status categorization:\n")
        print(df.head())
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading patient data: {str(e)}")
        raise

def read_patient_csv(filepath):
    """Read CSV file and print first five rows (deprecated - use load_patient_data instead)"""
    df = pd.read_csv(filepath)
    print("First 5 rows of patient data:\n")
    print(df.head())
    return df

def categorize_patient_health(bmi, blood_pressure, glucose_level):
    """
    Categorize patient health status based on BMI, Blood Pressure, and Glucose level

    Args:
        bmi (float): Body Mass Index
        blood_pressure (str): Blood pressure in format 'systolic/diastolic' (e.g., '130/85')
        glucose_level (int): Glucose level in mg/dL

    Returns:
        str: Health category - 'Healthy', 'AtRisk', or 'Critical'
    """
    critical_count = 0
    at_risk_count = 0

    # Parse blood pressure
    try:
        systolic, diastolic = map(int, blood_pressure.split('/'))
    except:
        logger.warning(f"Invalid blood pressure format: {blood_pressure}")
        return "Invalid blood pressure format"

    # Check BMI
    if bmi >= 30:
        critical_count += 1
        logger.debug(f"BMI {bmi} marked as Critical (≥30)")
    elif bmi >= 25:
        at_risk_count += 1
        logger.debug(f"BMI {bmi} marked as AtRisk (25-29.9)")

    # Check Blood Pressure
    if systolic >= 180 or diastolic >= 120:
        critical_count += 1
        logger.debug(f"BP {blood_pressure} marked as Critical (≥180/120)")
    elif systolic >= 130 or diastolic >= 80:
        at_risk_count += 1
        logger.debug(f"BP {blood_pressure} marked as AtRisk (130-179/80-119)")

    # Check Glucose Level
    if glucose_level >= 126:
        critical_count += 1
        logger.debug(f"Glucose {glucose_level} marked as Critical (≥126)")
    elif glucose_level >= 100:
        at_risk_count += 1
        logger.debug(f"Glucose {glucose_level} marked as AtRisk (100-125)")

    # Determine category
    if critical_count > 0:
        return "Critical"
    elif at_risk_count > 0:
        return "AtRisk"
    else:
        return "Healthy"

def add_health_category(df):
    """Add health category column to dataframe"""
    df['Health_Status'] = df.apply(
        lambda row: categorize_patient_health(
            row['BMI'],
            row['Blood_pressure'],
            row['Glucose_level']
        ),
        axis=1
    )
    return df

def plot_health_status_distribution(df):
    """Create a bar chart showing count of patients by health status"""
    try:
        logger.info("Starting visualization generation...")
        health_counts = df['health_status'].value_counts()
        logger.info(f"Health status distribution: {health_counts.to_dict()}")

        plt.figure(figsize=(10, 6))
        colors = {'Healthy': '#2ecc71', 'AtRisk': '#f39c12', 'Critical': '#e74c3c'}
        bar_colors = [colors.get(status, '#95a5a6') for status in health_counts.index]

        bars = plt.bar(health_counts.index, health_counts.values, color=bar_colors, edgecolor='black', linewidth=1.5)

        plt.xlabel('Health Status', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Patients', fontsize=12, fontweight='bold')
        plt.title('Patient Distribution by Health Status', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3, linestyle='--')

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

        plt.tight_layout()
        plt.savefig('health_status_distribution.png', dpi=300, bbox_inches='tight')
        logger.info("✓ Chart saved as 'health_status_distribution.png'")
        print("Chart saved as 'health_status_distribution.png'")
        plt.show()
    except Exception as e:
        logger.error(f"Error generating visualization: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("="*80)
    logger.info("Patient Health Analyzer - Starting execution")
    logger.info("="*80)

    try:
        df = load_patient_data("sample_paitents.csv")

        logger.info("Generating summary report...")
        print("\n" + "="*80)
        print("Detailed Patient Health Status:\n")
        print(df[['Paitentid', 'name', 'BMI', 'Blood_pressure', 'Glucose_level', 'health_status']])

        print("\n" + "="*80)
        print("Health Status Summary:")
        summary = df['health_status'].value_counts()
        print(summary)
        logger.info(f"Summary generated: {summary.to_dict()}")

        healthy_count = summary.get('Healthy', 0)
        atrisk_count = summary.get('AtRisk', 0)
        critical_count = summary.get('Critical', 0)

        logger.info(f"Healthy patients: {healthy_count}")
        logger.info(f"At-Risk patients: {atrisk_count}")
        logger.info(f"Critical patients: {critical_count}")

        print("\n" + "="*80)
        print("All Columns:")
        print(df)

        print("\n" + "="*80)
        print("Generating health status distribution chart...")
        plot_health_status_distribution(df)

        logger.info("="*80)
        logger.info("Patient Health Analyzer - Execution completed successfully")
        logger.info("="*80)

    except Exception as e:
        logger.error(f"Patient Health Analyzer - Execution failed: {str(e)}")
        logger.error("="*80)
        raise
