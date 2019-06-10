"""
Bank Account Class
A bank class consists of a dictionary of client client accounts. This class has 
the basic functionality for an account. These includes:
    Creating Accounts
    Destroying Accounts
    Modifying Accounts:
        Printing Account Client Balances (Debit/Credit)
"""

class Bank_Class():
    """"
    An ABC Bank holds a customers bank account. A bank must have the 
    following properties:
        
        
    Attributes:
        Account Number: An integer representing the client's's identity.
        Account Account Name: A string representing the client's name.
        Account Balance: A float maintaining the client's book balance.
        Account Type: A string representing the type of client account, either
                      bank, client, chequing, savings, or credit account.
    """ 
    __clients = dict()
        
        
    def __init__(self, number=0, name="Bank 1", balance=0.0, 
                 account_type = ""):
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
        
        print("Class Successfully Created")       
        
        
    def __destory__(self):
        """
        __destroy_(_self): destroys the instance of an entire bank class.
        Side Effects: Destorys a bank account instance.
                      Prints to I/O
        Time: O(1)
        """
        self.number = 0
        self.name = ""
        self.balance = 0.0
        print("Deleted")
        
    def __print_accounts__(self):
        """
        __print_accounts__(self): recursively prints all accounts number, name 
                                  and balance.
        Side Effects: Prints to I/O
        Time: O(n)
        """
        pass        