"""
Individual Account Class:
An individual account class consists of a series of functions linking user's 
account functions and their respective databases. This class has the 
functionanilty that is provided with managing accounts as a user and also 
provides data anlytics for business insights and risk mitigation. These include:
    Printing User DB Transactional History
    Modifying Bank Balances DB Transactional History with User's Deposits and 
    Withdrawals
    Data Analytics (Business Insights):
        Most Active Account
        Average Transaction per Month
        Average Type of Transaction per Month
    Data Analytics (Risk Mitigation):
        Working Capital
        Working Capital (Trending)
        Current Ratio
        Current Ratio (Trending)
        "Return on Equity" (Addition to Wealth)
        "Return on Equity" (Trending)
"""

from User_Account import User_Class

class Individual_Class(User_Account):
    """"
    An ABC indivual account class represents a single user's account.
    """
    
    def __init__(self, number = 0, name="Bank 1", balance=0.0, 
                 account_type = ""):
        """
        __init__(self, number, name, balance): return a user object whose 
                                               identity number is *number*, name
                                               is *name*, starting balance is
                                               *balance* and account type is 
                                               *type*.
        Side Effects: Creates a user account instance.
                      Prints to I/O
        Time: O(1)
        """
        
        self.number = number
        self.name = name
        self.balance = balance 
        self.account_type = account_type
        
        print("Individual Class Successfully Created")
        
        
    def __history__(self, date_start="", date_stop=""):
        pass
    
    def __deposit_track__(self, amount=0.0, source="", date=""):
        pass
    
    def __withdrawal_track_(self, amount=0.0, source="", date=""):
        pass
    
    def __most_active__(self, date_start="", date_stop=""):
        pass
    def __avg_trans__(self):
        pass
    
    def __avg_trans_type__(self):
        pass
    
    def __data_business__(self, date_start="", date_stop=""):
        pass
    
    def __work_cap__(self):
        pass
    
    def __work_cap_trend__(self):
        pass
    
    def __curr_ratio__(self):
        pass
    
    def __curr_ratio_trend__(self):
        pass
    
    def __return_on_eq__(self):
        pass
    
    def __return_on_eq_trend__(self):
        pass
    
    def __data_risk_(self, date_start="", date_stop=""):
        pass