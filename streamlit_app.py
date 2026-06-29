"""Patient Health Analyzer - Streamlit Web Application

Main entry point for the web-based dashboard application.
Provides multi-page interface for uploading, analyzing, and visualizing patient health data.
"""

import streamlit as st
from pages import upload_page, analysis_page, visualize_page

# Configure Streamlit page
st.set_page_config(
    page_title="Patient Health Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "patient_df" not in st.session_state:
    st.session_state.patient_df = None

# Sidebar navigation
with st.sidebar:
    st.title("🏥 Patient Health Analyzer")
    st.write("---")

    # Navigation
    page = st.radio(
        "📍 Navigation",
        ["Upload Data", "Analysis", "Visualizations"],
        index=0,
        help="Navigate to different sections of the application",
    )

    st.write("---")

    # Session info
    if st.session_state.file_uploaded and st.session_state.patient_df is not None:
        st.success("✅ Data Loaded")
        st.metric("Patients", len(st.session_state.patient_df))

        if st.button("🔄 Clear Data", use_container_width=True):
            st.session_state.file_uploaded = False
            st.session_state.patient_df = None
            st.rerun()
    else:
        st.info("📁 No data loaded yet")

    st.write("---")

    # About section
    with st.expander("ℹ️ About"):
        st.write(
            """
            **Patient Health Analyzer** is a web-based dashboard for analyzing
            patient health metrics and risk categorization.

            ### Features:
            - 📁 Upload patient data from CSV
            - 📊 View health status metrics
            - 📈 Interactive visualizations
            - 💾 Export analysis results

            ### Health Categories:
            - 🟢 **Healthy**: Low health risk
            - 🟡 **At Risk**: Moderate health concerns
            - 🔴 **Critical**: High health risk
            """
        )

    st.write("---")

    # Help section
    with st.expander("❓ Help"):
        st.write(
            """
            ### Required CSV Columns:
            1. **Paitentid**: Unique patient ID
            2. **name**: Patient name
            3. **BMI**: Body Mass Index
            4. **Blood_pressure**: Format 'systolic/diastolic'
            5. **Glucose_level**: Glucose in mg/dL

            ### Tips:
            - Use the Upload page to load your data
            - Check the Analysis page for detailed metrics
            - View charts on the Visualizations page
            """
        )

# Main content area
if page == "Upload Data":
    from pages import upload_page as page_module
    page_module.show()

elif page == "Analysis":
    from pages import analysis_page as page_module
    page_module.show()

elif page == "Visualizations":
    from pages import visualize_page as page_module
    page_module.show()

# Footer
st.write("---")
st.caption("Patient Health Analyzer v1.0 | Built with Streamlit")
