import mysql.connector
from Bank_Account import BankAccount


"""
Client Account Class:
A client account class consists of a dictionary of individual chequing, savings 
and credit accounts. This class has the functionanilty that is provided with 
managing multiple accounts as a client. These include:
    Modifying Bank Balances
        Deposits
        Withdrawals
"""




class ClientAccount(BankAccount):
    """"
    An ABC client holds mutiple client accounts. A client must have the 
    following properties:
        
    Attributes:
        Client Number: An integer representing the client's's identity.
        Client Account Name: A string representing the client's name.
        Client Balance: A float maintaining the client's book balance.
        Client Type: A string representing the type of client account, either
                   chequing, savings, or credit account.
    """

    __accounts = dict()

    def __deposit__(self, source: str, date: str, amount: float):
        """
        __deposit(self, amount, source, date): consumes an amount, date, deposit
                                               description, updates its
                                               balance, and logs in the account's history DB table.
        Side Effect: Print to I/O (asks for destination)
        Time: O(1)
        """

        self.balance += amount

        # Connect to mySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="anshulshawn",
            database="Bank_Ecosystem_DB"
        )

        # Record history -- add time.
        mycursor = mydb.cursor()
        history_record = 'INSERT INTO {0} (Date, Transaction_Description, Deposits, Balance) VALUES ({1}, {2}, {3})'.format(
            self.table, date, source, amount, self.balance)
        mycursor.execute(history_record)
        mydb.commit()

        mycursor.close()

        # Print to I/O
        print("Successful Deposit to Account Number {0} on {1}, {2}".format(self.number, date, source))
        print("Account Balance", self.balance)

    def __withdrawal__(self, amount=0.0, source="", date=""):
        """
        withdrawal(self, amount, source, date): consumes withdrawal amount, date
                                                and withdrawal description, updates its
                                               balance, and logs in the account's history DB table.
        Side Effects: Print to I/O
        Time: O(1)
        """

        self.balance -= amount

        # Check Account Balance to Determine if Transaction is Valid
        if self.balance < 0:
            print("Insufficient Funds to Complete Transaction")
            self.balance += amount

        # Connect to mySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="anshulshawn",
            database="Bank_Ecosystem_DB"
        )

        # Record history -- add time.
        mycursor = mydb.cursor()
        history_record = 'INSERT INTO {0} (Date, Transaction_Description, Withdrawals, Balance) VALUES ({1}, {2}, {3})'.format(
            self.table, date, source, amount, self.balance)
        mycursor.execute(history_record)
        mydb.commit()

        mycursor.close()

        # Print to I/O
        print("Successful Withdrawal from Account Number {0} on {1}, {2}".format(self.number, date, source))
        print("Account Balance", self.balance)
