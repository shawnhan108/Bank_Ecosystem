from general_dbs import IncidentDB, UsersDB, AccountsDB
from Bank_Account_Class import UserDB


class Load:

    def __init__(self):
        """
        __init__: loads incident DB, userDB and AccountsDB in RAM dictionary.
                  loads all DBAccount and UserDB objects and store in accounts_users_dict RAM dictionary.
        """
        self.incident_db = IncidentDB()
        self.users_db = UsersDB()
        self.accounts_db = AccountsDB()

        temp_dict = dict()
        for key in self.users_db.users_dict.items():
            temp_user = UserDB()
            temp_user.__load_user__(key)
            temp_user.__load_user_dict__()
            temp_dict[key] = temp_user
        self.accounts_users_dict = temp_dict


def start_backend():
    app = Load()
    return app


app = start_backend()
