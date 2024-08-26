# Simple Banking System

## Overview
This project implements a basic banking system using Python and SQLite. It provides functionality for creating bank accounts, making deposits and withdrawals, and tracking transaction history.

## Features
- Create and manage bank accounts
- Deposit and withdraw funds
- View account balances
- Track transaction history
- Persistent data storage using SQLite

## Requirements
- Python 3.x
- SQLite3 (usually comes pre-installed with Python)

## Installation
1. Clone this repository or download the source code.
2. Ensure you have Python 3.x installed on your system.
3. No additional libraries are required as this project uses only built-in Python modules.

## Usage

### Initializing the Bank
```python
from banking_system import Bank

# Create a new bank
bank = Bank("MyBank")

#Creating Accounts
# Create a new account with an initial balance
account_number = bank.create_account("Alice", 1000)

# Create another account
another_account_number = bank.create_account("Bob", 500)

#Performing Transactions
# Get an existing account
account = bank.get_account(account_number)

# Deposit money
account.deposit(500)

# Withdraw money
account.withdraw(200)

# Check balance
balance = account.get_balance()
print(f"Current balance: ${balance}")

#Viewing Transaction History
# Print transaction history for an account
account.print_transaction_history()





Code Structure
Classes

Bank: Manages the overall banking system.
BankAccount: Represents individual bank accounts and handles transactions.

Main Functions

create_connection(): Establishes a connection to the SQLite database.
initialize_database(): Sets up the necessary tables in the database.
BankAccount.deposit(): Adds funds to an account.

BankAccount.withdraw(): Removes funds from an account.
BankAccount.get_balance(): Retrieves the current balance of an account.
BankAccount.print_transaction_history(): Displays the transaction history of an account.
Bank.create_account(): Creates a new bank account.
Bank.get_account(): Retrieves an existing account.
Bank.list_accounts(): Displays information for all accounts.

Database Schema
Tables
accounts: Stores account information.

Columns: account_number (TEXT, PRIMARY KEY), account_holder (TEXT), balance (REAL)


transactions: Logs all transactions.

Columns: id (INTEGER, PRIMARY KEY), account_number (TEXT, FOREIGN KEY), transaction_type (TEXT), amount (REAL), timestamp (TEXT)
