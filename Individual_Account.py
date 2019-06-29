"""
Individual Account Class:
An individual account class consists of a series of functions linking client's 
account functions and their respective databases. This class has the 
functionanilty that is provided with managing accounts as a client and also 
provides data anlytics for business insights and risk mitigation. These include:
    Printing Client DB Transactional History
    Modifying Bank Balances DB Transactional History with Ckient's Deposits and 
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

from Client_Account import ClientAccount


class IndividualAccount(ClientAccount):
    """"
    An ABC indivual account class represents a single client's account. An
    individual client must have the following properties:
        
    Attributes:
        Account Number: An integer representing the client's's identity.
        Account Account Name: A string representing the client's name.
        Account Balance: A float maintaining the client's book balance.
        Account Type: A string representing the type of client account, either
                      bank, client, chequing, savings, or credit account.
    """

    def __transfer__(self, account_dep = "", account_withdraw = ""):
        pass

    def __history__(self, date_start="", date_stop=""):
        """
        Selects records from SQL table with date filter.
        :param date_start: string. The start date of the history requested.
        :param date_stop:  string. The end date of the history requested.
        :return: Void. displays the account's transaction history within the range of time defined by params
        """
        pass

    def __deposit_track__(self, amount=0.0, source="", date=""):
        """
        Selects records from SQL table with type = deposit filter.
        :param amount: float. The amount of transaction.
        :param source: string. The source of transaction.
        :param date: string. The day of transaction.
        :return: deposit transaction records that satisfy the conditions defined by params.
        """
        pass

    def __withdrawal_track_(self, amount=0.0, source="", date=""):
        """
        Selects records from SQL table with type = withdrawal filter
        :param amount: float. The amount of transaction.
        :param source: string. The source of transaction.
        :param date: string. The day of transaction.
        :return: withdrawal transaction records that satisfy the conditions defined by params.
        """
        pass

    def __most_active__(self, date_start="", date_stop=""):
        pass
    
    def __most_active__type(self, data_start="", date_stop=""):
        pass

    def __avg_trans__(self):
        """
        Use SQL function to obtain sum of transaction records and total transaction numbers.
        :return: Average transaction amount (float) = sum of transaction records/total transaction nums.
        """
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
        """
        Using object 'amount' attribute for total deposit (D).
        :return: the currency ratio of the client = C/D
        """
        pass

    def __curr_ratio_trend__(self):
        """
        SQL function to calculate total deposit on each day.
        :return: the trend of client's currency ratio stored in a dict, ideally used for graphing (front).
        """
        pass

    def __return_on_eq__(self):
        """
        Using object 'amount' attribute for total equity (D).
        :return: the return on equity of the client = net income/total Equity
        """
        pass

    def __return_on_eq_trend__(self):
        """
        SQL function to calculate total equity on each day.
        :return: The trend of client's return on equity stored in a dict, ideally used for graphing (front).
        """
        pass

    def __data_risk_(self, date_start="", date_stop=""):
        pass
