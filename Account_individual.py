"""
Individual Accounts
Each individual account (I.A.) should:
    Create I.A. DB Table:
        Initalize I.A. DB Table
        Link Individual Account DB Table with User's DB Table
        Link Individual Account DB Table with Bank's DB Table
    Document Money Deposits into Individual Account in Inv
    Document Money Withdrawls from Individual Account
    
    
    
    
    
    Be linked with its own database table and the Bank’s table
        When individual accounts are created, their own table is created.
        When individual accounts’ amount is modified, the Bank’s table and its own table will be updated.
    Provide essential account information to user
        Transactions history in the past week/month/quarter
        Total amounts
"""
from User_Account import Account


# class Account_Indiviual provides all functions to a specific account
#     object and their database as attributes.
class Account_Individual():

    # deposit (amount, source) consumes deposit amount and deposit description,
    #       and updates its account_balance and DB attributes.
    # DB: date, description, category, deposit_amount, balance.
    # Time: O(1)
    def deposit(self, amount, source):
        pass

    # withdrawal (amount, source) consumes withdrawal amount and withdrawal description,
    #       and updates its account_balance and DB attributes.
    # withdrawal(amount, source): (ID, name, DB, account_bal), int, source -> (ID, name, DB', account_bal')
    # update record in DB: date, description, category, withdrawal_amount, balance.
    def withdrawal(self, amount, source):
        pass

    # transfer (amount, dest_account_ID) consumes transfer amount and destination account,
    #       and updates both account_balances and DB attributes.
    # transfer(amount, dest_account_ID):
    # (ID, name, DB, account_bal), int, int  -> (ID, name, DB', account_bal') -- self
    # (ID, name, DB, account_bal), int, str -> (ID, name, DB', account_bal') --destination account searched by ID (int)
    # update record in DB: date, description, category, deposit_amount/withdrawal_amount, balance.
    def transfer(self, amount, dest_account_ID):
        pass

    # history (category, length) consumes the category of transactions and the number of days of past transactions that
    #       the user requests, and displays all records in the account DB that satisfies the filtering conditions.
    # history (category, length):(ID, name, DB, account_bal), str, int -> NULL, π
    def history(self, cat, length):
        pass

    # check_bal() returns the current account balance without connecting to DB.
    # check_bal(): (ID, name DB, account_bal) -> account_bal
    def check_bal(self):
        pass

    # verify_amount(amount) consumes an amount for transfer/withdrawal, and verifies if the current account_bal is
    #       sufficient for the transaction.
    # verify_amount(amount): (ID, name, DB, account_bal), amount -> bool
    def verify_amount(self, amount):
        pass

    # create DB and link to parent

    # updates its account_balance and DB attributes --> Deposit

    # report_generate(length) generates an account's summary for the specified duration, using the DB function
    #       DB_report_generate.
    # report_generate(length): (ID, name, DB, account_bal), length -> PDF/docx etc.
    def report_generate(self, length):
        pass
