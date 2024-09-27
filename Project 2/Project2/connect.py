import pyodbc
import pandas as pd

# Connect to MSSQL database
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-2S6KAQD\SQLEXPRESS;'
    'DATABASE=Project2;'
    'Trusted_Connection=yes;'
)

# Create a cursor
#conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
print("connected successfully")