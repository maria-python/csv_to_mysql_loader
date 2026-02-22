import csv
import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG


def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        city VARCHAR(100)
    )
    """
    cursor.execute(create_table_query)


def insert_data(cursor, row):
    insert_query = """
    INSERT INTO users (name, age, city)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (row["name"], int(row["age"]), row["city"]))


def load_csv_to_db(csv_file):
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        create_table(cursor)

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                insert_data(cursor, row)

        connection.commit()
        print("Data successfully inserted into database")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()
        print("Database connection closed")


if __name__ == "__main__":
    load_csv_to_db("sample.csv")