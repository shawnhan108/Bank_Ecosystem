from general_dbs import IncidentDB, UsersDB, AccountsDB
from Bank_Account_Class import UserDB


class Load:

    def __init__(self):
        """
        __init__: loads incident DB, userDB and AccountsDB in RAM dictionary.
                  loads all DBAccount and UserDB objects and store in accounts_users_dict RAM dictionary.
                  Gets the largest transaction number over all transactions.
        """
        self.incident_db = IncidentDB()
        self.users_db = UsersDB()
        self.accounts_db = AccountsDB()
        self.trans_num = 0
        temp_dict = dict()

        for key in self.users_db.users_dict.items():
            # First, load userDB Object and add to accounts_users_dict.
            temp_user = UserDB()
            temp_user.__load_user__(key)
            temp_user.__load_user_dict__()
            temp_dict[key] = temp_user

            # Find max transaction number.
            max_trans_num_from_user = max(temp_user.trans_dict.keys())
            if max_trans_num_from_user > self.trans_num:
                self.trans_num = max_trans_num_from_user

        self.accounts_users_dict = temp_dict
        self.trans_num += 1  # now this is the next transaction number ready to use.


def start_backend():
    app = Load()
    return app


app = start_backend()
