import datetime
from typing import Optional

import mysql.connector


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
        self.acc_name = None  # Account Name
        self.acc_balance = 0.0  # Account Balance
        self.acc_type = None  # Account Type
        self.acc_table = 'DB_' + str(self.acc_number)  # Account DB Table Name
        self.acc_dict = dict()  # Initiate account dictionary

        print("Class Successfully Created.")

    def __create_new_account__(self, acc_number: int):
        """
        __create_new_account__ requests for user's info and stores the info into a BankAccount object.
        Side Effects: Creates a Bank Account Instance by requesting info from I/O stream
        :param acc_number: The new account's account number.
        Time: O(1)
        """
        # Initialize Account Details
        self.acc_number = acc_number
        self.acc_name = str(input("Please enter account name:"))  # Account Name
        self.acc_balance = 0.0  # Account Balance
        self.acc_type = str(input("Please enter account type (Personal, Family, or Savings): "))  # Account Type
        self.acc_table = 'DB_' + str(self.acc_number)  # Account DB Table Name
        self.acc_dict = dict()  # Initiate account dictionary

        print("New Account Successfully Created.")


class DBAccount(BankAccount):

    def __init__(self, transaction_num: int, new_account: Optional[bool] = False, acc_number: int = 0):
        """
        __init__(self, acc_num): returns a new,basic account object with account number *acc_num* and a respective MySQL
                                 database to store transaction history.
        Side Effects: Create a DB Instance
                      Create a Bank Account Instance
                      Prints to I/O
        Time: O(1)
        :param transaction_num: newest transaction number.
        :param acc_number: Account Number, int.
        :param new_account: boolean -- if the account represented by acc_number is a new account.
        COMMENT: since new DB table only needs to be generated for new accounts, we have to specify if the function is
                 applied to new account.
                 Need to increment trans_num in main by 1 after using the function.
        """

        if new_account:

            # Create a Bank Account Instance and setup new BankAccount
            BankAccount.__create_new_account__(BankAccount.__init__(self, acc_number), acc_number)

            # Connect to mySQL Database
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                           database="Bank_Ecosystem_DB")

            # Create New Table in mySQL Database
            mycursor = mydb.cursor()
            create_table_command = 'CREATE TABLE {0} (Transaction_Num int, Date varchar(255), Transaction_Description' \
                                   ' varchar(255), Withdrawals float, Deposits float, Balance float);'.format(
                self.acc_table)
            mycursor.execute(create_table_command)
            mydb.commit()

            # Generate First History Entry -- Recording Account Creation
            first_record_command = 'INSERT INTO {0} (Transaction_Num, Date, Transaction_Description, Withdrawals, ' \
                                   'Deposits, Balance) VALUES ({1}, {2}, {3}, {4}, {5}, {6});'.format(
                self.acc_table, transaction_num, str(datetime.date.today()),
                'Account ' + str(self.acc_number) + ' Created', 0.00, 0.00, 0.00)
            mycursor.execute(first_record_command)
            mydb.commit()
            mycursor.close()

            # Update account dictionary attribute as well
            self.acc_dict[transaction_num] = (
                str(datetime.date.today()), 'Account ' + str(self.acc_number) + ' Created',
                0.00, 0.00, 0.00)

        else:
            # Create a Bank Account Instance
            BankAccount.__init__(self, acc_number)

    def __load_account_dict__(self):
        """
        __load_account_dict__ loads the account's transaction history from acc_table to acc_dict
        :return: a DBAccount object with populated acc_dict.
        Category: DB Function, Load function.
        COMMENT: to fully load an BankAccount object, first call __load_account__ then call __load_account_dict__.
        """
        # Load account dict by first connecting to DB.
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()
        temp_dict = dict()
        mycursor.execute("SELECT * FROM {0};".format(self.acc_table))
        data_list = mycursor.fetchall()

        for record in data_list:
            temp_dict[record[0]] = record[1:]

        self.accounts_dict = temp_dict
        mycursor.close()

    def commit_account_db(self, transaction_num: int, trans_description: str, withdrawal: float, deposits: float):
        """
        commit_account_db updates the account's DB with the new transaction information.
        :param transaction_num: newest transaction number
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

        # will not update trans_num in main here. It will be updated in commit_user_db function.


class UserID:
    # name: str
    # accounts: dict
    # age: int
    # username: str
    # password: str

    def __init__(self):
        """
        __init__: return a new, empty UserID object.
        Side Effects: Creates a new UserID object.
        Time: O(1)
        COMMENT: user_table should be populated/updated once UserID is used.
        """

        # initialize fields for user details
        self.name = ''
        self.accounts = dict()
        self.age = -1
        self.username = ''
        self.password = ''
        self.user_table = ''
        self.trans_dict = dict()

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
        :return: object with qualified password; password string
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


class UserDB(UserID):

    def __init__(self):
        """
        __init__(self): returns a new UserID = UsesDB instance.
        Side Effects: Create a UserDB Instance
                      Create a UserID Instance
                      Prints to I/O
        Time: O(1)
        COMMENT: After each transaction, UserDB table should be updated along with the account's DB table.
                 Since new DB table only needs to be generated for new users, we have to specify if the function is
                 applied to new user.
        """
        # Create a UserID instance
        UserID.__init__(self)

    def commit_user_db(self, transaction_num: int, transaction_description: str, account_num: int, withdrawal: float,
                       deposits: float, balance: float):
        """
        commit_user_db updates the UserDB with the new transaction information.
        :param transaction_num: newest transaction number.
        :param transaction_description: str
        :param account_num: int
        :param withdrawal: float
        :param deposits: float
        :param balance: account's new balance, float.
        :return: Updated UserDB with new transaction record
        Side Effects: Updated the userID instance
        Time: O(1)
        COMMENT: commit_user_db should be called with commit_account_db so that both tables are updated.
                 need to increment trans_num by 1 in main.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate a transaction record into the userDB table.
        mycursor = mydb.cursor()
        record_command = 'INSERT INTO {0} (Transaction_Num, Date, Account, Transaction_Description, Withdrawals, ' \
                         'Deposits, Balance) VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7});'.format(
            self.user_table, transaction_num, str(datetime.date.today()), account_num, transaction_description,
            withdrawal, deposits, balance)
        mycursor.execute(record_command)
        mydb.commit()
        mycursor.close()

        # Update trans_dict attribute as well
        self.trans_dict[transaction_num] = (str(datetime.date.today()), transaction_description, withdrawal,
                                            deposits, balance)

    def __deposit__(self, transaction_num: int, acc_num: int, source: str, amount: float):
        """
        __deposit__: consumes deposit description and amount, and updates its balance,
                     logs in the account's DB table.
        :param transaction_num: newest transaction number
        :param source: deposit description.
        :param amount: the amount of transaction.
        :return: updated account's DB table.
        Side Effect: Print to I/O (asks for destination)
        Time: O(1)
        COMMENT: need to increment trans_num by 1 in main.
        """
        target_account = self.accounts[acc_num]

        # update account balance
        target_account.acc_balance += amount

        # update both account DBs and dictionaries.
        target_account.commit_account_db(transaction_num, source, 0.00, amount)
        self.commit_user_db(transaction_num, source, acc_num, 0.00, amount, target_account.acc_balance)

        print("Successful Deposit to Account Number {0}, {1}".format(target_account.acc_name, source))
        print("Account Balance", target_account.acc_balance)

    def __withdrawal__(self, transaction_num: int, acc_num: int, source: str, amount: float):
        """
        __withdrawal__: consumes withdrawal description and amount, and updates its balance,
                        logs in the account's DB table.
        :param transaction_num: newest transaction number
        :param source: withdrawal description.
        :param amount: the amount of transaction.
        :return: updated account's DB table.
        Side Effect: Print to I/O (asks for destination)
        Time: O(1)
        COMMENT: need to increment trans_num by 1 in main.
        """
        target_account = self.accounts[acc_num]

        # update account balance, checks if account balance to determine if transaction is valid.
        target_account.acc_balance -= amount
        if target_account.acc_balance < 0.00:
            print("Insufficient Funds to Complete Transaction")
            target_account.acc_balance += amount
            return

        # update both account DB and UserDB.
        target_account.commit_account_db(transaction_num, source, amount, 0.00)
        self.commit_user_db(transaction_num, source, acc_num, amount, 0.00, target_account.acc_balance)

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
