# utils/helpers.py
import psycopg2

def get_database_connection():
    """
    Creates a connection to the PostgreSQL database.

    Returns:
        connection: A psycopg2 connection object.
    """
    try:
        connection = psycopg2.connect(
            dbname="acma_db",
            user="user",
            password="password",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None
    
def validate_input(data, schema):
    """
    Validates the given data against the provided schema.
    
    Args:
        data (dict): The input data to validate.
        schema (dict): The schema to validate against.
    
    Returns:
        bool: True if data is valid, False otherwise.
    """
    try:
        for key, rules in schema.items():
            if key not in data:
                return False
            if not isinstance(data[key], rules['type']):
                return False
        return True
    except Exception as e:
        return False


def format_date(date, format="%Y-%m-%d"):
    """
    Formats a given date into the specified format.
    
    Args:
        date (datetime): The date object to format.
        format (str): The format string.
    
    Returns:
        str: The formatted date as a string.
    """
    from datetime import datetime
    if isinstance(date, datetime):
        return date.strftime(format)
    return date
