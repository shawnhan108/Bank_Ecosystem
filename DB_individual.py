from Account_individual import Individual_Account


# class DB makes each DB an object, and provides functions for all account's DB, inherits all account attributes.
# most functions use SQL functions
class DB(Account):

    # popular_cat() consumes an object, connect to DB, finds the category that appears the most,
    #       and returns the category.
    # popular_cat(): (ID, name, DB, account_bal) -> str
    def popular_cat(self):
        pass

    # avg_transaction(category, length) consumes the category of transactions and the number of days of past
    #       transactions that the user requests, and calculates average transaction per week in that category during the
    #       length of time
    # avg_transaction(category, length) -> long
    def avg_transaction(self, cat, length):
        pass

    # DB_report_generate(length) generates an account's DB summary for the specified duration
    # DB_report_generate(length): (ID, name, DB, account_bal) -> PDF/docx etc.
    def db_report_generate(self, length):
        pass

    # cat_change(cat, compare_period) consumes the category of transactions and the period of time of past
    #       transactions that the user requests, and calculates the percentage change of expenditure on that category
    #       in the past <duration> comparing to the period before.
    # cat_change(cat, compare_period): (ID, name, DB, account_bal), str, int -> long%
    def cat_change(self, cat, compare_period):
        pass
