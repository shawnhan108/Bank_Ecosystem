import datetime
import random
from typing import Optional

import mysql.connector

import main
from general_dbs import IncidentDB


class BankAccount:

    def __init__(self, acc_number: int = 0):
        """
        __init__(self, acc_num): return a new, basic account object whose account number is *acc_num*, account name is
                                 *acc_name* starting balance is *acc_balance* and account type is *acc_type*.
        Side Effects: Creates a Bank Account Instance
                    Prints to I/O
        Time: O(1)
        COMMENT: acc_number and acc_table should be updated once BankAccount is used.
        :param acc_number: Account Number, int.
        """

        # Initialize Account Details
        self.acc_number = acc_number
        self.acc_name = str(input("Please enter account name:"))  # Account Name
        self.acc_balance = 0.0  # Account Balance
        self.acc_type = str(input("Please enter account type (Personal, Family, or Savings): "))  # Account Type
        self.acc_table = 'DB_' + str(self.acc_number)  # Account DB Table Name
        self.acc_dict = dict()  # Initiate account dictionary

        print("Class Successfully Created.")

    def load_account_from_db(self):
        pass


class DBAccount(BankAccount):

    def __init__(self, transaction_num: int, acc_number: int = 0):
        """
        __init__(self, acc_num): returns a new,basic account object with account number *acc_num* and a respective MySQL
                                 database to store transaction history.
        Side Effects: Create a DB Instance
                      Create a Bank Account Instance
                      Prints to I/O
        Time: O(1)
        :param acc_number: Account Number, int.
        """

        # Create a Bank Account Instance
        BankAccount.__init__(self, acc_number)

        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Create New Table in mySQL Database
        mycursor = mydb.cursor()
        create_table_command = 'CREATE TABLE {0} (Transaction_Num int, Date varchar(255), Transaction_Description ' \
                               'varchar(255), Withdrawals float, Deposits float, Balance float);'.format(self.acc_table)
        mycursor.execute(create_table_command)
        mydb.commit()

        # Generate First History Entry -- Recording Account Creation
        first_record_command = 'INSERT INTO {0} (Transaction_Num, Date, Transaction_Description, Withdrawals, Deposits,' \
                               'Balance) VALUES ({1}, {2}, {3}, {4}, {5}, {6});'.format(self.acc_table,
                                                                                        transaction_num,
                                                                                        str(datetime.date.today()),
                                                                                        'Account ' + str(
                                                                                            self.acc_number) +
                                                                                        ' Created', 0.00, 0.00, 0.00)
        mycursor.execute(first_record_command)
        mydb.commit()
        mycursor.close()

        # Update account dictionary attribute as well
        self.acc_dict[transaction_num] = (str(datetime.date.today()), 'Account ' + str(self.acc_number) + ' Created',
                                          0.00, 0.00, 0.00)

    def commit_account_db(self, transaction_num: int, trans_description: str, withdrawal: float, deposits: float):
        """
        commit_account_db updates the account's DB with the new transaction information.
        :param trans_description: str
        :param withdrawal: float
        :param deposits: float
        :return: Updated account's DB with new transaction record
        Side Effects: Updated the account's DB
        Time: O(1)
        COMMENT: commit_account_db must be called after the self.acc_balance field is updated with the new transaction.
                 commit_account_db should be called with commit_user_db so that both tables are updated.
        """

        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate a transaction record into the userDB table.
        mycursor = mydb.cursor()
        record_command = 'INSERT INTO {0} (Transaction_Num, Date, Transaction_Description, Withdrawals, Deposits, ' \
                         'Balance) VALUES ({1}, {2}, {3}, {4}, {5}, {6});'.format(self.acc_table, transaction_num,
                                                                                  str(datetime.date.today()),
                                                                                  trans_description, withdrawal,
                                                                                  deposits, self.acc_balance)
        mycursor.execute(record_command)
        mydb.commit()
        mycursor.close()

        # Update account dictionary attribute as well
        self.acc_dict[transaction_num] = (str(datetime.date.today()), trans_description, withdrawal, deposits,
                                          self.acc_balance)


class UserID:
    # name: str
    # accounts: dict
    # age: int
    # username: str
    # password: str

    def __init__(self):
        """
        __init__(self): return a User ID, DB and Bank Account with username and password credentials along with other
                        account details
        Side Effect: Create a User ID Instance
                     Prints to I/O
        Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
        """

        self.name = str(input("Name: "))  # Initialize User ID Name
        self.accounts = dict()  # Store Accounts for User ID

        age = input("Age: ")  # Request User Age

        while (not age.isnumeric()) or self.age < 0 or self.age > 125:  # Check User's Age is Valid
            print("Please enter your correct age.")
            self.age = int(input("Age: "))

            IncidentDB.commit_incident(main.Load.incident_db, self.name, self.username,
                                       'Unqualified User Account registration due to age out of range.')
        if self.age < 18:
            print("User is too young.")
            age = input("Age: ")

        self.age = int(age)
        self.username = str(input("Please enter your username: "))  # Request Username
        self.password = '000000'  # initialize temporary password
        self.__password_setup__()  # Request Password and Create Successful Password Setup

        print("Successful Account Created.")  # Notify User of Successful Account Creation

    def __is_valid_Pass__(self):
        """
        __is_valid_Pass_(self): checks if a string meets the acceptance criteria for a password.
        Time: O(n) -> Θ(4n), where n is the length of the string.
        :return: boolean indicating if the password is valid.
        """

        special_chars = ("[", "@", "_", "!", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?", "/", "\\", "|", "}",
                         "{", "~", ":", "]", '"')  # Tuple of Characters Considered as Special Characters
        password = self.password  # the password string to be examined.

        if (any(i.isupper() for i in password) and  # Check if Password Contains a Uppercase Character
                any(i.islower() for i in password) and  # Check if Password Contains a Lowercase Character
                any(i.isdigit() for i in password) and  # Check if Password Contains a Numerical Digit Character
                any(i in special_chars for i in password) and  # Check if Password Contains a Special Character
                len(password) >= 6):  # Check if Password is Minimum 6 Characters Length
            return True
        else:
            return False

    def __password_setup__(self, reset: Optional[bool] = False):
        """
        __password_setup__(self): maintains the process to successful password setup for a User ID.
        Side Effects: Mutates UserID
                      Print to I/O
        Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
        :return: object with qualified password
        """

        while True:  # Request New Password Till Successful Completion of User ID Password Set-up
            while not self.__is_valid_Pass__:  # Check if User ID Password is Valid
                # Print Valid Password Acceptance Criteria
                print("Please make sure you're password has at least:\n")
                print("1) At least one upper case character;\n")
                print("2) At least one lower case character;\n")
                print("3) At least one numerical digit character;\n")
                print("4) At least one special character; and\n")
                print("5) Minimum 6 characters.")

                if reset:
                    self.password = input("Please enter your new password: ")
                else:
                    self.password = input("Please enter your password: ")  # Request User ID Password

            check_password: str = input("Please re-enter your password: ")  # Request Password Confirmation

            if check_password == self.password:  # Acceptance Criteria
                break  # Successful Password Setup
            else:
                self.password = "0"  # Automatic Password Failure to Reset Password Set-Up Process

    def __change_password__(self):
        """
        __change_password__(self): modifies User ID password with the valid password set-up protocol.
        Side Effects: Mutates UserID
                      Print to I/O
        Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
        :return: Account object with valid new password.
        """
        attempt: int = 0

        # Request old password for security:
        while attempt <= 3:
            if input("Please enter your old password") == self.password:
                break  # successful
            elif attempt == 3:
                return  # exit from procedure due to security
            else:
                attempt += 1

        self.__password_setup__()  # Create Successful Password Setup

    def __change_username__(self):
        """
        __change_username__(self): modifies User ID username.
        Side Effect: Mutates UserID
                     Prints to I/O
        Time: O(1)
        :return: Account object with updated username
        """

        self.username = input("Please enter your username: ")  # Request User for Username

    def __add_account__(self):
        """
        __add_account__(self): creates a new bank account instance and assigns ownership to the User ID
        Side Effect: Mutates UserID
                     Create a DB Instance
                     Create a Bank Account Instance
                     Print to I/O
        Time: O(1)
        :return: a new bank account instance and assigns ownership to the User ID
        """

        acc_num = random.randint(100000, 999999)

        while acc_num in self.accounts:
            acc_num = random.randint(100000, 999999)

        account_temp = DBAccount.__init__(acc_num)

        self.accounts[acc_num] = account_temp


class UserDB(UserID):

    def __init__(self):
        """
        __init__(self, username): returns a user account with username *username* and a respective MySQL database
                                  to store transaction history of all user's accounts
        Side Effects: Create a UserDB Instance
                      Create a UserID Instance
                      Prints to I/O
        Time: O(1)
        COMMENT: After each transaction, UserDB table should be updated along with the account's DB table.
        """

        self.user_table = 'UserDB_' + self.username

        # Create a UserID instance
        UserID.__init__(self)

        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Create New Table in mySQL Database
        mycursor = mydb.cursor()
        create_table_command = 'CREATE TABLE {0} (Date varchar(255), Account int, Transaction_Description varchar(255), ' \
                               'Withdrawals float, Deposits float, Balance float);'.format(self.user_table)
        mycursor.execute(create_table_command)
        mydb.commit()

        # Generate First History Entry -- Recording UserDB Creation
        first_record_command = 'INSERT INTO {0} (Date, Transaction_Description, Withdrawals, Deposits, Balance) VALUES' \
                               '({1}, {2}, {3}, {4}, {5});'.format(self.user_table, str(datetime.date.today()),
                                                                   'UserDB ' + self.user_table + ' created',
                                                                   0.00, 0.00, 0.00)
        mycursor.execute(first_record_command)
        mydb.commit()

        mycursor.close()

    def commit_user_db(self, transaction_description: str, account: int, withdrawal: float, deposits: float,
                       balance: float):
        """
        commit_user_db updates the UserDB with the new transaction information.
        :param transaction_description: str
        :param account: int
        :param withdrawal: float
        :param deposits: float
        :param balance: account's new balance, float.
        :return: Updated UserDB with new transaction record
        Side Effects: Updated the userID instance
        Time: O(1)
        COMMENT: commit_user_db should be called with commit_account_db so that both tables are updated.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate a transaction record into the userDB table.
        mycursor = mydb.cursor()
        record_command = 'INSERT INTO {0} (Date, Account, Transaction_Description, Withdrawals, Deposits, Balance) ' \
                         'VALUES ({1}, {2}, {3}, {4}, {5});'.format(self.user_table, str(datetime.date.today()),
                                                                    account, transaction_description, withdrawal,
                                                                    deposits, balance)
        mycursor.execute(record_command)
        mydb.commit()
        mycursor.close()

    def __deposit__(self, acc_num: int, source: str, amount: float):
        """
        __deposit__: consumes deposit description and amount, and updates its balance,
                     logs in the account's DB table.
        :param source: deposit description.
        :param amount: the amount of transaction.
        :return: updated account's DB table.
        Side Effect: Print to I/O (asks for destination)
        Time: O(1)
        """
        target_account = self.accounts[acc_num]

        # update account balance
        target_account.acc_balance += amount

        # update both account DB and UserDB.
        target_account.commit_account_db(source, 0.00, amount)
        self.commit_user_db(source, acc_num, 0.00, amount, target_account.acc_balance)

        print("Successful Deposit to Account Number {0}, {1}".format(target_account.acc_name, source))
        print("Account Balance", target_account.acc_balance)

    def __withdrawal__(self, acc_num: int, source: str, amount: float):
        """
        __withdrawal__: consumes withdrawal description and amount, and updates its balance,
                        logs in the account's DB table.
        :param source: withdrawal description.
        :param amount: the amount of transaction.
        :return: updated account's DB table.
        Side Effect: Print to I/O (asks for destination)
        Time: O(1)
        """
        target_account = self.accounts[acc_num]

        # update account balance, checks if account balance to determine if transaction is valid.
        target_account.acc_balance -= amount
        if target_account.acc_balance < 0.00:
            print("Insufficient Funds to Complete Transaction")
            target_account.acc_balance += amount
            return

        # update both account DB and UserDB.
        target_account.commit_account_db(source, amount, 0.00)
        self.commit_user_db(source, acc_num, amount, 0.00, target_account.acc_balance)

        print("Successful Withdrawal to Account Number {0}, {1}".format(target_account.acc_name, source))
        print("Account Balance", target_account.acc_balance)

    def __print_User_Details__(self):
        """
        __print_User_Details__(self): prints User ID and it's bank accounts detail.
        Side Effect: Print to I/O
        Time: O(1)
        :return: void
        """
        pass

    def __transfer__(self):
        """
        __transfer__(self): withdraws money from one account and deposits it to another.
        Side Effect: Print to I/O
        Time: O(1)
        :return: updated objects after transfer.
        """
        pass
