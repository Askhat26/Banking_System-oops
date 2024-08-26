import sqlite3
from datetime import datetime

def create_connection():
    conn = sqlite3.connect('bank.db')
    return conn

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_number TEXT PRIMARY KEY,
        account_holder TEXT,
        balance REAL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT,
        transaction_type TEXT,
        amount REAL,
        timestamp TEXT,
        FOREIGN KEY (account_number) REFERENCES accounts (account_number)
    )
    ''')
    
    conn.commit()
    conn.close()

class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

        # Check if account already exists
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (self.account_number,))
        account = cursor.fetchone()

        if not account:
            cursor.execute('INSERT INTO accounts (account_number, account_holder, balance) VALUES (?, ?, ?)',
                           (self.account_number, self.account_holder, self.balance))
            conn.commit()
        else:
            self.balance = account[2]  # Set balance if account exists
        conn.close()

    def deposit(self, amount):
        if amount > 0:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE account_number = ?',
                           (amount, self.account_number))
            self.log_transaction(cursor, "Deposit", amount)
            conn.commit()
            conn.close()
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET balance = balance - ? WHERE account_number = ?',
                           (amount, self.account_number))
            self.log_transaction(cursor, "Withdrawal", amount)
            conn.commit()
            conn.close()
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM accounts WHERE account_number = ?', (self.account_number,))
        balance = cursor.fetchone()
        conn.close()
        return balance[0] if balance else 0.0

    def log_transaction(self, cursor, transaction_type, amount):
        cursor.execute('INSERT INTO transactions (account_number, transaction_type, amount, timestamp) VALUES (?, ?, ?, ?)',
                       (self.account_number, transaction_type, amount, datetime.now().isoformat()))

    def print_transaction_history(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT transaction_type, amount, timestamp FROM transactions WHERE account_number = ?',
                       (self.account_number,))
        transactions = cursor.fetchall()
        conn.close()
        
        for transaction in transactions:
            print(f"{transaction[0]}: ${transaction[1]} on {transaction[2]}")

class Bank:
    def __init__(self, name):
        self.name = name
        initialize_database()

    def create_account(self, account_holder, initial_balance=0):
        account_number = self.generate_account_number()
        new_account = BankAccount(account_number, account_holder, initial_balance)
        return account_number

    def generate_account_number(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM accounts')
        count = cursor.fetchone()[0]
        conn.close()
        return str(count + 1000)

    def get_account(self, account_number):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE account_number = ?', (account_number,))
        account_data = cursor.fetchone()
        conn.close()
        
        if account_data:
            return BankAccount(account_data[0], account_data[1], account_data[2])
        return None

    def list_accounts(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()
        conn.close()
        
        for account in accounts:
            print(f"Account Number: {account[0]}, Holder: {account[1]}, Balance: ${account[2]}")

# Example usage
bank = Bank("MyBank")

# Create accounts
acc1 = bank.create_account("Alice", 1000)
acc2 = bank.create_account("Bob", 500)

# Perform operations
account1 = bank.get_account(acc1)
account1.deposit(500)
account1.withdraw(200)

account2 = bank.get_account(acc2)
account2.deposit(1000)
account2.withdraw(300)

# Print account information
bank.list_accounts()

# Print transaction history for an account
print("\nTransaction History for Alice:")
account1.print_transaction_history()
