"""
Bank Account Class
A bank class consists of a dictionary of client client accounts. This class has 
the basic functionality for an account. These includes:
    Creating Accounts
    Destroying Accounts
    Modifying Accounts:
        Printing Account Client Balances (Debit/Credit)
"""
import mysql.connector
import datetime


class BankAccount:
    """"
    An ABC Bank holds a customers bank account. A bank must have the 
    following properties:
        
        
    Attributes:
        Account Number: An integer representing the client's's identity.
        Account Account Name: A string representing the client's name.
        Account Balance: A float maintaining the client's book balance.
        Account Type: A string representing the type of client account, either
                      bank, client, chequing, savings, or credit account.
        Account Table: A string representing the name of a DB table that stores the account's transaction history.
    """
    
    __clients = dict()
    

    def __init__(self, number=0, name="Bank 1", balance=0.0, account_type=""):
        """
        __init__(self, number, name, balance, account_type): return a basic 
            account object whose identity number is *number*, name is *name*, 
            starting balance is *balance* and account type is *sccount_type*.
        Side Effects: Creates a client account instance.
                      Prints to I/O
        Time: O(1)
        """

        self.number = number
        self.name = name
        self.balance = balance
        self.account_type = account_type
        self.table = 'DB_' + str(self.number)

        # Create new DB table for the new account
        # Connect to mySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="anshulshawn",
            database="Bank_Ecosystem_DB"
        )

        # Create new table
        mycursor = mydb.cursor()
        create_table_command = 'CREATE TABLE {0} (Date varchar(255), Transaction_Description varchar(255), ' \
                               'Withdrawals float, Deposits float, Balance float);'.format(self.table)
        mycursor.execute(create_table_command)
        mydb.commit()

        # Generate the first history entry recording account creation.
        first_record_command = 'INSERT INTO {0} (Date, Transaction_Description, Balance) VALUES ({1}, {2}, {3})'.format(
            self.table, str(datetime.date.today()), 'Account ' + str(self.number) + ' Created', 0.00)
        mycursor.execute(first_record_command)
        mydb.commit()

        mycursor.close()

        print("Class Successfully Created")


    def __destory__(self):
        """
        __destroy_(_self): destroys the instance of an entire bank class.
        Side Effects: Destorys a bank account instance. Drops the account's DB table.
                      Prints to I/O
        Time: O(1)
        """
        self.number = 0
        self.name = ""
        self.balance = 0.0

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="anshulshawn",
            database="Bank_Ecosystem_DB"
        )

        mycursor = mydb.cursor()
        drop_command = 'DROP TABLE {0}'.format(self.table)
        mycursor.execute(drop_command)
        mydb.commit()
        mycursor.close()

        ## Destroy the instance in the dictionary!

        print("Deleted")


    def __print_accounts__(self):
        """
        __print_accounts__(self): recursively prints all accounts number, name 
                                  and balance.
        Side Effects: Prints to I/O
        Time: O(n)
        """
        account_nums = BankAccount.__clients.keys()

        for i in account_nums:
            print("Account Number: ", i, "Account Name: ", BankAccount.__clients[i].name, "Account Type: ",
                  BankAccount.__clients[i].account_type)
            print("Account Balance: ", BankAccount.__clients[i].balance, "\n")
