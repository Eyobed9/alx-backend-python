import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to the MySQL server (no database selected)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # Change if your MySQL has a password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")


def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Add password if needed
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection to ALX_prodev error: {err}")
        return None


def create_table(connection):
    """Create user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_data(connection, filename):
    """Insert data from a CSV file into the user_data table"""
    try:
        cursor = connection.cursor()
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row.get("user_id") or str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Check if the user already exists
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s;", (user_id,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))

        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")


def stream_user_data(connection):
    """Generator that yields one row at a time from user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        cursor.close()
    except Exception as e:
        print(f"Error streaming user data: {e}")
