import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PatientDataReader:
    def __init__(self, host='localhost', user='root', password='', database='patient_health'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                ssl_disabled=True
            )
            logging.info(f"Connected to database '{self.database}'")
            return True
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return False

    def read_all_patients(self):
        """Read all patient records from database"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sampledata ORDER BY id")
            results = cursor.fetchall()
            cursor.close()
            logging.info(f"Retrieved {len(results)} patient records")
            return results
        except Error as e:
            logging.error(f"Error reading all patients: {e}")
            return None

    def read_patient_by_id(self, patient_id):
        """Read specific patient by PatientID"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sampledata WHERE PatientID = %s", (patient_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                logging.info(f"Found patient {patient_id}")
            else:
                logging.warning(f"Patient {patient_id} not found")
            return result
        except Error as e:
            logging.error(f"Error reading patient: {e}")
            return None

    def read_patients_as_dataframe(self):
        """Read all patient data as pandas DataFrame"""
        try:
            query = "SELECT * FROM sampledata ORDER BY id"
            df = pd.read_sql(query, self.connection)
            logging.info(f"Converted {len(df)} records to DataFrame")
            return df
        except Error as e:
            logging.error(f"Error reading data as DataFrame: {e}")
            return None

    def get_statistics(self):
        """Get health statistics from patient data"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Count by gender
            cursor.execute("""
                SELECT gender, COUNT(*) as count
                FROM sampledata
                GROUP BY gender
            """)
            gender_stats = cursor.fetchall()

            # Average metrics
            cursor.execute("""
                SELECT
                    ROUND(AVG(age), 2) as avg_age,
                    ROUND(AVG(BMI), 2) as avg_bmi,
                    ROUND(AVG(Glucose_level), 2) as avg_glucose,
                    MIN(age) as min_age,
                    MAX(age) as max_age
                FROM sampledata
            """)
            metrics = cursor.fetchone()

            cursor.close()

            return {
                'gender_distribution': gender_stats,
                'health_metrics': metrics
            }
        except Error as e:
            logging.error(f"Error getting statistics: {e}")
            return None

    def search_patients(self, **criteria):
        """Search patients by multiple criteria"""
        try:
            conditions = []
            params = []

            if 'name' in criteria:
                conditions.append("name LIKE %s")
                params.append(f"%{criteria['name']}%")

            if 'gender' in criteria:
                conditions.append("gender = %s")
                params.append(criteria['gender'])

            if 'age_min' in criteria:
                conditions.append("age >= %s")
                params.append(criteria['age_min'])

            if 'age_max' in criteria:
                conditions.append("age <= %s")
                params.append(criteria['age_max'])

            if 'bmi_min' in criteria:
                conditions.append("BMI >= %s")
                params.append(criteria['bmi_min'])

            if 'bmi_max' in criteria:
                conditions.append("BMI <= %s")
                params.append(criteria['bmi_max'])

            if not conditions:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM sampledata")
            else:
                where_clause = " AND ".join(conditions)
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute(f"SELECT * FROM sampledata WHERE {where_clause}", params)

            results = cursor.fetchall()
            cursor.close()
            logging.info(f"Found {len(results)} matching patients")
            return results
        except Error as e:
            logging.error(f"Error searching patients: {e}")
            return None

    def export_to_csv(self, output_file):
        """Export database data to CSV"""
        try:
            df = self.read_patients_as_dataframe()
            if df is not None:
                df.to_csv(output_file, index=False)
                logging.info(f"Exported data to {output_file}")
                return True
        except Exception as e:
            logging.error(f"Error exporting to CSV: {e}")
        return False

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")


def main():
    # Initialize reader
    reader = PatientDataReader(
        host='localhost',
        user='root',
        password='Tek@12345',
        database='test_db'
    )

    # Connect to database
    if not reader.connect():
        logging.error("Failed to connect to database")
        return

    # Read all patients
    logging.info("\n=== All Patients ===")
    patients = reader.read_all_patients()
    if patients:
        for patient in patients:
            print(f"ID: {patient['PatientID']}, Name: {patient['name']}, Age: {patient['age']}, "
                  f"Gender: {patient['gender']}, BMI: {patient['BMI']}, "
                  f"BP: {patient['Blood_pressure']}, Glucose: {patient['Glucose_level']}")

    # Read specific patient
    logging.info("\n=== Specific Patient ===")
    specific_patient = reader.read_patient_by_id('P001')
    if specific_patient:
        print(specific_patient)

    # Get statistics
    logging.info("\n=== Health Statistics ===")
    stats = reader.get_statistics()
    if stats:
        print("Gender Distribution:", stats['gender_distribution'])
        print("Health Metrics:", stats['health_metrics'])

    # Search patients
    logging.info("\n=== Search: Males aged 40-60 ===")
    search_results = reader.search_patients(gender='Male', age_min=40, age_max=60)
    if search_results:
        for patient in search_results:
            print(patient)

    # Export to CSV
    logging.info("\n=== Exporting to CSV ===")
    reader.export_to_csv('patient_data_from_db.csv')

    # Close connection
    reader.close_connection()


if __name__ == "__main__":
    main()
