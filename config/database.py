import os
import pyodbc


def get_connection():
    server = os.environ.get('SQL_SERVER', 'YOUR_SERVER_NAME\\SQLEXPRESS')
    try:
        conn = pyodbc.connect(
            'Driver={SQL Server};'
            f'Server={server};'
            'Database=python_project;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print(f"Connection Error: {e}")
        return None