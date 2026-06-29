"""Upload and process patient data page."""

import streamlit as st
import pandas as pd

from web_utils import validate_csv_file, validate_dataframe_schema, display_data_summary, display_column_info, display_error_message
from read_patients_web import process_patient_data
from exceptions import PatientHealthAnalyzerError


def show():
    """Display the upload and data processing page."""
    st.title("📁 Upload Patient Data")

    st.write(
        """
        Upload a CSV file containing patient health data. The file must include
        the following columns:
        - **Paitentid**: Unique patient identifier
        - **name**: Patient name
        - **BMI**: Body Mass Index
        - **Blood_pressure**: In format 'systolic/diastolic' (e.g., '130/85')
        - **Glucose_level**: Fasting glucose level in mg/dL
        """
    )

    # File uploader
    st.subheader("Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose a CSV file", type="csv", help="Upload a CSV file with patient data"
    )

    if uploaded_file is not None:
        # Validate and load file
        st.write("---")
        st.write("**Processing uploaded file...**")

        df, success, error_msg = validate_csv_file(uploaded_file)

        if not success:
            st.error(f"❌ {error_msg}")
            st.info("Please check your CSV file and try again.")
            return

        # Display data summary
        st.success("✅ File loaded successfully!")

        st.subheader("📊 Data Summary")
        display_data_summary(df)

        st.subheader("📋 Column Details")
        with st.expander("Show column information"):
            display_column_info(df)

        # Process data
        st.subheader("🔄 Health Categorization")
        if st.button("Process Patient Data", type="primary", use_container_width=True):
            with st.spinner("Processing patient data..."):
                df_processed, success, error_msg = process_patient_data(df)

                if not success:
                    st.error(f"❌ {error_msg}")
                    st.info("Please check your data and try again.")
                    return

                st.success("✅ Data processed successfully!")

                # Store in session state for other pages
                st.session_state.patient_df = df_processed
                st.session_state.file_uploaded = True

                # Display results
                st.write("**Processed Data Preview:**")
                st.dataframe(
                    df_processed,
                    use_container_width=True,
                    hide_index=True,
                )

                # Show next steps
                st.info(
                    "✨ Data ready for analysis! "
                    "Go to the **Analysis** page to see detailed metrics and charts."
                )

    else:
        st.info(
            "👆 Upload a CSV file to get started. "
            "The file must contain patient health data with required columns."
        )

        # Show sample CSV structure
        with st.expander("📝 Sample CSV Format"):
            sample_data = {
                "Paitentid": ["P001", "P002", "P003"],
                "name": ["John Smith", "Jane Doe", "Bob Wilson"],
                "BMI": [26.5, 23.2, 29.8],
                "Blood_pressure": ["130/85", "118/76", "145/92"],
                "Glucose_level": [105, 92, 148],
            }
            sample_df = pd.DataFrame(sample_data)
            st.dataframe(sample_df, use_container_width=True)

            # Download sample
            csv = sample_df.to_csv(index=False)
            st.download_button(
                label="Download Sample CSV",
                data=csv,
                file_name="sample_patient_data.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    show()
