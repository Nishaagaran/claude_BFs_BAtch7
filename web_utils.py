"""Utility functions for Streamlit web application.

Provides helper functions for data validation, formatting, error display,
and other common UI operations.
"""

from typing import Tuple, Dict, Optional
import pandas as pd
import streamlit as st

from constants import (
    CSV_PATIENT_ID_COLUMN,
    CSV_NAME_COLUMN,
    CSV_BMI_COLUMN,
    CSV_BLOOD_PRESSURE_COLUMN,
    CSV_GLUCOSE_COLUMN,
    CSV_HEALTH_STATUS_COLUMN,
)
from exceptions import (
    PatientHealthAnalyzerError,
    BloodPressureFormatError,
    PatientDataError,
    DataLoadError,
    VisualizationError,
)
from models import HealthStatus


def validate_dataframe_schema(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate that DataFrame has all required columns.

    Args:
        df (pd.DataFrame): DataFrame to validate

    Returns:
        Tuple[bool, str]:
            - True if valid, False otherwise
            - Message describing any validation issues
    """
    required_columns = [
        CSV_PATIENT_ID_COLUMN,
        CSV_NAME_COLUMN,
        CSV_BMI_COLUMN,
        CSV_BLOOD_PRESSURE_COLUMN,
        CSV_GLUCOSE_COLUMN,
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    if len(df) == 0:
        return False, "DataFrame is empty. Please upload a file with patient data."

    return True, ""


def validate_csv_file(uploaded_file) -> Tuple[Optional[pd.DataFrame], bool, str]:
    """Validate and load CSV file uploaded via Streamlit.

    Args:
        uploaded_file: Streamlit file uploader object

    Returns:
        Tuple[Optional[pd.DataFrame], bool, str]:
            - DataFrame if successful, None otherwise
            - Success flag
            - Error message if failed, empty string if successful
    """
    if uploaded_file is None:
        return None, False, "No file uploaded"

    try:
        df = pd.read_csv(uploaded_file)

        # Check if DataFrame has data
        if df.empty:
            return None, False, "CSV file is empty. Please provide patient data."

        # Basic schema validation
        is_valid, error_msg = validate_dataframe_schema(df)
        if not is_valid:
            return None, False, error_msg

        return df, True, ""

    except pd.errors.ParserError as e:
        return None, False, f"Failed to parse CSV: {str(e)}"
    except Exception as e:
        return None, False, f"Error reading file: {str(e)}"


def display_error_message(error: Exception) -> None:
    """Display appropriate error message based on exception type.

    Uses Streamlit st.error() to display user-friendly error messages.

    Args:
        error (Exception): Exception object to display
    """
    if isinstance(error, BloodPressureFormatError):
        st.error(f"❌ Blood Pressure Format Error: {str(error)}")
    elif isinstance(error, PatientDataError):
        st.error(f"❌ Patient Data Error: {str(error)}")
    elif isinstance(error, DataLoadError):
        st.error(f"❌ Data Loading Error: {str(error)}")
    elif isinstance(error, VisualizationError):
        st.error(f"❌ Visualization Error: {str(error)}")
    elif isinstance(error, PatientHealthAnalyzerError):
        st.error(f"❌ Application Error: {str(error)}")
    else:
        st.error(f"❌ Unexpected Error: {str(error)}")


def format_health_status_summary(
    df: pd.DataFrame,
) -> Tuple[Dict[str, int], Optional[str]]:
    """Format health status summary for display.

    Args:
        df (pd.DataFrame): DataFrame with health_status column

    Returns:
        Tuple[Dict[str, int], Optional[str]]:
            - Dictionary with status counts
            - Error message if failed, None if successful
    """
    try:
        summary = df[CSV_HEALTH_STATUS_COLUMN].value_counts().to_dict()

        # Ensure all statuses are present
        result = {
            HealthStatus.HEALTHY.value: summary.get(HealthStatus.HEALTHY.value, 0),
            HealthStatus.AT_RISK.value: summary.get(HealthStatus.AT_RISK.value, 0),
            HealthStatus.CRITICAL.value: summary.get(HealthStatus.CRITICAL.value, 0),
        }

        return result, None
    except Exception as e:
        return {}, f"Error formatting summary: {str(e)}"


def get_status_color(status: str) -> str:
    """Get Streamlit color for health status.

    Args:
        status (str): Health status string ('Healthy', 'AtRisk', or 'Critical')

    Returns:
        str: Streamlit color code
    """
    color_map = {
        HealthStatus.HEALTHY.value: "green",
        HealthStatus.AT_RISK.value: "orange",
        HealthStatus.CRITICAL.value: "red",
    }
    return color_map.get(status, "gray")


def display_data_summary(df: pd.DataFrame) -> None:
    """Display basic summary of loaded data.

    Args:
        df (pd.DataFrame): DataFrame to summarize
    """
    st.write(f"📊 **Total Records:** {len(df)}")
    st.write(f"📋 **Columns:** {', '.join(df.columns)}")

    # Show first few rows
    st.write("**Preview (First 5 rows):**")
    st.dataframe(df.head(), use_container_width=True)


def display_column_info(df: pd.DataFrame) -> None:
    """Display column information and data types.

    Args:
        df (pd.DataFrame): DataFrame to analyze
    """
    st.write("**Column Information:**")
    col_info = pd.DataFrame(
        {
            "Column": df.columns,
            "Type": df.dtypes,
            "Non-Null Count": df.count(),
        }
    )
    st.dataframe(col_info, use_container_width=True)


def format_number(value: float, decimal_places: int = 2) -> str:
    """Format number for display.

    Args:
        value (float): Number to format
        decimal_places (int): Number of decimal places (default: 2)

    Returns:
        str: Formatted number string
    """
    return f"{value:.{decimal_places}f}"
