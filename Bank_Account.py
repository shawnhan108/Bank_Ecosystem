"""
Bank Account Class
A bank class consists of a dictionary of client user accounts. This class has 
the basic functionality for an account. These includes:
    Creating Accounts
    Destroying Accounts
    Modifying Accounts:
        Printing Account User Balances (Debit/Credit)
"""

class Bank_Class():
    """"
    An ABC Bank holds a customers bank account. A bank must have the 
    following properties:
        
        
    Attributes:
        Bank Number: An integer representing the bank's identity.
        Bank Account Name: A string representing the bank's name.
        Bank Balance: A float maintaining the bank's book balance.
    """
    __users = dict()
        
        
    def __init__(self, number, name="Bank 1", balance=0.0):
        """
        __init__(self, number, name, balance): return a bank object whose 
                                               identity number is *number*, name
                                               is *name* and starting balance is
                                               *balance*.
        Side Effects: Creates a bank account instance.
                      Prints to I/O
        Time: O(1)
        """
        self.number = number
        self.name = name
        self.balance = balance
        
        print("Bank Class Successfully Created")        
        
        
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
        
    
    
        
        