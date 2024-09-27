import pyodbc
#import pandas as pd

# Define the connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-2S6KAQD\SQLEXPRESS;"  
    "DATABASE=Project1;"
    "Trusted_Connection=yes;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
print("Connected successfully")