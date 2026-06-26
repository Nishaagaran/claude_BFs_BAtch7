"""Patient Health Analyzer - Load, categorize, and visualize patient health data.

This module provides functionality to:
- Load patient health data from CSV files
- Categorize patients into health status categories (Healthy, At-Risk, Critical)
- Generate visualizations of health status distribution

All functions include comprehensive type hints and follow Python best practices
for exception handling and logging.
"""

from typing import Tuple, List, Any

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
    CSV_HEALTH_STATUS_COLUMN, DEFAULT_CSV_FILE, LOG_FILE,
    REPORT_BORDER, CHART_XLABEL_SIZE, CHART_YLABEL_SIZE,
    CHART_TITLE_SIZE, CHART_LABEL_SIZE, CHART_FONT_WEIGHT,
    CHART_GRID_ALPHA, CHART_GRID_LINESTYLE, CHART_BAR_EDGE_COLOR,
    CHART_BAR_EDGE_WIDTH,
)
from exceptions import (
    PatientHealthAnalyzerError,
    BloodPressureFormatError,
    PatientDataError,
    DataLoadError,
    VisualizationError,
)
from logging_config import setup_logger

logger: logging.Logger = setup_logger(__name__, LOG_FILE)


def _load_csv(filepath: str) -> pd.DataFrame:
    """Load and return CSV data from file.

    Args:
        filepath (str): Path to CSV file

    Returns:
        pd.DataFrame: DataFrame containing CSV data

    Raises:
        DataLoadError: If file not found or cannot be read as CSV
    """
    try:
        logger.info(f"Starting data load from: {filepath}")
        df: pd.DataFrame = pd.read_csv(filepath)
        logger.info(f"Data loaded successfully. Total records: {len(df)}")
        logger.debug(f"Columns loaded: {list(df.columns)}")
        return df
    except FileNotFoundError as e:
        logger.error(f"File not found: {filepath}")
        raise DataLoadError(f"Cannot load data: file not found at {filepath}") from e
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}", exc_info=True)
        raise DataLoadError(f"Cannot load CSV file: {str(e)}") from e


def _parse_blood_pressure(blood_pressure: str) -> Tuple[int, int]:
    """Parse blood pressure string into systolic and diastolic values.

    Args:
        blood_pressure (str): String in format 'systolic/diastolic'
                             (e.g., '130/85')

    Returns:
        Tuple[int, int]: Tuple of (systolic, diastolic) as integers

    Raises:
        BloodPressureFormatError: If format is invalid or cannot be parsed
    """
    try:
        systolic_str, diastolic_str = blood_pressure.split("/")
        systolic: int = int(systolic_str)
        diastolic: int = int(diastolic_str)
        return systolic, diastolic
    except ValueError as e:
        logger.warning(f"Invalid blood pressure format: {blood_pressure}")
        raise BloodPressureFormatError(
            f"Blood pressure must be in format 'systolic/diastolic', "
            f"got: {blood_pressure}"
        ) from e


def _evaluate_bmi(bmi: float) -> str:
    """Evaluate BMI and return health status level.

    Args:
        bmi (float): Body Mass Index value

    Returns:
        str: Status level - STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if bmi >= BMI_CRITICAL_THRESHOLD:
        return STATUS_CRITICAL
    elif bmi >= BMI_AT_RISK_THRESHOLD:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def _evaluate_blood_pressure(systolic: int, diastolic: int) -> str:
    """Evaluate blood pressure and return health status level.

    Args:
        systolic (int): Systolic blood pressure value
        diastolic (int): Diastolic blood pressure value

    Returns:
        str: Status level - STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if systolic >= BP_CRITICAL_SYSTOLIC or diastolic >= BP_CRITICAL_DIASTOLIC:
        return STATUS_CRITICAL
    elif systolic >= BP_AT_RISK_SYSTOLIC or diastolic >= BP_AT_RISK_DIASTOLIC:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def _evaluate_glucose(glucose_level: float) -> str:
    """Evaluate glucose level and return health status level.

    Args:
        glucose_level (float): Glucose level in mg/dL

    Returns:
        str: Status level - STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if glucose_level >= GLUCOSE_CRITICAL_THRESHOLD:
        return STATUS_CRITICAL
    elif glucose_level >= GLUCOSE_AT_RISK_THRESHOLD:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def _determine_overall_category(metric_statuses: List[str]) -> str:
    """Determine overall health category from individual metric statuses.

    Applies priority logic: Critical > AtRisk > Healthy
    If any metric is Critical, overall status is Critical.
    If any metric is AtRisk (and none Critical), overall status is AtRisk.
    Otherwise, overall status is Healthy.

    Args:
        metric_statuses (List[str]): List of individual metric status strings

    Returns:
        str: Overall status - STATUS_CRITICAL, STATUS_AT_RISK, or STATUS_HEALTHY
    """
    if STATUS_CRITICAL in metric_statuses:
        return STATUS_CRITICAL
    elif STATUS_AT_RISK in metric_statuses:
        return STATUS_AT_RISK
    return STATUS_HEALTHY


def categorize_patient_health(
    bmi: float, blood_pressure: str, glucose_level: float
) -> str:
    """Categorize patient health status based on BMI, BP, and glucose level.

    Combines individual metric evaluations to determine overall health category
    using priority-based aggregation (Critical > AtRisk > Healthy).

    Args:
        bmi (float): Body Mass Index
        blood_pressure (str): Blood pressure string in format 'systolic/diastolic'
        glucose_level (float): Glucose level in mg/dL

    Returns:
        str: Health category - 'Healthy', 'AtRisk', or 'Critical'

    Raises:
        BloodPressureFormatError: If blood pressure format is invalid
    """
    try:
        systolic, diastolic = _parse_blood_pressure(blood_pressure)
    except BloodPressureFormatError:
        raise

    bmi_status: str = _evaluate_bmi(bmi)
    bp_status: str = _evaluate_blood_pressure(systolic, diastolic)
    glucose_status: str = _evaluate_glucose(glucose_level)

    return _determine_overall_category([bmi_status, bp_status, glucose_status])


def _add_health_categorization(
    df: pd.DataFrame, column_name: str = CSV_HEALTH_STATUS_COLUMN
) -> pd.DataFrame:
    """Apply health categorization to DataFrame.

    Adds a new column with health status for each patient row based on
    their BMI, blood pressure, and glucose level.

    Args:
        df (pd.DataFrame): DataFrame with patient data
        column_name (str): Name of column to store results
                          (default: 'health_status')

    Returns:
        pd.DataFrame: DataFrame with health_status column added

    Raises:
        PatientDataError: If required columns are missing from DataFrame
    """
    required_columns: List[str] = [
        CSV_BMI_COLUMN,
        CSV_BLOOD_PRESSURE_COLUMN,
        CSV_GLUCOSE_COLUMN,
    ]

    missing_columns: List[str] = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        error_msg: str = f"Required columns missing: {missing_columns}"
        logger.error(error_msg)
        raise PatientDataError(error_msg)

    logger.info("Starting health categorization...")
    try:
        df[column_name] = df.apply(
            lambda row: categorize_patient_health(
                float(row[CSV_BMI_COLUMN]),
                str(row[CSV_BLOOD_PRESSURE_COLUMN]),
                float(row[CSV_GLUCOSE_COLUMN]),
            ),
            axis=1,
        )
        logger.info("Health categorization completed for all records")
    except Exception as e:
        logger.error(f"Error during health categorization: {str(e)}", exc_info=True)
        raise PatientDataError(f"Categorization failed: {str(e)}") from e

    return df


def _display_loaded_data(df: pd.DataFrame) -> None:
    """Log loaded patient data to output.

    Args:
        df (pd.DataFrame): DataFrame with patient data
    """
    logger.info("Patient data loaded with health status categorization")
    logger.debug(f"Sample data:\n{df.head().to_string()}")


def load_patient_data(filepath: str) -> pd.DataFrame:
    """Load patient data, categorize health status, and return DataFrame.

    Main entry point for loading and processing patient CSV data.
    Handles file I/O, categorization, and logging.

    Args:
        filepath (str): Path to patient CSV file

    Returns:
        pd.DataFrame: DataFrame with patient data and health_status column

    Raises:
        DataLoadError: If file cannot be loaded
        PatientDataError: If data is malformed
    """
    df: pd.DataFrame = _load_csv(filepath)
    df = _add_health_categorization(df)
    _display_loaded_data(df)
    return df


def add_health_category(df: pd.DataFrame) -> pd.DataFrame:
    """Add health category column to dataframe.

    Convenience function for adding health status column to an existing
    DataFrame with patient data.

    Args:
        df (pd.DataFrame): DataFrame with patient data

    Returns:
        pd.DataFrame: DataFrame with health_status column added

    Raises:
        PatientDataError: If required columns are missing
    """
    return _add_health_categorization(df)


def _get_chart_colors(health_statuses: pd.Index) -> List[str]:
    """Get colors for health statuses, with gray default for unknowns.

    Maps each health status value to its corresponding color from
    the configuration. Unknown statuses default to gray.

    Args:
        health_statuses (pd.Index): Index of health status values

    Returns:
        List[str]: List of hex color codes corresponding to statuses
    """
    return [HEALTH_STATUS_COLORS.get(status, "#95a5a6") for status in health_statuses]


def _add_bar_labels(bars: Any) -> None:
    """Add value labels on top of bar chart bars.

    Displays the count value above each bar in the chart.

    Args:
        bars: Bar container from matplotlib bar chart
    """
    for bar in bars:
        height: float = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=CHART_LABEL_SIZE,
            fontweight=CHART_FONT_WEIGHT,
        )


def _configure_chart_appearance() -> None:
    """Configure chart labels, title, and grid styling."""
    plt.xlabel("Health Status", fontsize=CHART_XLABEL_SIZE, fontweight=CHART_FONT_WEIGHT)
    plt.ylabel(
        "Number of Patients", fontsize=CHART_YLABEL_SIZE, fontweight=CHART_FONT_WEIGHT
    )
    plt.title(
        "Patient Distribution by Health Status",
        fontsize=CHART_TITLE_SIZE,
        fontweight=CHART_FONT_WEIGHT,
    )
    plt.grid(axis="y", alpha=CHART_GRID_ALPHA, linestyle=CHART_GRID_LINESTYLE)


def plot_health_status_distribution(df: pd.DataFrame) -> None:
    """Create and save bar chart showing patient distribution by health status.

    Generates a bar chart with patient counts for each health status category
    and saves to a PNG file.

    Args:
        df (pd.DataFrame): DataFrame with patient data including health_status

    Raises:
        VisualizationError: If chart generation or saving fails
    """
    try:
        logger.info("Starting visualization generation...")
        health_counts: pd.Series = df[CSV_HEALTH_STATUS_COLUMN].value_counts()
        logger.info(f"Health status distribution: {health_counts.to_dict()}")

        plt.figure(figsize=CHART_FIGURE_SIZE)
        bar_colors: List[str] = _get_chart_colors(health_counts.index)

        bars: plt.Container = plt.bar(
            health_counts.index,
            health_counts.values,
            color=bar_colors,
            edgecolor=CHART_BAR_EDGE_COLOR,
            linewidth=CHART_BAR_EDGE_WIDTH,
        )

        _configure_chart_appearance()
        _add_bar_labels(bars)

        plt.tight_layout()
        plt.savefig(CHART_OUTPUT_FILE, dpi=CHART_DPI, bbox_inches="tight")
        logger.info(f"Chart saved as '{CHART_OUTPUT_FILE}'")
        plt.show()
    except Exception as e:
        logger.error(f"Error generating visualization: {str(e)}", exc_info=True)
        raise VisualizationError(f"Failed to generate chart: {str(e)}") from e


def _display_summary_report(df: pd.DataFrame) -> None:
    """Log detailed patient health status summary.

    Args:
        df (pd.DataFrame): DataFrame with patient data
    """
    logger.info(REPORT_BORDER)
    logger.info("Detailed Patient Health Status Report")
    logger.info(REPORT_BORDER)

    columns_to_display: List[str] = [
        CSV_PATIENT_ID_COLUMN,
        CSV_NAME_COLUMN,
        CSV_BMI_COLUMN,
        CSV_BLOOD_PRESSURE_COLUMN,
        CSV_GLUCOSE_COLUMN,
        CSV_HEALTH_STATUS_COLUMN,
    ]

    report_df: pd.DataFrame = df[columns_to_display]
    logger.info(f"\n{report_df.to_string()}")


def _display_health_summary(df: pd.DataFrame) -> None:
    """Log and display health status summary statistics.

    Args:
        df (pd.DataFrame): DataFrame with patient data
    """
    logger.info(REPORT_BORDER)
    logger.info("Health Status Summary")
    logger.info(REPORT_BORDER)

    summary: pd.Series = df[CSV_HEALTH_STATUS_COLUMN].value_counts()
    logger.info(f"\n{summary.to_string()}")
    logger.info(f"Summary statistics: {summary.to_dict()}")

    healthy_count: int = int(summary.get(STATUS_HEALTHY, 0))
    atrisk_count: int = int(summary.get(STATUS_AT_RISK, 0))
    critical_count: int = int(summary.get(STATUS_CRITICAL, 0))

    logger.info(f"Healthy patients: {healthy_count}")
    logger.info(f"At-Risk patients: {atrisk_count}")
    logger.info(f"Critical patients: {critical_count}")


def _display_all_data(df: pd.DataFrame) -> None:
    """Log all patient data columns.

    Args:
        df (pd.DataFrame): DataFrame with patient data
    """
    logger.info(REPORT_BORDER)
    logger.info("All Patient Data")
    logger.info(REPORT_BORDER)
    logger.info(f"\n{df.to_string()}")


if __name__ == "__main__":
    logger.info(REPORT_BORDER)
    logger.info("Patient Health Analyzer - Starting execution")
    logger.info(REPORT_BORDER)

    try:
        df: pd.DataFrame = load_patient_data(DEFAULT_CSV_FILE)

        logger.info("Generating summary report...")
        _display_summary_report(df)
        _display_health_summary(df)
        _display_all_data(df)

        logger.info(REPORT_BORDER)
        logger.info("Generating health status distribution chart...")
        logger.info(REPORT_BORDER)
        plot_health_status_distribution(df)

        logger.info(REPORT_BORDER)
        logger.info("Patient Health Analyzer - Execution completed successfully")
        logger.info(REPORT_BORDER)

    except PatientHealthAnalyzerError as e:
        logger.error(f"Patient Health Analyzer - Execution failed: {str(e)}", exc_info=True)
        logger.error(REPORT_BORDER)
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error in Patient Health Analyzer: {str(e)}", exc_info=True
        )
        logger.error(REPORT_BORDER)
        raise
