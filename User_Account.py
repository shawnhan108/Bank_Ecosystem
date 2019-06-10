"""
User Account Class:
A user account class consists of a dictionary of individual chequing, savings 
and credit accounts. This class has the functionanilty that is provided with 
managing multiple accounts as a user. These include:
    Modifying Bank Balances
        Deposits
        Withdrawals
"""

from Bank_Account import Bank_Class

class User_Class(Bank_Class):
    """"
    An ABC user holds mutiple user accounts. A user must have the 
    following properties:
        
    Attributes:
        User Number: An integer representing the user's's identity.
        User Account Name: A string representing the user's name.
        User Balance: A float maintaining the user's book balance.
        User Type: A string representing the type of user account, either
                   chequing, savings, or credit account.
    """
    
    __accounts = dict()
    
    
    def __init__(self, number = 0, name="Bank 1", balance=0.0, 
                 account_type = ""):
        """
        __init__(self, number, name, balance): return a user object whose 
                                               identity number is *number*, name
                                               is *name*, starting balance is
                                               *balance* and account type is 
                                               *type*.
        Side Effects: Creates a user account instance.
                      Prints to I/O.
        Time: O(1)
        """
        
        self.number = number
        self.name = name
        self.balance = balance 
        self.account_type = account_type
        
        print("User Class Successfully Created")
    
    
    def __deposit__(self, amount=0.0, source="", date=""):
        """
        __deposit(self, amount, source, date): consumes an amount, date, deposit
                                               description, and updates its 
                                               balance.
        Side Effect: Print to I/O (asks for destination)
        Time: O(1)
        """
        pass    

    def __withdrawal__(self, amount=0.0, source="", date=""):
        """
        withdrawal(self, amount, source, date): consumes withdrawal amount, date
                                                and withdrawl description, and 
                                                updates its balance.
        Side EffectsL Print to I/O (asks for destination)
        Time: O(1)
        """
        pass
