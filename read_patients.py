"""Patient Health Analyzer - Load, categorize, and visualize patient health data."""

import pandas as pd
import matplotlib.pyplot as plt
import logging
from constants import (
    BMI_CRITICAL_THRESHOLD, BMI_AT_RISK_THRESHOLD,
    BP_CRITICAL_SYSTOLIC, BP_CRITICAL_DIASTOLIC,
    BP_AT_RISK_SYSTOLIC, BP_AT_RISK_DIASTOLIC,
    GLUCOSE_CRITICAL_THRESHOLD, GLUCOSE_AT_RISK_THRESHOLD,
    STATUS_HEALTHY, STATUS_AT_RISK, STATUS_CRITICAL,
    HEALTH_STATUS_COLORS, CHART_FIGURE_SIZE, CHART_DPI,
    CHART_OUTPUT_FILE, CSV_PATIENT_ID_COLUMN, CSV_NAME_COLUMN,
    CSV_BMI_COLUMN, CSV_BLOOD_PRESSURE_COLUMN, CSV_GLUCOSE_COLUMN,
    CSV_HEALTH_STATUS_COLUMN, DEFAULT_CSV_FILE, LOG_FILE
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def _load_csv(filepath):
    """Load and return CSV data.

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with CSV data

    Raises:
        FileNotFoundError: If file not found
        Exception: If file cannot be read as CSV
    """
    try:
        logger.info(f"Starting data load from: {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Data loaded successfully. Total records: {len(df)}")
        logger.debug(f"Columns loaded: {list(df.columns)}")
        return df
    except FileNotFoundError as e:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}")
        raise


def _parse_blood_pressure(blood_pressure):
    """Parse blood pressure string into systolic and diastolic values.

    Args:
        blood_pressure: String in format 'systolic/diastolic' (e.g., '130/85')

    Returns:
        Tuple of (systolic, diastolic) as integers

    Raises:
        ValueError: If format is invalid
    """
    try:
        systolic, diastolic = map(int, blood_pressure.split('/'))
        return systolic, diastolic
    except ValueError:
        logger.warning(f"Invalid blood pressure format: {blood_pressure}")
        raise


def _evaluate_bmi(bmi):
    """Evaluate BMI and return health status level.

    Args:
        bmi: Body Mass Index value

    Returns:
        Status level: STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if bmi >= BMI_CRITICAL_THRESHOLD:
        return STATUS_CRITICAL
    elif bmi >= BMI_AT_RISK_THRESHOLD:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def _evaluate_blood_pressure(systolic, diastolic):
    """Evaluate blood pressure and return health status level.

    Args:
        systolic: Systolic blood pressure
        diastolic: Diastolic blood pressure

    Returns:
        Status level: STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if systolic >= BP_CRITICAL_SYSTOLIC or diastolic >= BP_CRITICAL_DIASTOLIC:
        return STATUS_CRITICAL
    elif systolic >= BP_AT_RISK_SYSTOLIC or diastolic >= BP_AT_RISK_DIASTOLIC:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def _evaluate_glucose(glucose_level):
    """Evaluate glucose level and return health status level.

    Args:
        glucose_level: Glucose level in mg/dL

    Returns:
        Status level: STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if glucose_level >= GLUCOSE_CRITICAL_THRESHOLD:
        return STATUS_CRITICAL
    elif glucose_level >= GLUCOSE_AT_RISK_THRESHOLD:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def _determine_overall_category(metric_statuses):
    """Determine overall health category from individual metric statuses.

    Args:
        metric_statuses: List of status strings from individual metrics

    Returns:
        Overall status: STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if STATUS_CRITICAL in metric_statuses:
        return STATUS_CRITICAL
    elif STATUS_AT_RISK in metric_statuses:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def categorize_patient_health(bmi, blood_pressure, glucose_level):
    """Categorize patient health status based on BMI, BP, and glucose level.

    Args:
        bmi: Body Mass Index
        blood_pressure: Blood pressure string in format 'systolic/diastolic'
        glucose_level: Glucose level in mg/dL

    Returns:
        Health category: 'Healthy', 'AtRisk', or 'Critical'
    """
    try:
        systolic, diastolic = _parse_blood_pressure(blood_pressure)
    except ValueError:
        return "Invalid blood pressure format"

    bmi_status = _evaluate_bmi(bmi)
    bp_status = _evaluate_blood_pressure(systolic, diastolic)
    glucose_status = _evaluate_glucose(glucose_level)

    return _determine_overall_category([bmi_status, bp_status, glucose_status])


def _add_health_categorization(df, column_name=CSV_HEALTH_STATUS_COLUMN):
    """Apply health categorization to DataFrame.

    Args:
        df: DataFrame with patient data
        column_name: Name of column to store results (default: 'health_status')

    Returns:
        DataFrame with health_status column added
    """
    logger.info("Starting health categorization...")
    df[column_name] = df.apply(
        lambda row: categorize_patient_health(
            row[CSV_BMI_COLUMN],
            row[CSV_BLOOD_PRESSURE_COLUMN],
            row[CSV_GLUCOSE_COLUMN]
        ),
        axis=1
    )
    logger.info("Health categorization completed for all records")
    return df


def _display_loaded_data(df):
    """Display loaded patient data to console.

    Args:
        df: DataFrame with patient data
    """
    print("Patient data loaded with health status categorization:\n")
    print(df.head())


def load_patient_data(filepath):
    """Load patient data, categorize health status, and display results.

    Args:
        filepath: Path to patient CSV file

    Returns:
        DataFrame with patient data and health_status column
    """
    df = _load_csv(filepath)
    df = _add_health_categorization(df)
    _display_loaded_data(df)
    return df


def add_health_category(df):
    """Add health category column to dataframe.

    Args:
        df: DataFrame with patient data

    Returns:
        DataFrame with health_status column added
    """
    return _add_health_categorization(df)


def _get_chart_colors(health_statuses):
    """Get colors for health statuses, defaulting to gray for unknown statuses.

    Args:
        health_statuses: Index of health status values

    Returns:
        List of color codes
    """
    return [HEALTH_STATUS_COLORS.get(status, '#95a5a6') for status in health_statuses]


def _add_bar_labels(bars):
    """Add value labels on top of bar chart bars.

    Args:
        bars: Bar container from matplotlib bar chart
    """
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=11, fontweight='bold'
        )


def _configure_chart_appearance():
    """Configure chart labels, title, and grid."""
    plt.xlabel('Health Status', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Patients', fontsize=12, fontweight='bold')
    plt.title('Patient Distribution by Health Status', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')


def plot_health_status_distribution(df):
    """Create and save bar chart showing patient distribution by health status.

    Args:
        df: DataFrame with patient data including health_status column
    """
    try:
        logger.info("Starting visualization generation...")
        health_counts = df[CSV_HEALTH_STATUS_COLUMN].value_counts()
        logger.info(f"Health status distribution: {health_counts.to_dict()}")

        plt.figure(figsize=CHART_FIGURE_SIZE)
        bar_colors = _get_chart_colors(health_counts.index)

        bars = plt.bar(
            health_counts.index, health_counts.values,
            color=bar_colors, edgecolor='black', linewidth=1.5
        )

        _configure_chart_appearance()
        _add_bar_labels(bars)

        plt.tight_layout()
        plt.savefig(CHART_OUTPUT_FILE, dpi=CHART_DPI, bbox_inches='tight')
        logger.info(f"Chart saved as '{CHART_OUTPUT_FILE}'")
        print(f"Chart saved as '{CHART_OUTPUT_FILE}'")
        plt.show()
    except Exception as e:
        logger.error(f"Error generating visualization: {str(e)}")
        raise


def _display_summary_report(df):
    """Display detailed patient health status summary.

    Args:
        df: DataFrame with patient data
    """
    print("\n" + "="*80)
    print("Detailed Patient Health Status:\n")
    print(df[[
        CSV_PATIENT_ID_COLUMN, CSV_NAME_COLUMN, CSV_BMI_COLUMN,
        CSV_BLOOD_PRESSURE_COLUMN, CSV_GLUCOSE_COLUMN, CSV_HEALTH_STATUS_COLUMN
    ]])


def _display_health_summary(df):
    """Display and log health status summary statistics.

    Args:
        df: DataFrame with patient data
    """
    print("\n" + "="*80)
    print("Health Status Summary:")
    summary = df[CSV_HEALTH_STATUS_COLUMN].value_counts()
    print(summary)
    logger.info(f"Summary generated: {summary.to_dict()}")

    healthy_count = summary.get(STATUS_HEALTHY, 0)
    atrisk_count = summary.get(STATUS_AT_RISK, 0)
    critical_count = summary.get(STATUS_CRITICAL, 0)

    logger.info(f"Healthy patients: {healthy_count}")
    logger.info(f"At-Risk patients: {atrisk_count}")
    logger.info(f"Critical patients: {critical_count}")


def _display_all_data(df):
    """Display all patient data columns.

    Args:
        df: DataFrame with patient data
    """
    print("\n" + "="*80)
    print("All Columns:")
    print(df)


if __name__ == "__main__":
    logger.info("="*80)
    logger.info("Patient Health Analyzer - Starting execution")
    logger.info("="*80)

    try:
        df = load_patient_data(DEFAULT_CSV_FILE)

        logger.info("Generating summary report...")
        _display_summary_report(df)
        _display_health_summary(df)
        _display_all_data(df)

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
