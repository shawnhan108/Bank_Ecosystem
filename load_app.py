import datetime
import random
from typing import Optional

import mysql.connector

from Bank_Account_Class import UserDB, DBAccount
from general_dbs import IncidentDB, UsersDB, AccountsDB


class App:
    """
    App class is the main instance. It is the intersection of DB RAMs and account/user objects.
    Therefore, all functions that change DB RAMs have to be placed in this class to access dicts.
    """

    def __init__(self):
        """
        __init__: loads incident DB, userDB and AccountsDB in RAM dictionary.
                  loads all DBAccount and UserDB objects and store in accounts_users_dict RAM dictionary.
                  accounts_users_dict: username as key, UserDB object as content
                  Gets the largest transaction number over all transactions.
        """
        self.incident_db = IncidentDB()
        self.users_db = UsersDB()
        self.accounts_db = AccountsDB()
        self.trans_num = 0
        temp_dict = dict()

        for key in self.users_db.users_dict.items():
            # First, load userDB Object and add to accounts_users_dict.
            temp_user = UserDB()
            self.__load_user__(temp_user, key)
            self.__load_user_dict__(temp_user)
            temp_dict[key] = temp_user

            # Find max transaction number.
            max_trans_num_from_user = max(temp_user.trans_dict.keys())
            if max_trans_num_from_user > self.trans_num:
                self.trans_num = max_trans_num_from_user

        self.accounts_users_dict = temp_dict
        self.trans_num += 1  # now this is the next transaction number ready to use.

    def __load_account__(self, account: DBAccount, acc_number: int):
        """
        __load_account__ loads an account's info from accounts_dict in AccountsDB into a BankAccount object
        :param acc_number: the account number of the account to be loaded
        :return: a loaded BankAccount object with account info.
        Category: non-DB function
        """
        # Gets account info from AccountsDB dict.
        info_tuple = self.accounts_db.accounts_dict[acc_number]

        # Load into object
        account.acc_number = acc_number
        account.acc_name = info_tuple[1]
        account.acc_balance = info_tuple[2]
        account.acc_type = info_tuple[3]
        account.acc_table = 'DB_' + str(account.acc_number)

    def __load_user__(self, user: UserDB, username: str):
        """
        __load_user__ loads user info from users_dict in UsersDB into a UserID object.
        :param username: the username of the user to be loaded.
        :return: a loaded UserID object with user info
        Category: non-DB function
        COMMENT: self.accounts and trans_dict dictionaries is not updated. Will be updated in UserDB, load_user_dict.
        """
        # Gets user info from UserDB dict.
        info_tuple = self.users_db.users_dict[username]

        # Load into object
        user.name = info_tuple[0]
        user.accounts = dict()
        user.trans_dict = dict()
        user.age = info_tuple[1]
        user.username = username
        user.password = info_tuple[2]
        user.user_table = 'UserDB_' + user.username

    def __load_user_dict__(self, user: UserDB):
        """
        __load_user_dict__ loads the user's transaction history from user_table to trans_dict
                           loads user's accounts from accounts_dict in AccountsDB to user accounts dict.
        :return: A UserDB that has trans_dict and accounts fields populated.
        Time: O(n) where n is the size of the accounts_dict
        Category: DB function, Load function.
        COMMENT: to fully load a UserDB object, first call __load_user__ then __load_user_dict__.
        """
        # Load trans_dict by first connecting to DB.
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()
        temp_trans_dict = dict()
        mycursor.execute("SELECT * FROM {0};".format(user.user_table))
        data_list = mycursor.fetchall()

        for record in data_list:
            temp_trans_dict[record[0]] = record[1:]

        user.trans_dict = temp_trans_dict
        mycursor.close()

        # Load user accounts dict by searching in accounts_dict
        temp_accounts_dict = dict()
        for key, content in self.accounts_db.accounts_dict.items():

            # if the account belongs to the username in accounts_dict, then load the account object.
            if content[0] == user.username:
                temp_account = DBAccount(self.trans_num)
                self.trans_num += 1
                self.__load_account__(temp_account, key)
                temp_account.__load_account_dict__()
                temp_accounts_dict[key] = temp_account
        user.accounts = temp_accounts_dict

    def __create_new_user__(self):
        """
        __create_new_user__(self): return a User ID, DB and Bank Account with username and password credentials
                                   along with other account details by requesting user info from I/O stream.
                                   returns a user account with username *username* and a respective MySQL database
                                  to store transaction history of all user's accounts
        Side Effect: Create a User ID Instance
                     Prints to I/O
        Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
        """
        user = UserDB()
        user.name = str(input("Name: "))  # Initialize User ID Name
        user.accounts = dict()  # Store Accounts for User ID

        # Request and validate user age
        age = input("Age: ")
        while (not age.isnumeric()) or user.age < 0 or user.age > 125:  # Check User's Age is Valid
            print("Please enter your correct age.")
            user.age = int(input("Age: "))
            self.incident_db.commit_incident(user.name, user.username,
                                             'Unqualified User Account registration due to age out of range.')
        if user.age < 18:
            print("User is too young.")
            age = input("Age: ")

        user.age = int(age)
        self.__username_setup__(user)  # Request Username and verifies its validity
        user.password = '000000'  # initialize temporary password
        user.user_table = 'UserDB_' + user.username
        user.trans_dict = dict()
        user.__password_setup__()  # Request Password and Create Successful Password Setup

        # Create a UserID instance and setup new userID

        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Create New Table in mySQL Database
        mycursor = mydb.cursor()
        create_table_command = 'CREATE TABLE {0} (Transaction_Num int, Date varchar(255), Account int, ' \
                               'Transaction_Description varchar(255), Withdrawals float, Deposits float, ' \
                               'Balance float);'.format(user.user_table)
        mycursor.execute(create_table_command)
        mydb.commit()

        # Generate First History Entry -- Recording UserDB Creation
        first_record_command = 'INSERT INTO {0} (Transaction_Num, Date, Transaction_Description, Withdrawals,' \
                               ' Deposits, Balance) VALUES ({1}, {2}, {3}, {4}, {5}, {6});'.format(
            user.user_table, self.trans_num, str(datetime.date.today()),
            'UserDB ' + user.user_table + ' created', 0.00, 0.00, 0.00)
        mycursor.execute(first_record_command)
        mydb.commit()
        mycursor.close()

        # Update user dictionary attribute
        user.trans_dict[self.trans_num] = (
            str(datetime.date.today()), 'UserDB ' + user.user_table + ' created', 0.00, 0.00, 0.00)
        self.trans_num += 1

        # Update all db tables and dictionaries with new user info
        self.users_db.add_user(user.name, user.age, user.username, user.password)
        self.accounts_users_dict[user.username] = user

        print("Successful UserID Created.")  # Notify User of Successful UserID Creation

    def __username_setup__(self, user: UserDB):
        """
        __username_setup__ requests user's username from I/O stream, verifies its validity, and stores it to the field.
        :param user: the UserDB object to have its username set up
        Side Effect: Mutate UserDB
        Time: O(1)
        """
        valid = False
        while not valid:
            user.username = input('Please enter your username')
            if user.username in self.users_db.users_dict.keys():
                print('The username you have entered is taken.')
            else:
                valid = True

    def __add_account__(self, user: UserDB):
        """
        __add_account__(self): creates a new bank account instance and assigns ownership to the User ID
        Side Effect: Mutates UserID
                     Create a DB Instance
                     Create a Bank Account Instance
                     Updates accounts_table in AccountsDB
                     Print to I/O
        Time: O(1)
        :return: a new bank account instance and assigns ownership to the User ID
        """

        acc_num = random.randint(100000, 999999)

        while acc_num in self.accounts_db.accounts_dict.keys():
            acc_num = random.randint(100000, 999999)

        account_temp = DBAccount(transaction_num=self.trans_num, new_account=True, acc_number=acc_num)

        # Update dictionaries and DBs
        user.accounts[acc_num] = account_temp
        self.accounts_db.add_account(account_temp.acc_number, account_temp.acc_name, account_temp.acc_balance,
                                     account_temp.acc_type, user.username)
        self.trans_num += 1

    def __change_username__(self, user: UserDB):
        """
        __change_username__(self): modifies User ID username, changes all username instances in DB tables,
                                   renames user_table.
        Side Effect: Mutates UserID object
                     Mutates DB table columns, user_table table name.
                     Prints to I/O
        Time: O(n) where n = max(incident_db, Users_db, accounts_db)
        :return: Account object with updated username
        Category/COMMENT: Very expensive DB function because of update_username
        """
        old_username = user.username
        old_tablename = user.user_table
        self.__username_setup__(user)  # Request User for Username
        user.user_table = 'UserDB_' + user.username

        # Commit changes in DB and dicts
        self.incident_db.update_username(old_username, user.username)
        self.users_db.update_username(old_username, user.username)
        self.accounts_db.update_username(old_username, user.username)

        # Also need to change user_table name in database
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()

        # Change table name
        rename_command = "ALTER TABLE {0} RENAME TO {1};".format(old_tablename, user.user_table)
        mycursor.execute(rename_command)
        mydb.commit()
        mycursor.close()

    def __change_password__(self, user: UserDB):
        """
        __change_password__(self): modifies User ID password with the valid password set-up protocol.
        Side Effects: Mutates UserID
                      Print to I/O
        Time: max{O(n * m), O(t)}
              where n is the length of the password and m is the number of attempts to setup a password.
              t is the size of users_table
        :return: Account object with valid new password.
        """
        attempt: int = 0

        # Request old password for security:
        while attempt <= 3:
            if input("Please enter your old password") == user.password:
                break  # successful
            elif attempt == 3:
                return  # exit from procedure due to security
            else:
                attempt += 1

        user.__password_setup__(reset=True)  # Create Successful Password Setup

        # Commit changes in DB and dicts
        self.users_db.update_user(username=user.username, password=user.password)

    def __update_account__(self, acc_num: int, acc_name: Optional[str] = None, acc_bal: Optional[float] = None,
                           acc_type: Optional[str] = None):
        """
        __update_account__ updates an account's info by finding the account object, and updating fields, tables, and DBs
        :param acc_num: Mandatory: account number
        :param acc_name: account name
        :param acc_bal: account balance
        :param acc_type: account type
        :return: Updated account object, dbs and dicts
        COMMENT: Username of account holder will not be updated in this function. If change of username occurs, it will
                 be handled by __change_username__ instead.
        """
        username = self.accounts_db.accounts_dict[acc_num][0]
        if acc_name:
            self.accounts_db.update_account(acc_num, account_name=acc_name)
            self.accounts_users_dict[username].accounts[acc_num].acc_name = acc_name
        if acc_bal:
            self.accounts_db.update_account(acc_num, account_bal=acc_bal)
            self.accounts_users_dict[username].accounts[acc_num].acc_balance = acc_bal
        if acc_type:
            self.accounts_db.update_account(acc_num, account_type=acc_type)
            self.accounts_users_dict[username].accounts[acc_num].acc_type = acc_type

    def __update_user__(self, username: str, name: Optional[str] = None, age: Optional[int] = None,
                        password: Optional[str] = None):
        """
        __update_user__ updates a user's info by finding the user object, and updating fields, tables, and DBs
        :param username: Mandatory: username of the user
        :param name: User's name
        :param age: User's age
        :param password: UserID password
        :return: Updated User object, DBs and dicts
        COMMENT: Username will not be updated in this function. If change of username occurs, it will
                 be handled by __change_username__ instead.
        """
        if name:
            self.users_db.update_user(username, name=name)
            self.accounts_users_dict[username].name = name
        if age:
            self.users_db.update_user(username, age=age)
            self.accounts_users_dict[username].age = age
        if password:
            self.users_db.update_user(username, password=password)
            self.accounts_users_dict[username].password = password
