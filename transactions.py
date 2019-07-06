from main import App


class Transactions(App):

    def __deposit__(self, username: str, acc_num: int, source: str, amount: float):
        """
        Deposit transaction at high level. Update dicts, db_tables, and increments trans_num.
        :param username: username of the account holder
        :param acc_num: account to receive deposit.
        :param source: description of deposit
        :param amount: amount to be deposited
        """
        self.accounts_users_dict[username].__deposit__(self.trans_num, acc_num, source, amount)
        self.trans_num += 1

    def __withdrawal__(self, username: str, acc_num: int, source: str, amount: float):
        """
        withdrawal transaction at high level. Update dicts, db_tables, and increments trans_num.
        :param username: username of the account holder
        :param acc_num: account to withdraw from.
        :param source: description of withdrawal
        :param amount: amount to be withdrawn
        """
        self.accounts_users_dict[username].__withdrawal__(self.trans_num, acc_num, source, amount)
        self.trans_num += 1

    #  TODO: all types of transaction functions
