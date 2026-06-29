"""Web-compatible wrapper functions for Patient Health Analyzer.

This module provides Streamlit-compatible versions of functions from read_patients.py.
It maintains separation between business logic and web UI while reusing core functionality.
"""

from typing import Tuple, Dict, List
import pandas as pd
import matplotlib.pyplot as plt

from read_patients import (
    categorize_patient_health,
    _evaluate_bmi,
    _evaluate_blood_pressure,
    _evaluate_glucose,
    _parse_blood_pressure,
    _determine_overall_category,
    add_health_category,
    _get_chart_colors,
    _configure_chart_appearance,
    _add_bar_labels,
)
from constants import (
    CSV_HEALTH_STATUS_COLUMN,
    CHART_FIGURE_SIZE,
    CHART_BAR_EDGE_COLOR,
    CHART_BAR_EDGE_WIDTH,
)
from models import HealthStatus
import logging

logger = logging.getLogger(__name__)


def process_patient_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, bool, str]:
    """Process and categorize patient data for web display.

    This function wraps add_health_category() for use in Streamlit context.
    It provides better error handling and status information for UI feedback.

    Args:
        df (pd.DataFrame): DataFrame with patient health metrics

    Returns:
        Tuple[pd.DataFrame, bool, str]:
            - DataFrame with health_status column added
            - Success flag (True if processing succeeded)
            - Message (empty string if success, error message if failed)
    """
    try:
        df_processed = add_health_category(df)
        return df_processed, True, ""
    except Exception as e:
        error_msg = f"Error processing patient data: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return df, False, error_msg


def create_health_status_chart(df: pd.DataFrame) -> Tuple[plt.Figure, bool, str]:
    """Create health status distribution chart for Streamlit display.

    Refactored version of plot_health_status_distribution() that returns the
    figure object instead of saving to file or calling plt.show().

    Args:
        df (pd.DataFrame): DataFrame with health_status column

    Returns:
        Tuple[plt.Figure, bool, str]:
            - matplotlib Figure object (or None if failed)
            - Success flag
            - Message (empty string if success, error message if failed)
    """
    try:
        health_counts: pd.Series = df[CSV_HEALTH_STATUS_COLUMN].value_counts()
        logger.debug(f"Health status distribution: {health_counts.to_dict()}")

        fig, ax = plt.subplots(figsize=CHART_FIGURE_SIZE)
        bar_colors: List[str] = _get_chart_colors(health_counts.index)

        bars = ax.bar(
            health_counts.index,
            health_counts.values,
            color=bar_colors,
            edgecolor=CHART_BAR_EDGE_COLOR,
            linewidth=CHART_BAR_EDGE_WIDTH,
        )

        ax.set_xlabel("Health Status", fontsize=12, fontweight="bold")
        ax.set_ylabel("Number of Patients", fontsize=12, fontweight="bold")
        ax.set_title(
            "Patient Distribution by Health Status", fontsize=14, fontweight="bold"
        )
        ax.grid(axis="y", alpha=0.3, linestyle="--")

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
            )

        plt.tight_layout()
        return fig, True, ""

    except Exception as e:
        error_msg = f"Error creating chart: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return None, False, error_msg


def get_health_summary(df: pd.DataFrame) -> Tuple[Dict[str, int], bool, str]:
    """Extract health status summary statistics from DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with health_status column

    Returns:
        Tuple[Dict[str, int], bool, str]:
            - Dictionary with counts by status (e.g., {'Healthy': 4, 'AtRisk': 3})
            - Success flag
            - Message (empty string if success, error message if failed)
    """
    try:
        summary = df[CSV_HEALTH_STATUS_COLUMN].value_counts().to_dict()

        # Ensure all status types are in the dict with 0 count if not present
        default_summary = {
            HealthStatus.HEALTHY.value: 0,
            HealthStatus.AT_RISK.value: 0,
            HealthStatus.CRITICAL.value: 0,
        }
        default_summary.update(summary)

        return default_summary, True, ""

    except Exception as e:
        error_msg = f"Error calculating summary: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {}, False, error_msg


def evaluate_patient_metrics(
    bmi: float, blood_pressure: str, glucose_level: float
) -> Tuple[Dict[str, str], bool, str]:
    """Evaluate individual patient health metrics in real-time.

    Useful for single-patient metric display or form validation.

    Args:
        bmi (float): Body Mass Index
        blood_pressure (str): Blood pressure in 'systolic/diastolic' format
        glucose_level (float): Glucose level in mg/dL

    Returns:
        Tuple[Dict[str, str], bool, str]:
            - Dictionary with individual metric statuses
            - Success flag
            - Message (empty string if success, error message if failed)
    """
    try:
        # Parse and validate blood pressure
        try:
            systolic, diastolic = _parse_blood_pressure(blood_pressure)
        except Exception as e:
            return {}, False, f"Invalid blood pressure format: {str(e)}"

        # Evaluate each metric
        bmi_status = _evaluate_bmi(float(bmi))
        bp_status = _evaluate_blood_pressure(systolic, diastolic)
        glucose_status = _evaluate_glucose(float(glucose_level))

        metrics = {
            "BMI": bmi_status,
            "Blood Pressure": bp_status,
            "Glucose": glucose_status,
            "Overall": _determine_overall_category(
                [bmi_status, bp_status, glucose_status]
            ),
        }

        return metrics, True, ""

    except ValueError as e:
        error_msg = f"Invalid input values: {str(e)}"
        logger.warning(error_msg)
        return {}, False, error_msg
    except Exception as e:
        error_msg = f"Error evaluating metrics: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {}, False, error_msg
