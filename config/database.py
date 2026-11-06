import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=YOUR_SERVER_NAME\\SQLEXPRESS;'
            'Database=python_project;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print(f"Connection Error: {e}")
        return None