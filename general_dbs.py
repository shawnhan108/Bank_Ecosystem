import datetime
import mysql.connector
from typing import Optional


class IncidentDB:

    def __init__(self):
        """
        __init__(self): creates an incidentDB object and update the incident_num attribute.
                        retrieves incident records from incident_table, and stores it in a dictionary in RAM for faster
                        use. That is, copies database into dict.
        Side Effects: creates an incidentDB object; Creates incident dict.
        Time: O(n) where n is the size of the table.
        COMMENT: The incident dictionary has incident number as key, and other columns stored as tuple in contents.
                 when starting the program, dict and incident_table are both up to date.
                 when committing changes to database, Dict should be updated simultaneously as well.
                 Also include sync database to sync RAM to database when database is temporarily unavailable.
        Category: Load Function, Database Function.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # to get the next incident_num to be used
        mycursor = mydb.cursor()
        mycursor.execute("SELECT MAX(Incident_num) FROM incident_table;")
        self.incident_num = mycursor.fetchone()[0] + 1

        # retrieve data from incident_table and store in dictionary.
        out_dict = dict()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM incident_table;")
        data_list = mycursor.fetchall()

        for record in data_list:
            out_dict[record[0]] = record[1:]

        self.incident_dict = out_dict

        mycursor.close()

    def reconstruct_incident_db(self):
        """
        reconstruct_incident_db(self): Removes the old incident table, and creates a new incident table that collects
                                        all account incidents from all user's accounts.
        Side Effects: Remove old incident_table, and create an incident DB table
                      Prints to I/O
        Time: O(1)
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Remove the old table
        mycursor = mydb.cursor()
        remove_command = 'DROP TABLE incident_table;'
        mycursor.execute(remove_command)
        mydb.commit()

        # Create a new incident table in mySQL database
        create_table_command = 'CREATE TABLE {0} (Incident_num int, Date varchar(255), User_name varchar(255), ' \
                               'Username varchar(255), Account int, Incident_Description varchar(255), Status' \
                               ' varchar(255));'.format('incident_table')

        mycursor.execute(create_table_command)
        mydb.commit()
        mycursor.close()

        self.incident_num = 1
        self.incident_dict = dict()

        print('New incident table successfully created.')

    def commit_incident(self, user_name: str, username: str, incident_description: str,
                        account_num: Optional[int] = None):
        """
        commit_incident: creates a record in incident_table that records the incident.
                         add a key-content in incident dict that records the incident.
        :param user_name: the user's name
        :param username:  the Username of UserID
        :param account_num: optional. The account related to the incident.
        :param incident_description: The description of the incident.
        :return: an updated incident table with updated incident_dict.
        Side Effects: Update incident table; Update incident dict
        Time: O(1)
        COMMENT: if "SELECT MAX(Incident_num) FROM incident_table" command is used, the runtime without SQL index
                 will be O(n), and with index will be O(log n). That is, every time the program restarts, at least a
                  O(log n) process is necessary to find the updated incident_num using the command.
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate the incident record into incident_table
        mycursor = mydb.cursor()

        if account_num:
            commit_command = 'INSERT INTO {0}(Incident_num, Date, User_name, Username, Account, Incident_Description, ' \
                             'Status) VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7});'.format('incident_table',
                                                                                          self.incident_num,
                                                                                          str(datetime.date.today()),
                                                                                          user_name, username,
                                                                                          account_num,
                                                                                          incident_description,
                                                                                          'Unresolved')
        else:
            commit_command = 'INSERT INTO {0}(Incident_num, Date, User_name, Username, Account, Incident_Description, ' \
                             'Status) VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7});'.format('incident_table',
                                                                                          self.incident_num,
                                                                                          str(datetime.date.today()),
                                                                                          user_name, username, 'NULL',
                                                                                          incident_description,
                                                                                          'Unresolved')
        mycursor.execute(commit_command)
        mydb.commit()

        mycursor.close()

        # add key to the dictionary as well
        if account_num:
            self.incident_dict[self.incident_num] = (
                str(datetime.date.today()), user_name, username, account_num, incident_description, 'Unresolved')
        else:
            self.incident_dict[self.incident_num] = (
                str(datetime.date.today()), user_name, username, 'NULL', incident_description, 'Unresolved')

        self.incident_num += 1

    def delete_incident(self, incident_num):
        """
        delete_incident removes the record of that incident from the table.
        :param incident_num: the incident number indicating the record to be deleted.
        :return: an updated incident table and incident dict
        Side Effects: Update incident table and incident dict
        Time: O(n), or using index can be optimized to O(log n)
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Delete the record in incident_table
        mycursor = mydb.cursor()
        delete_command = 'DELETE FROM incident_table WHERE Incident_num={0}'.format(incident_num)
        mycursor.execute(delete_command)
        mydb.commit()
        mycursor.close()

        # delete key from the dictionary as well
        del self.incident_dict[incident_num]

    def update_incident(self, incident_num, user_name: Optional[str] = None, username: Optional[str] = None,
                        incident_description: Optional[str] = None, account_num: Optional[int] = None,
                        status: Optional[str] = None):
        """
        update_incident updates the incident record info in both incident_table and incident_dict.
        :param incident_num: mandatory. The incident number of the record that is being updated.
        :param user_name: Updated User's Name
        :param username: Updated Username
        :param incident_description: Updated incident description
        :param account_num: updated account number
        :param status: updated status, usually changes from Unresolved to resolved.
        :return: Updated incident table and incident dict.
        Side Effects: Updated incident table and incident dict.
        Time: O(1)
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()

        if user_name:
            # Update database
            update_command = "UPDATE incident_table SET User_name = '{0}' WHERE Incident_num = {1};".format(user_name,
                                                                                                            incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = (original_record[0],) + (user_name,) + original_record[2:]

        if username:
            # Update database
            update_command = "UPDATE incident_table SET Username = '{0}' WHERE Incident_num = {1};".format(username,
                                                                                                           incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:2] + (username,) + original_record[3:]

        if incident_description:
            # Update database
            update_command = "UPDATE incident_table SET Incident_Description = '{0}' WHERE Incident_num = {1};".format(
                incident_description, incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:4] + (incident_description,) + original_record[5:]

        if account_num:
            # Update database
            update_command = "UPDATE incident_table SET Account = '{0}' WHERE Incident_num = {1};".format(
                account_num, incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:3] + (account_num,) + original_record[4:]

        if status:
            # Update database
            update_command = "UPDATE incident_table SET Status = '{0}' WHERE Incident_num = {1};".format(
                status, incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:5] + (status,)

        mycursor.close()

    def update_username(self, old_username: str, new_username: str):
        """
        Updates incident_db and its corresponding dict/RAM instances.
        :param old_username: original username
        :param new_username: new username
        :return: Updated dbs.
        Time: O(n) where n = size of incident_db
        COMMENT: expensive DB function.
        """
        #  First connect to DB
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()

        #  Update incident_db
        update_command = "UPDATE incident_table SET Username = '{0}' WHERE Username = {1};".format(new_username,
                                                                                                   old_username)
        mycursor.execute(update_command)
        mydb.commit()
        mycursor.close()

        #  Update incident_dict
        for key, content in self.incident_dict.items():
            if content[2] == old_username:
                self.incident_dict[key] = content[:2] + (new_username,) + content[3:]


class UsersDB:
    def __init__(self):
        """
        __init__(self): creates an UsersDB object and update the accounts_num attribute.
                        retrieves users records from users_table, and stores it in a dictionary in RAM for faster
                        use. That is, copies database into dict.
        Side Effects: creates an UsersDB object; Creates users dict.
        Time: O(n), where n is the size of users_table.
        COMMENT: The Users dictionary has username as key, and other columns stored as tuple in contents.
                 when starting the program, dict and users_table are both up to date.
                 when committing changes to database, dict should be updated simultaneously as well.
                 Also include sync database to sync RAM to database when database is temporarily unavailable.
        Category: Load Function, Database Function.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # retrieve data from users_table and store in dictionary.
        out_dict = dict()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users_table;")
        data_list = mycursor.fetchall()

        for record in data_list:
            out_dict[record[2]] = record[:2] + (record[3],)
        self.users_dict = out_dict

        mycursor.close()

    def reconstruct_users_db(self):
        """
        reconstruct_users_db(self): Removes the old users_table and creates a new users_table that has all users' info.
        Side Effects: Remove old users_table, and create a new, empty users_table
                      Prints to I/O
        Time: O(1)
        :return: Truncated users_table
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Remove the old table
        mycursor = mydb.cursor()
        remove_command = 'DROP TABLE users_table;'
        mycursor.execute(remove_command)
        mydb.commit()

        # Create a new accounts_table in mySQL database
        create_table_command = 'CREATE TABLE {0} (Name varchar(255), Age int, Username varchar(255),' \
                               ' Password varchar(255));'.format('users_table')

        mycursor.execute(create_table_command)
        mydb.commit()
        mycursor.close()

        self.users_dict = dict()

        print('New users_table successfully created.')

    def add_user(self, name: str, age: int, username: str, password: str):
        """
        add_user: creates a record in users_table that records the new registered user.
                     add a key-content in accounts dict that records the new user.
        :param name: name of user
        :param age: age of user
        :param username: username of user
        :param password: password of user
        :return: an updated users_table with updated users dict
        Side Effects: Update users table; update users dict
        Time: O(1)
        Category: DB Function
        COMMENT: cannot pass in a UserID object because of circular import.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate the new user record into users_table
        mycursor = mydb.cursor()
        commit_command = 'INSERT INTO {0} (Name, Age, Username, Password) VALUES ({1}, {2}, {3}, {4});'.format(
            'users_table', name, age, username, password)
        mycursor.execute(commit_command)
        mydb.commit()

        mycursor.close()

        # add key to dictionary
        self.users_dict[username] = (name, age, password)

    def delete_user(self, username: int):
        """
        delete_user removes the record of that user from the table.
        :param username: the username of the user to be deleted.
        :return: an updated user table and user dict
        Side Effects: Update user table and user dict
        Time: O(n), or use index can be optimized to O(log n)
        Category: DB Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Delete the record in users_table
        mycursor = mydb.cursor()
        delete_command = 'DELETE FROM users_table WHERE Username={0}'.format(username)
        mycursor.execute(delete_command)
        mydb.commit()
        mycursor.close()

        # delete key from the dictionary as well
        del self.users_dict[username]

    def update_username(self, old_username: str, new_username: str):
        """
        Updates Users_db and its corresponding dict/RAM instances.
        :param old_username: original username
        :param new_username: new username
        :return: Updated dbs.
        Time: O(n) where n = size of Users_db
        COMMENT: expensive DB function.
        """
        #  First connect to DB
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()

        #  Update Users_db
        update_command = "UPDATE users_table SET Username = '{0}' WHERE Username = {1};".format(new_username,
                                                                                                old_username)
        mycursor.execute(update_command)
        mydb.commit()
        mycursor.close()

        #  Update users_dict
        for key, content in self.users_dict.items():
            if key == old_username:
                self.users_dict[new_username] = content
                del self.users_dict[old_username]

    def update_user(self, username: str, name: Optional[str] = None, age: Optional[int] = None,
                    password: Optional[str] = None):
        """
        update_accounts updates the user record info in both users_table and users dict.
        :param username: mandatory. The username of the user record to be updated.
        :param name: Updated User's name
        :param age: Updated User's age
        :param password: Updated password
        :return: Updated users_table and users dict.
        Time: O(n), where n is the size of users_table
        Category: DB function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()

        if name:
            # Update database
            update_command = "UPDATE users_table SET Name = '{0}' WHERE Username = {1};".format(name, username)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.users_dict[username]
            self.users_dict[username] = (name,) + original_record[1:]

        if age:
            # Update database
            update_command = "UPDATE users_table SET Age = '{0}' WHERE Username = {1};".format(age, username)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.users_dict[username]
            self.users_dict[username] = (original_record[0],) + (age,) + (original_record[2])

        if password:
            # Update database
            update_command = "UPDATE users_table SET Password = '{0}' WHERE Username = {1};".format(password,
                                                                                                    username)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.users_dict[username]
            self.users_dict[username] = original_record[:2] + (password,)

        mycursor.close()


class AccountsDB:

    def __init__(self):
        """
        __init__(self): creates an AccountDB object and update the account_num attribute.
                        retrieves account records from accounts_table, and stores it in a dict in RAM for faster use.
                        That is, copies DB into Dict.
        Side Effects: Creates an AccountsDB Object, Creates accounts dict;
        Time: O(n) where n is the size of the table.
        COMMENT: The accounts dictionary has account number as key, and other columns stored as tuple in contents.
                 when starting the program, dict and accounts_table are both up to date.
                 when committing changes to database, Dict should be updated simultaneously as well.
                 Also include sync database to sync RAM to database when database is temporarily unavailable.
        Category: Load Function, Database Function.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # retrieve data from accounts_table and store in dictionary.
        out_dict = dict()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM accounts_table;")
        data_list = mycursor.fetchall()

        for record in data_list:
            out_dict[record[0]] = record[1:]

        self.accounts_dict = out_dict

        mycursor.close()

    def reconstruct_accounts_db(self):
        """
        reconstruct_accounts_db(self): Removes the old accounts_table, and creates a new accounts_table that collects
                                       all accounts info.
        Side Effects: Truncate accounts_table.
                      Prints to I/O
        Time: O(1)
        :return: Updated, empty accounts_table.
        Category: DB Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Remove the old table
        mycursor = mydb.cursor()
        remove_command = 'DROP TABLE accounts_table;'
        mycursor.execute(remove_command)
        mydb.commit()

        # Create a new accounts table in mySQL database
        create_table_command = 'CREATE TABLE {0} (Account_num int, Username varchar(255), Account_name varchar(255), ' \
                               'Account_bal float, Account_type varchar(255));'.format('accounts_table')

        mycursor.execute(create_table_command)
        mydb.commit()
        mycursor.close()

        self.accounts_dict = dict()

        print('New accounts_table successfully created.')

    def add_account(self, acc_number: int, acc_name: str, acc_balance: float, acc_type: str, username: str):
        """
        add_account: creates a record in accounts_table that records the new registered account.
                     add a key-content in accounts dict that records the new account.
        :param acc_number: account number
        :param acc_name: account name
        :param acc_balance: account balance
        :param acc_type: account type
        :param username: username of account holder
        :return: an updated accounts_table with updated accounts dict
        Side Effects: Update accounts_table; update accounts dict
        Time: O(1)
        Category: DB Function
        COMMENT: cannot pass in a DBAccount object because of circular import.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate the new account record into accounts_table
        mycursor = mydb.cursor()
        commit_command = 'INSERT INTO {0} (Account_num, Username, Account_name, Account_bal, Account_type) VALUES ' \
                         '({1}, {2}, {3}, {4}, {5});'.format('accounts_table', acc_number, username,
                                                             acc_name, acc_balance, acc_type)
        mycursor.execute(commit_command)
        mydb.commit()
        mycursor.close()

        # add key to dictionary
        self.accounts_dict[acc_number] = (username, acc_name, acc_balance, acc_type)

    def delete_account(self, account_number: int):
        """
        delete_account removes the record of that account from the table.
        :param account_number: the account_num of the account to be deleted.
        :return: an updated accounts_table and accounts dict
        Side Effects: Update accounts_table and accounts dict
        Time: O(n), or use index can be optimized to O(log n)
        Category: DB Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Delete the record in accounts_table
        mycursor = mydb.cursor()
        delete_command = 'DELETE FROM accounts_table WHERE Account_num={0}'.format(account_number)
        mycursor.execute(delete_command)
        mydb.commit()
        mycursor.close()

        # delete key from the dictionary as well
        del self.accounts_dict[account_number]

    def update_account(self, account_number: int, username: Optional[str] = None, account_name: Optional[str] = None,
                       account_bal: Optional[float] = None, account_type: Optional[str] = None):
        """
        update_account updates the account record info in both accounts_table and accounts dict.
        :param account_number: mandatory. The account_number of the account to be modified
        :param username: username of the account
        :param account_name: name of account
        :param account_bal: account balance
        :param account_type: type of account
        :return: Updated accounts_table and accounts dict
        Time: O(1)
        Category: DB Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()

        if username:
            # Update database
            update_command = "UPDATE accounts_table SET Username = '{0}' WHERE Account_num = {1};".format(username,
                                                                                                          account_number)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.accounts_dict[account_number]
            self.accounts_dict[account_number] = (username,) + original_record[1:]

        if account_name:
            # Update database
            update_command = "UPDATE accounts_table SET Account_name = '{0}' WHERE Account_num = {1};".format(
                account_name, account_number)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.accounts_dict[account_number]
            self.accounts_dict[account_number] = (original_record[0],) + (account_name,) + original_record[2:]

        if account_bal:
            # Update database
            update_command = "UPDATE accounts_table SET Account_bal = '{0}' WHERE Account_num = {1};".format(
                account_bal, account_number)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.accounts_dict[account_number]
            self.accounts_dict[account_number] = original_record[:2] + (account_bal,) + (original_record[3])

        if account_type:
            # Update database
            update_command = "UPDATE accounts_table SET Account_type = '{0}' WHERE Account_num = {1};".format(
                account_type, account_number)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.accounts_dict[account_number]
            self.accounts_dict[account_number] = original_record[:3] + (account_type,)

        mycursor.close()

    def update_username(self, old_username: str, new_username: str):
        """
        Updates accounts_db and its corresponding dict/RAM instances.
        :param old_username: original username
        :param new_username: new username
        :return: Updated dbs.
        Time: O(n) where n = size of accounts_db
        COMMENT: expensive DB function.
        """
        #  First connect to DB
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()

        #  Update accounts_db
        update_command = "UPDATE accounts_table SET Username = '{0}' WHERE Username = {1};".format(new_username,
                                                                                                   old_username)
        mycursor.execute(update_command)
        mydb.commit()
        mycursor.close()

        #  Update accounts_dict
        for key, content in self.accounts_dict.items():
            if content[0] == old_username:
                self.accounts_dict[key] = (new_username,) + content[1:]
