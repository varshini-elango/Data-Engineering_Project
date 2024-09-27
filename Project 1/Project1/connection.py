import pyodbc
import pandas as pd

# Define the connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-2S6KAQD\SQLEXPRESS;"  
    "DATABASE=Project1;"
    "Trusted_Connection=yes;"
)

# Establish a connection to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Function to insert data from a DataFrame into a table
def insert_data(df, table_name, exclude_columns=[]):
    for index, row in df.iterrows():
        # Exclude specific columns (e.g., timestamp)
        columns = [col for col in df.columns if col not in exclude_columns]
        placeholders = ', '.join('?' * len(columns))
        columns_str = ', '.join(columns)

        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        # Get the row data for the selected columns
        values = tuple(row[col] for col in columns)

        cursor.execute(sql, values)

# Load and insert data from user_dim.csv
user_dim_df = pd.read_csv('D:/varshini/Hexaware/training/Training 4/Project/Project 1/user_dim.csv')
insert_data(user_dim_df, 'user_dim')

# Load and insert data from transaction_fact.csv
transaction_fact_df = pd.read_csv('D:/varshini/Hexaware/training/Training 4/Project/Project 1/transaction_fact.csv')
insert_data(transaction_fact_df, 'transaction_fact',exclude_columns=['transaction_time'])

# Load and insert data from fraud_indicators.csv
fraud_indicators_df = pd.read_csv('D:/varshini/Hexaware/training/Training 4/Project/Project 1/fraud_indicators.csv')
insert_data(fraud_indicators_df, 'fraud_indicators')

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data insertion completed successfully!")

