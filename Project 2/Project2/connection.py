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

# Load data from Transactions table into a pandas DataFrame
transactions_query = "SELECT * FROM Transactions"
transactions_df = pd.read_sql(transactions_query, conn)

# load Users and FraudLabels data
users_query = "SELECT * FROM Users"
users_df = pd.read_sql(users_query, conn)

fraudlabels_query = "SELECT * FROM FraudLabels"
fraudlabels_df = pd.read_sql(fraudlabels_query, conn)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Connected successfully!")

# Display the data
print(transactions_df.head())
print(users_df.head())
print(fraudlabels_df.head())

# Re-open connection for writing processed data
'''conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-2S6KAQD\SQLEXPRESS;'
    'DATABASE=Project2;'
    'Trusted_Connection=yes;'
)

# Save the processed DataFrame to a new table in MSSQL
transactions_df.to_sql('ProcessedTransactions', conn, if_exists='replace', index=False)

# Close the connection when done
conn.close()'''