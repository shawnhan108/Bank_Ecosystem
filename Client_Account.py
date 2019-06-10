"""
Client Account Class:
A client account class consists of a dictionary of individual chequing, savings 
and credit accounts. This class has the functionanilty that is provided with 
managing multiple accounts as a client. These include:
    Modifying Bank Balances
        Deposits
        Withdrawals
"""

from Bank_Account import Bank_Class

class Client_Class(Bank_Class):
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
