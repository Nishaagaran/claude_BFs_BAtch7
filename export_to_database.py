import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PatientDatabaseManager:
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
                ssl_disabled=True
            )
            logging.info("Connected to MySQL server")
            return True
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return False

    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.connection.database = self.database
            logging.info(f"Database '{self.database}' created or already exists")
            cursor.close()
            return True
        except Error as e:
            logging.error(f"Error creating database: {e}")
            return False

    def create_table(self):
        """Create sampledata table"""
        try:
            cursor = self.connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS sampledata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                PatientID VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                BMI FLOAT NOT NULL,
                Blood_pressure VARCHAR(20) NOT NULL,
                Glucose_level INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            self.connection.commit()
            logging.info("Table 'sampledata' created successfully")
            cursor.close()
            return True
        except Error as e:
            logging.error(f"Error creating table: {e}")
            return False

    def export_csv_to_database(self, csv_file):
        """Export CSV data to database"""
        try:
            df = pd.read_csv(csv_file)
            logging.info(f"Loaded CSV file with {len(df)} rows")

            cursor = self.connection.cursor()

            insert_query = """
            INSERT INTO sampledata (PatientID, name, age, gender, BMI, Blood_pressure, Glucose_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            for index, row in df.iterrows():
                try:
                    cursor.execute(insert_query, (
                        row['Paitentid'],
                        row['name'],
                        int(row['age']),
                        row['gender'],
                        float(row['BMI']),
                        row['Blood_pressure'],
                        int(row['Glucose_level'])
                    ))
                except Error as e:
                    logging.warning(f"Row {index} skipped: {e}")
                    self.connection.rollback()

            self.connection.commit()
            logging.info(f"Successfully exported {len(df)} records to database")
            cursor.close()
            return True
        except Exception as e:
            logging.error(f"Error exporting CSV to database: {e}")
            return False

    def read_all_data(self):
        """Read all data from sampledata table"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sampledata")
            results = cursor.fetchall()
            cursor.close()
            logging.info(f"Retrieved {len(results)} records from database")
            return results
        except Error as e:
            logging.error(f"Error reading data: {e}")
            return None

    def read_data_by_health_status(self, status=None):
        """Read data filtered by health status"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if status:
                query = f"""
                SELECT * FROM sampledata
                WHERE (CASE
                    WHEN BMI >= 30 OR CAST(SUBSTRING_INDEX(Blood_pressure, '/', 1) AS DECIMAL(5,1)) >= 180
                         OR CAST(SUBSTRING_INDEX(Blood_pressure, '/', -1) AS DECIMAL(5,1)) >= 120
                         OR Glucose_level >= 126 THEN 'Critical'
                    WHEN BMI >= 25 OR CAST(SUBSTRING_INDEX(Blood_pressure, '/', 1) AS DECIMAL(5,1)) >= 130
                         OR CAST(SUBSTRING_INDEX(Blood_pressure, '/', -1) AS DECIMAL(5,1)) >= 85
                         OR Glucose_level >= 100 THEN 'AtRisk'
                    ELSE 'Healthy'
                END) = %s
                """
                cursor.execute(query, (status,))
            else:
                cursor.execute("SELECT * FROM sampledata")

            results = cursor.fetchall()
            cursor.close()
            logging.info(f"Retrieved {len(results)} records with status '{status}'")
            return results
        except Error as e:
            logging.error(f"Error reading filtered data: {e}")
            return None

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")


def main():
    # Initialize database manager
    db_manager = PatientDatabaseManager(
        host='localhost',
        user='root',
        password='Tek@12345',
        database='test_db'
    )

    # Connect to MySQL
    if not db_manager.connect():
        logging.error("Failed to connect to MySQL server")
        return

    # Create database
    if not db_manager.create_database():
        logging.error("Failed to create database")
        return

    # Create table
    if not db_manager.create_table():
        logging.error("Failed to create table")
        return

    # Export CSV to database
    csv_file = 'sample_paitents.csv'
    if not db_manager.export_csv_to_database(csv_file):
        logging.error("Failed to export CSV data")
        return

    # Read all data
    logging.info("\n=== All Patient Data ===")
    all_data = db_manager.read_all_data()
    if all_data:
        for patient in all_data:
            print(patient)

    # Close connection
    db_manager.close_connection()
    logging.info("Export and read operation completed successfully")


if __name__ == "__main__":
    main()
