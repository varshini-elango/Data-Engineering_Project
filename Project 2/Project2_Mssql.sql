create database Project2

CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    UserName VARCHAR(255),
    Email VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Address VARCHAR(255),
    AccountCreatedDate DATETIME
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    TransactionAmount DECIMAL(18, 2),
    TransactionLocation VARCHAR(255),
    TransactionTime DATETIME,
    PaymentMethod VARCHAR(50),
    TransactionStatus VARCHAR(50), -- e.g., "Completed", "Pending"
    FraudLabel BIT DEFAULT 0 -- 0: Not Fraud, 1: Fraud
);

CREATE TABLE FraudLabels (
    LabelID INT PRIMARY KEY,
    TransactionID INT FOREIGN KEY REFERENCES Transactions(TransactionID),
    FraudReason VARCHAR(255),
    DateLabeled DATETIME
);

INSERT INTO Users (UserID, UserName, Email, PhoneNumber, Address, AccountCreatedDate)
VALUES 
(1, 'Alice Johnson', 'alice@example.com', '123-456-7890', '123 Maple St', '2023-01-15 08:30:00'),
(2, 'Bob Smith', 'bob@example.com', '098-765-4321', '456 Oak St', '2022-11-20 10:00:00'),
(3, 'Charlie Brown', 'charlie@example.com', '555-555-5555', '789 Pine St', '2023-06-01 09:45:00'),
(4, 'David Green', 'david@example.com', '222-333-4444', '101 Birch St', '2022-09-15 10:00:00'),
(5, 'Emily White', 'emily@example.com', '333-444-5555', '202 Cedar St', '2023-02-05 11:30:00'),
(6, 'Frank Lee', 'frank@example.com', '444-555-6666', '303 Walnut St', '2022-12-25 16:00:00'),
(7, 'Grace Kim', 'grace@example.com', '555-666-7777', '404 Ash St', '2023-03-18 14:20:00');

INSERT INTO Transactions (TransactionID, UserID, TransactionAmount, TransactionLocation, TransactionTime, PaymentMethod, TransactionStatus, FraudLabel)
VALUES 
(1001, 1, 200.50, 'New York', '2023-09-01 12:30:00', 'Credit Card', 'Completed', 0),
(1002, 1, 5000.00, 'Los Angeles', '2023-09-02 13:15:00', 'Debit Card', 'Completed', 1),
(1003, 2, 150.00, 'San Francisco', '2023-09-03 15:45:00', 'PayPal', 'Pending', 0),
(1004, 3, 750.00, 'Chicago', '2023-09-04 18:00:00', 'Credit Card', 'Completed', 1),
(1005, 2, 80.00, 'Miami', '2023-09-05 09:20:00', 'Debit Card', 'Completed', 0),
(1006, 4, 350.00, 'Houston', '2023-09-05 11:30:00', 'Credit Card', 'Completed', 0),
(1007, 4, 12000.00, 'Dallas', '2023-09-06 12:00:00', 'Credit Card', 'Completed', 1),
(1008, 5, 100.00, 'Boston', '2023-09-06 14:45:00', 'Debit Card', 'Completed', 0),
(1009, 6, 250.00, 'New York', '2023-09-07 15:30:00', 'PayPal', 'Pending', 0),
(1010, 7, 650.00, 'Chicago', '2023-09-08 16:00:00', 'Credit Card', 'Completed', 1),
(1011, 6, 5400.00, 'San Diego', '2023-09-09 17:00:00', 'Debit Card', 'Completed', 1),
(1012, 5, 175.00, 'Seattle', '2023-09-10 18:30:00', 'Credit Card', 'Completed', 0);

INSERT INTO FraudLabels (LabelID, TransactionID, FraudReason, DateLabeled)
VALUES 
(1, 1002, 'Suspiciously High Amount', '2023-09-02 14:00:00'),
(2, 1004, 'Unusual Location', '2023-09-04 19:00:00'),
(3, 1007, 'Unusually High Amount', '2023-09-06 12:30:00'),
(4, 1010, 'Transaction in Uncommon Location', '2023-09-08 16:30:00'),
(5, 1011, 'Multiple Large Transactions in Short Time', '2023-09-09 17:30:00');

select * from Users
select * from Transactions
select * from FraudLabels


--average transaction amount and the total no. of transactions 
SELECT T.UserID, U.UserName, 
COUNT(T.TransactionID) AS TotalTransactions, 
AVG(T.TransactionAmount) AS AvgTransactionAmount
FROM Transactions T
JOIN Users U ON T.UserID = U.UserID
GROUP BY T.UserID, U.UserName;

--transactions that exceed a certain threshold
SELECT T.TransactionID, U.UserName, T.TransactionAmount, T.TransactionLocation, 
T.TransactionTime
FROM Transactions T
JOIN Users U ON T.UserID = U.UserID
WHERE T.TransactionAmount > 5000 -- Example threshold
AND T.FraudLabel = 1;

--Calculating Metrics
SELECT COUNT(CASE WHEN T.FraudLabel = 1 THEN 1 END) * 100.0 / COUNT(*) AS FraudPercentage,
AVG(T.TransactionAmount) AS AvgTransactionAmount
FROM Transactions T;
