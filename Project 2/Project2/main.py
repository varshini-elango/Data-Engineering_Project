import pandas as pd

from connection import transactions_df, conn

#Data Preprocessing
# Handle Missing Values
print("Check for missing values:")
print(transactions_df.isnull().sum())
transactions_df['TransactionAmount'] = transactions_df['TransactionAmount'].fillna(transactions_df['TransactionAmount'].median())
transactions_df.dropna(subset=['UserID', 'TransactionTime'], inplace=True)
print(transactions_df.isnull().sum())

#Normalize Transaction Amounts
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
transactions_df['NormalizedAmount'] = scaler.fit_transform(transactions_df[['TransactionAmount']])
print("Transaction and Normalization:")
print(transactions_df[['TransactionAmount', 'NormalizedAmount']].head())

# Feature Engineering
#Time Difference Between Consecutive Transactions
print("Time Difference:")
transactions_df['TransactionTime'] = pd.to_datetime(transactions_df['TransactionTime'])
transactions_df = transactions_df.sort_values(by=['UserID', 'TransactionTime'])
transactions_df['TimeDiff'] = transactions_df.groupby('UserID')['TransactionTime'].diff().dt.total_seconds().fillna(0)
print(transactions_df[['UserID', 'TransactionTime', 'TimeDiff']].head())

#Transaction Frequency
print("Transaction Frequency:")
transaction_freq = transactions_df.groupby('UserID')['TransactionID'].count().reset_index(name='TransactionFrequency')
transactions_df = pd.merge(transactions_df, transaction_freq, on='UserID', how='left')
print(transactions_df[['UserID', 'TransactionFrequency']].head())

#Location Changes
print("Location Changes:")
location_changed = transactions_df.groupby('UserID')['TransactionLocation'].apply(lambda x: (x != x.shift(1)).astype(int))
location_changed = location_changed.reset_index(drop=True)
transactions_df['LocationChanged'] = location_changed
print(transactions_df[['UserID', 'TransactionLocation', 'LocationChanged']].head())

#Deviation from Usual Transaction Behavior
print("Deviation from Transaction:")
user_stats = transactions_df.groupby('UserID')['TransactionAmount'].agg(['mean', 'std']).reset_index()
user_stats.columns = ['UserID', 'MeanTransactionAmount', 'StdTransactionAmount']
transactions_df = pd.merge(transactions_df, user_stats, on='UserID', how='left')
transactions_df['DeviationFromMean'] = (transactions_df['TransactionAmount'] - transactions_df['MeanTransactionAmount']) / transactions_df['StdTransactionAmount']
print(transactions_df[['UserID', 'TransactionAmount', 'DeviationFromMean']].head())

# final Processed Data
#print("Store data:")
#transactions_df.to_sql('ProcessedTransactions', conn, if_exists='replace', index=False)
print("Success!!!")
