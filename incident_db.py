import datetime
import mysql.connector
from typing import Optional


class IncidentDB:

    def __init__(self):
        """
        __init__(self): creates an incident table that collects all account incidents from all user's accounts.
        Side Effects: Create an incident DB table
                      Prints to I/O
        Time: O(1)
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Create a new incident table in mySQL database
        mycursor = mydb.cursor()
        create_table_command = 'CREATE TABLE {0} (Incident_num int, Date varchar(255), User_name varchar(255), ' \
                               'Username varchar(255), Account int, Incident_Description varchar(255));'.format(
                                'incident_table')

        mycursor.execute(create_table_command)
        mydb.commit()
        mycursor.close()

        self.incident_num = 1

        print('Incident table successfully created.')

    def commit_incident(self, user_name: str, username: str, incident_description: str,
                        account_num: Optional[int] = None):
        """
        commit_incident: creates a record in incident_table that records the incident.
        :param user_name: the user's name
        :param username:  the Username of UserID
        :param account_num: optional. The account related to the incident.
        :param incident_description: The description of the incident.
        :return: an updated incident table.
        Side Effects: Update incident table.
        Time: O(1)
        COMMENT: if "SELECT MAX(Incident_num) FROM incident_table" command is used, the runtime without SQL index
                 will be O(n), and with index will be O(log n). That is, every time the program restarts, at least a
                  O(log n) process is necessary to find the updated incident_num using the command.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate the incident record into incident_table
        mycursor = mydb.cursor()

        if account_num:
            commit_command = 'INSERT INTO {0}(Incident_num, Date, User_name, Username, Account, Incident_Description)' \
                             'VALUES ({1}, {2}, {3}, {4}, {5}, {6});'.format('incident_table', self.incident_num,
                                                                             str(datetime.date.today()),
                                                                             user_name, username, 'NULL',
                                                                             incident_description)
        else:
            commit_command = 'INSERT INTO {0}(Incident_num, Date, User_name, Username, Account, Incident_Description)' \
                         'VALUES ({1}, {2}, {3}, {4}, {5}, {6});'.format('incident_table', self.incident_num,
                                                                         str(datetime.date.today()),
                                                                         user_name, username, account_num,
                                                                         incident_description)
        mycursor.execute(commit_command)
        mydb.commit()

        mycursor.close()

        self.incident_num += 1

    def resolve_incident(self, incident_num):
        """
        resolve_incident updates the incident table after the incident is resolved.
        That is, it removes the record of that incident from the table.
        :param incident_num: the incident number indicating the record to be deleted.
        :return: an updated incident table.
        Side Effects: Update incident table
        Time: O(n), or using index can be optimized to O(log n)
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Delete the record in incident_table
        mycursor = mydb.cursor()

        delete_command = 'DELETE FROM incident_table WHERE Incident_num={0}'.format(incident_num)
        mycursor.execute(delete_command)
        mydb.commit()

        mycursor.close()
