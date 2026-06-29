"""Visualization and charts page."""

import streamlit as st
import pandas as pd
import plotly.express as px

from read_patients_web import create_health_status_chart
from constants import CSV_HEALTH_STATUS_COLUMN


def show():
    """Display the visualization page."""
    st.title("📈 Visualizations")

    # Check if data has been loaded
    if not st.session_state.get("file_uploaded", False) or "patient_df" not in st.session_state:
        st.warning("⚠️ Please upload data first on the **Upload Data** page.")
        return

    df = st.session_state.patient_df

    # Tab selection for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Distribution", "BMI Analysis", "Glucose Analysis", "Blood Pressure Analysis"]
    )

    with tab1:
        st.subheader("Health Status Distribution")
        st.write("Overview of patient health status categories")

        col1, col2 = st.columns(2)

        with col1:
            # Matplotlib version
            st.write("**Bar Chart (Matplotlib)**")
            fig, success, error_msg = create_health_status_chart(df)

            if success and fig is not None:
                st.pyplot(fig)
            else:
                st.error(f"❌ {error_msg}")

        with col2:
            # Plotly interactive version
            st.write("**Interactive Chart (Plotly)**")
            try:
                health_counts = df[CSV_HEALTH_STATUS_COLUMN].value_counts()

                fig_plotly = px.bar(
                    x=health_counts.index,
                    y=health_counts.values,
                    labels={"x": "Health Status", "y": "Number of Patients"},
                    title="Patient Distribution by Health Status",
                    color=health_counts.index,
                    color_discrete_map={
                        "Healthy": "#2ecc71",
                        "AtRisk": "#f39c12",
                        "Critical": "#e74c3c",
                    },
                )

                fig_plotly.update_layout(
                    showlegend=False,
                    height=400,
                    hovermode="x unified",
                )

                st.plotly_chart(fig_plotly, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error creating interactive chart: {str(e)}")

    with tab2:
        st.subheader("BMI Analysis")
        st.write("Body Mass Index distribution and statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Average BMI", f"{df['BMI'].mean():.2f}")
            st.metric("Min BMI", f"{df['BMI'].min():.2f}")
            st.metric("Max BMI", f"{df['BMI'].max():.2f}")

        with col2:
            st.metric("Std Dev BMI", f"{df['BMI'].std():.2f}")
            st.metric("Median BMI", f"{df['BMI'].median():.2f}")

        # BMI distribution histogram
        try:
            fig_bmi = px.histogram(
                df,
                x="BMI",
                nbins=15,
                title="BMI Distribution",
                labels={"BMI": "Body Mass Index", "count": "Number of Patients"},
                color_discrete_sequence=["#3498db"],
            )

            fig_bmi.update_layout(
                showlegend=False,
                height=400,
                hovermode="x unified",
            )

            st.plotly_chart(fig_bmi, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error creating BMI chart: {str(e)}")

        # BMI vs Health Status
        try:
            fig_bmi_status = px.box(
                df,
                x=CSV_HEALTH_STATUS_COLUMN,
                y="BMI",
                title="BMI Distribution by Health Status",
                labels={"BMI": "Body Mass Index", CSV_HEALTH_STATUS_COLUMN: "Health Status"},
                color=CSV_HEALTH_STATUS_COLUMN,
                color_discrete_map={
                    "Healthy": "#2ecc71",
                    "AtRisk": "#f39c12",
                    "Critical": "#e74c3c",
                },
            )

            fig_bmi_status.update_layout(
                showlegend=False,
                height=400,
            )

            st.plotly_chart(fig_bmi_status, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error creating BMI vs Status chart: {str(e)}")

    with tab3:
        st.subheader("Glucose Level Analysis")
        st.write("Glucose level distribution and statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Average Glucose", f"{df['Glucose_level'].mean():.2f}")
            st.metric("Min Glucose", f"{df['Glucose_level'].min():.2f}")
            st.metric("Max Glucose", f"{df['Glucose_level'].max():.2f}")

        with col2:
            st.metric("Std Dev Glucose", f"{df['Glucose_level'].std():.2f}")
            st.metric("Median Glucose", f"{df['Glucose_level'].median():.2f}")

        # Glucose distribution histogram
        try:
            fig_glucose = px.histogram(
                df,
                x="Glucose_level",
                nbins=15,
                title="Glucose Level Distribution",
                labels={"Glucose_level": "Glucose (mg/dL)", "count": "Number of Patients"},
                color_discrete_sequence=["#e74c3c"],
            )

            fig_glucose.update_layout(
                showlegend=False,
                height=400,
                hovermode="x unified",
            )

            st.plotly_chart(fig_glucose, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error creating Glucose chart: {str(e)}")

        # Glucose vs Health Status
        try:
            fig_glucose_status = px.box(
                df,
                x=CSV_HEALTH_STATUS_COLUMN,
                y="Glucose_level",
                title="Glucose Distribution by Health Status",
                labels={"Glucose_level": "Glucose (mg/dL)", CSV_HEALTH_STATUS_COLUMN: "Health Status"},
                color=CSV_HEALTH_STATUS_COLUMN,
                color_discrete_map={
                    "Healthy": "#2ecc71",
                    "AtRisk": "#f39c12",
                    "Critical": "#e74c3c",
                },
            )

            fig_glucose_status.update_layout(
                showlegend=False,
                height=400,
            )

            st.plotly_chart(fig_glucose_status, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error creating Glucose vs Status chart: {str(e)}")

    with tab4:
        st.subheader("Blood Pressure Analysis")
        st.write("Blood pressure readings by health status")

        try:
            fig_bp_status = px.box(
                df,
                x=CSV_HEALTH_STATUS_COLUMN,
                y="Blood_pressure",
                title="Blood Pressure by Health Status",
                labels={"Blood_pressure": "Blood Pressure", CSV_HEALTH_STATUS_COLUMN: "Health Status"},
                color=CSV_HEALTH_STATUS_COLUMN,
                color_discrete_map={
                    "Healthy": "#2ecc71",
                    "AtRisk": "#f39c12",
                    "Critical": "#e74c3c",
                },
            )

            fig_bp_status.update_layout(
                showlegend=False,
                height=400,
            )

            st.plotly_chart(fig_bp_status, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error creating Blood Pressure chart: {str(e)}")

        # Blood Pressure summary
        st.write("**Blood Pressure Summary:**")
        st.dataframe(df[["name", "Blood_pressure", CSV_HEALTH_STATUS_COLUMN]], use_container_width=True)


if __name__ == "__main__":
    show()
