import random
import mysql.connector


class BankAccount:
    acc_number: int
    acc_name: str
    acc_balance: float
    acc_type: str
    acc_table: str

    # __init__(self, acc_num): return a basic account object whose account number is *acc_num*, account name is
    #                          *acc_name* starting balance is *acc_balance* and account type is *acc_type*.
    # Side Effects: Creates a Bank Account Instance
    #               Prints to I/O
    # Time: O(1)
    def __init__(self, acc_number=0):
        # Initialize Account Details
        self.acc_number = acc_number  # Account Number
        self.acc_name = input("Please enter account name:")  # Account Name
        self.acc_balance = 0.0  # Account Balance
        self.acc_type = input("Please enter account type (Personal, Savings, Family or Savings): ")  # Account Type
        self.acc_table = 'DB_' + str(self.acc_number)  # Account DB Table Name

        print("Class Successfully Created.")


class DBAccount(BankAccount):
    acc_number: int

    # __init__(self, acc_num): returns a basic account object with account number *acc_num* and a respective MySQL
    #                          database to store transaction history.
    # Side Effects: Create a DB Instance
    #               Create a Bank Account Instance
    #               Prints to I/O
    # Time: O(1)
    def __init__(self, acc_number=0):
        BankAccount.__init__(self, acc_number)

        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Create New Table in mySQL Database
        mycursor = mydb.cursor()
        create_table_command = 'CREATE TABLE {0} (Date varchar(255), Transaction_Description varchar(255),' \
                               '  Withdrawals float, Deposits float, Balance float);'.format(self.acc_table)

        mycursor.execute(create_table_command)
        mydb.commit()

        # Generate First History Entry -- Recording Account Creation
        first_record_command = 'INSERT INTO {0} (Date, Transaction_Description, Withdrawls, Deposits, Balance) VALUES' \
                               '({1}, {2}, {3}. {4} {5})'.format(self.acc_table, str(datetime.date.today()),
                                                                 'Account ' + str(self.acc_number) + ' Created', 0.00,
                                                                 0.00, 0.00)
        mycursor.execute(first_record_command)
        mydb.commit()

        mycursor.close()


class UserID(DBAccount):
    name: str
    accounts: dict
    age: int
    username: str
    password: str

    # __is_valid_Pass_(self): checks if a string meets the acceptance criteria for a password.
    # Time: O(n), where n is the length of the string.
    def __is_valid_Pass__(self):
        upper_pass: int
        lower_pass: int
        num_pass: int
        spec_char_pass:
        length_pass: int
        special_chars: tuple
        password: str
        password_valid_score: int

        upper_pass = 0  # Store Criteria as Boolean Variable
        lower_pass = 0
        num_pass = 0
        spec_char_pass = 0
        length_pass = 0

        special_chars = ("[", "@", "_", "!", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?", "/", "\\", "|", "}",
                         "{", "~", ":", "]", '"')  # Tuple of Characters Considered as Special Characters

        password = self.password


        for i in password: # Compute password_valid_score
            if i.isupper():  # Check if Password Contains a Uppercase Character
                upper_pass = 1

            if i.islower():  # Check if Password Contains a Lowercase Character
                lower_pass = 1

            if i.isdigit():  # Check if Password Contains a Numerical Digit Character
                num_pass = 1

            if i in special_chars:
                spec_char_pass = 1  # Check if Password Contains a Special Character

        if len(password) >= 6:
            length_pass = 1  # Check if Password is Minimum 6 Characters Length

        password_valid_score = length_pass + lower_pass + num_pass + spec_char_pass + upper_pass

        if password_valid_score == 5:
            return True
        else:
            return False


    # __password_setup__(self): maintains the process to successful password setup for a User ID.
    # Side Effects: Mutates UserID
    #               Print to I/O
    # Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
    def __password_setup__(self):
        i: int = 0  # Boolean to Represent Password Set-up Status

        while i == 0:  # Request New Password Till Successful Completion of User ID Password Set-up
            while not self.__is_valid_Pass__:  # Check if User ID Password is Valid
                # Print Valid Password Acceptance Criteria
                print("Please make sure you're password has at least:\n")
                print("1) At least one upper case character;\n")
                print("2) At least one lower case character;\n")
                print("3) At least one numerical digit character;\n")
                print("4) At least one special character; and\n")
                print("5) Minimum 6 characters.")

                self.password = input("Please enter your password: ")  # Request User ID Password

            check_password: str = input("Please renter your password: ")  # Request Password Confirmation

            if check_password == self.password:  # Acceptance Criteria
                i = 1 # Successful Password Setup
            else:
                self.password = "0" # Automatic Password Failure to Reset Password Set-Up Process


    # __init__(self): return a User ID, DB and Bank Account with username and password credentials along with other
    #                 account details
    # Side Effect: Create a User ID Instance
    #              Prints to I/O
    # Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
    def __init__(self):
        self.name = input("Name: ")  # Initialize User ID Name
        self.accounts = dict() # Store Accounts for User ID

        age = input("Age: ")  # Request User Age

        while (not age.isnumeric()) or self.age < 0 or self.age > 125:  # Check User's Age is Valid
            print("Please enter your correct age.")
            self.age = input("Age: ")

            # TODO Record "incidents" -- user too young -- in a database
        if self.age < 18:
            print("User is too young.")
            age = input("Age: ")

        self.age = int(age)
        self.username = input("Please enter your username: ")  # Request Username
        self.password = input("Please enter your password: ")  # Request Password

        self.__password_setup__()  # Create Successful Password Setup

        print("Successful Account Created.")  # Notify User of Successful Account Creation


    # __change_password__(self): modifies User ID password with the valid password set-up protocol.
    # Side Effects: Mutates UserID
    #               Print to I/O
    # Time: O(n * m), where n is the length of the password and m is the number of attempts to setup a password.
    def __change_password__(self):
        self.password = input("Please enter your new password: ")  # Request User for New Password

        self.__change_password__()  # Create Successful Password Setup


    # __change_username__(self): modifies User ID username.
    # Side Effect: Mutates UserID
    #              Prints to I/O
    # Time: O(1)
    def __change_username__(self):
        self.username = input("Please enter your username: ")  # Request User for Username


    # __add_account__(self): creates a new bank account instance and assigns ownership to the User ID
    # Side Effect: Mutates UserID
    #              Create a DB Instance
    #              Create a Bank Account Instance
    #              Print to I/O
    # Time: O(1)
    def __add_account__(self):
        acc_num = random.randint(100000, 999999)

        while acc_num in self.accounts:
            acc_num = random.randint(100000, 999999)


        account_temp = DBAccount.__init__(self, acc_num)

        self.accounts[acc_num] = account_temp


    # __print_User_Details__(self): prints User ID and it's bank accounts detail.
    # Side Effect: Print to I/O
    # Time: O(1)
    def __print_User_Details__(self):


    # __transfer__(self): withdraws money from one accout and deposits it to another.
    # Side Effect: Print to I/O
    # Time: O(1)
    def __transfer__(self):

