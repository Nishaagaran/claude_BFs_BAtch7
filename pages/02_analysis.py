"""Data analysis and metrics page."""

import streamlit as st
import pandas as pd

from web_utils import (
    display_error_message,
    format_health_status_summary,
    get_status_color,
)
from read_patients_web import get_health_summary
from constants import CSV_HEALTH_STATUS_COLUMN
from models import HealthStatus


def show():
    """Display the analysis and metrics page."""
    st.title("📊 Patient Analysis")

    # Check if data has been loaded
    if not st.session_state.get("file_uploaded", False) or "patient_df" not in st.session_state:
        st.warning("⚠️ Please upload data first on the **Upload Data** page.")
        return

    df = st.session_state.patient_df

    # Display basic statistics
    st.subheader("📈 Overall Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Patients", len(df), delta=None)

    with col2:
        st.metric(
            "Average BMI",
            f"{df['BMI'].mean():.1f}",
            delta=None,
        )

    with col3:
        st.metric(
            "Average Glucose",
            f"{df['Glucose_level'].mean():.1f}",
            delta="mg/dL",
        )

    # Health status summary
    st.subheader("🏥 Health Status Distribution")

    summary, error_msg = get_health_summary(df)

    if error_msg:
        st.error(f"❌ {error_msg}")
        return

    # Display metrics for each status
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Healthy",
            summary.get(HealthStatus.HEALTHY.value, 0),
            delta=None,
        )

    with col2:
        st.metric(
            "At Risk",
            summary.get(HealthStatus.AT_RISK.value, 0),
            delta=None,
        )

    with col3:
        st.metric(
            "Critical",
            summary.get(HealthStatus.CRITICAL.value, 0),
            delta=None,
        )

    # Detailed patient table
    st.subheader("👥 Patient Details")

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")

        # Status filter
        status_filter = st.multiselect(
            "Filter by Health Status",
            options=[
                HealthStatus.HEALTHY.value,
                HealthStatus.AT_RISK.value,
                HealthStatus.CRITICAL.value,
            ],
            default=[
                HealthStatus.HEALTHY.value,
                HealthStatus.AT_RISK.value,
                HealthStatus.CRITICAL.value,
            ],
        )

        # BMI range filter
        bmi_min, bmi_max = st.slider(
            "BMI Range",
            min_value=float(df["BMI"].min()),
            max_value=float(df["BMI"].max()),
            value=(float(df["BMI"].min()), float(df["BMI"].max())),
            step=0.5,
        )

        # Glucose range filter
        glucose_min, glucose_max = st.slider(
            "Glucose Level Range (mg/dL)",
            min_value=float(df["Glucose_level"].min()),
            max_value=float(df["Glucose_level"].max()),
            value=(float(df["Glucose_level"].min()), float(df["Glucose_level"].max())),
            step=5.0,
        )

    # Apply filters
    filtered_df = df[
        (df[CSV_HEALTH_STATUS_COLUMN].isin(status_filter))
        & (df["BMI"] >= bmi_min)
        & (df["BMI"] <= bmi_max)
        & (df["Glucose_level"] >= glucose_min)
        & (df["Glucose_level"] <= glucose_max)
    ].copy()

    # Display filtered data
    st.write(f"**Showing {len(filtered_df)} of {len(df)} patients**")

    # Color-code the health status column for display
    def highlight_status(val):
        if val == HealthStatus.HEALTHY.value:
            color = "lightgreen"
        elif val == HealthStatus.AT_RISK.value:
            color = "lightyellow"
        elif val == HealthStatus.CRITICAL.value:
            color = "lightcoral"
        else:
            color = "white"
        return f"background-color: {color}"

    styled_df = filtered_df.style.applymap(
        highlight_status, subset=[CSV_HEALTH_STATUS_COLUMN]
    )
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Summary statistics
    st.subheader("📊 Health Status Breakdown (Filtered)")

    col1, col2, col3 = st.columns(3)

    with col1:
        healthy_count = len(filtered_df[filtered_df[CSV_HEALTH_STATUS_COLUMN] == HealthStatus.HEALTHY.value])
        st.write(f"**Healthy:** {healthy_count}")

    with col2:
        atrisk_count = len(filtered_df[filtered_df[CSV_HEALTH_STATUS_COLUMN] == HealthStatus.AT_RISK.value])
        st.write(f"**At Risk:** {atrisk_count}")

    with col3:
        critical_count = len(filtered_df[filtered_df[CSV_HEALTH_STATUS_COLUMN] == HealthStatus.CRITICAL.value])
        st.write(f"**Critical:** {critical_count}")

    # Detailed breakdown by column
    st.subheader("📋 Data Summary Statistics")

    summary_stats = filtered_df.describe()
    st.dataframe(summary_stats, use_container_width=True)

    # Export functionality
    st.subheader("💾 Export Data")

    col1, col2 = st.columns(2)

    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="patient_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        excel_buffer = pd.ExcelWriter("temp.xlsx", engine="openpyxl")
        filtered_df.to_excel(excel_buffer, index=False, sheet_name="Patients")
        excel_buffer.close()

        with open("temp.xlsx", "rb") as f:
            st.download_button(
                label="Download as Excel",
                data=f,
                file_name="patient_analysis.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )


if __name__ == "__main__":
    show()
