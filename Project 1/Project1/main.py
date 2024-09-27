import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the data
df = pd.read_csv('D:/varshini/Hexaware/training/Training 4/Project/Project 1/transaction_fact.csv')

# Handle missing values
df['transaction_amount'] = df['transaction_amount'].fillna(df['transaction_amount'].mean())
df['payment_method'] = df['payment_method'].fillna('Unknown')

# Normalize transaction amounts
scaler = MinMaxScaler()
df['normalized_amount'] = scaler.fit_transform(df[['transaction_amount']])

# Feature Engineering
# 1. Transaction Frequency
df['transaction_count'] = df.groupby('user_id')['transaction_id'].transform('count')

# 2. Location Changes
df['location_change'] = df.groupby('user_id')['location'].transform(lambda x: x != x.shift()).astype(int)

# 3. Deviation from Typical User Behavior
df['mean_transaction_amount'] = df.groupby('user_id')['transaction_amount'].transform('mean')
df['amount_deviation'] = df['transaction_amount'] - df['mean_transaction_amount']

# View the processed data
print(df.head())
