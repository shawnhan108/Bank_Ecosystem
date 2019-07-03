import datetime
import mysql.connector
from typing import Optional


class IncidentDB:

    def __init__(self):
        """
        __init__(self): creates a incidentDB object and update the incident_num attribute.
                        retrieves incident records from incident_table, and stores it in a dictionary in RAM for faster
                        use. That is, copies database into dict.
        Side Effects: creates an incidentDB object; Creates incident_table.
        Time: O(n) where n is the size of the table.
        COMMENT: The incident dictionary has incident number as key, and other columns stored in list.
                 when starting the program, dict and incident_table are both update to date.
                 when committing changes to database, Dict should be updated simultaneously as well.
                 Also include sync database to sync RAM to database when database is temporarily unavailable.
        Category: Load Function, Database Function.
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # to get the next incident_num to be used
        mycursor = mydb.cursor()
        mycursor.execute("SELECT MAX(Incident_num) FROM incident_table;")
        self.incident_num = mycursor.fetchone()[0] + 1

        # retrieve data from incident_table and store in dictionary.
        out_dict = dict()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM incident_table;")
        data_list = mycursor.fetchall()

        for record in data_list:
            out_dict[record[0]] = record[1:]

        self.incident_dict = out_dict

        mycursor.close()

    def reconstruct_incident_db(self):
        """
        reconstruct_incident_db(self): Removes the old incident table, and creates a new incident table that collects
                                        all account incidents from all user's accounts.
        Side Effects: Remove old incident_table, and create an incident DB table
                      Prints to I/O
        Time: O(1)
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Remove the old table
        mycursor = mydb.cursor()
        remove_command = 'DROP TABLE incident_table;'
        mycursor.execute(remove_command)
        mydb.commit()

        # Create a new incident table in mySQL database
        create_table_command = 'CREATE TABLE {0} (Incident_num int, Date varchar(255), User_name varchar(255), ' \
                               'Username varchar(255), Account int, Incident_Description varchar(255), Status' \
                               ' varchar(255));'.format('incident_table')

        mycursor.execute(create_table_command)
        mydb.commit()
        mycursor.close()

        self.incident_num = 1
        self.incident_dict = dict()

        print('New incident table successfully created.')

    def commit_incident(self, user_name: str, username: str, incident_description: str,
                        account_num: Optional[int] = None):
        """
        commit_incident: creates a record in incident_table that records the incident.
                         add a key-content in incident dict that records the incident.
        :param user_name: the user's name
        :param username:  the Username of UserID
        :param account_num: optional. The account related to the incident.
        :param incident_description: The description of the incident.
        :return: an updated incident table with updated incident_dict.
        Side Effects: Update incident table; Update incident dict
        Time: O(1)
        COMMENT: if "SELECT MAX(Incident_num) FROM incident_table" command is used, the runtime without SQL index
                 will be O(n), and with index will be O(log n). That is, every time the program restarts, at least a
                  O(log n) process is necessary to find the updated incident_num using the command.
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")

        # Generate the incident record into incident_table
        mycursor = mydb.cursor()

        if account_num:
            commit_command = 'INSERT INTO {0}(Incident_num, Date, User_name, Username, Account, Incident_Description, ' \
                             'Status) VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7});'.format('incident_table',
                                                                                          self.incident_num,
                                                                                          str(datetime.date.today()),
                                                                                          user_name, username,
                                                                                          account_num,
                                                                                          incident_description,
                                                                                          'Unresolved')
        else:
            commit_command = 'INSERT INTO {0}(Incident_num, Date, User_name, Username, Account, Incident_Description, ' \
                             'Status) VALUES ({1}, {2}, {3}, {4}, {5}, {6}, {7});'.format('incident_table',
                                                                                          self.incident_num,
                                                                                          str(datetime.date.today()),
                                                                                          user_name, username, 'NULL',
                                                                                          incident_description,
                                                                                          'Unresolved')
        mycursor.execute(commit_command)
        mydb.commit()

        mycursor.close()

        # add key to the dictionary as well
        if account_num:
            self.incident_dict[self.incident_num] = (
                str(datetime.date.today()), user_name, username, account_num, incident_description, 'Unresolved')
        else:
            self.incident_dict[self.incident_num] = (
                str(datetime.date.today()), user_name, username, 'NULL', incident_description, 'Unresolved')

        self.incident_num += 1

    def delete_incident(self, incident_num):
        """
        resolve_incident updates the incident table after the incident is resolved.
        That is, it removes the record of that incident from the table.
        :param incident_num: the incident number indicating the record to be deleted.
        :return: an updated incident table.
        Side Effects: Update incident table
        Time: O(n), or using index can be optimized to O(log n)
        Category: Database Function
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

        # delete key from the dictionary as well
        del self.incident_dict[incident_num]

    def update_incident(self, incident_num, user_name: Optional[str] = None, username: Optional[str] = None,
                        incident_description: Optional[str] = None, account_num: Optional[int] = None,
                        status: Optional[str] = None):
        """
        update_incident updates the incident record info in both incident_table and incident_dict.
        :param incident_num: mandatory. The incident number of the record that is being updated.
        :param user_name: Updated User's Name
        :param username: Updated Username
        :param incident_description: Updated incident description
        :param account_num: updated account number
        :param status: updated status, usually changes from Unresolved to resolved.
        :return: Updated incident table and incident dict.
        Side Effects: Updated incident table and incident dict.
        Time: O(1)
        Category: Database Function
        """
        # Connect to mySQL Database
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="anshulshawn",
                                       database="Bank_Ecosystem_DB")
        mycursor = mydb.cursor()
        if user_name:
            # Update database
            update_command = "UPDATE incident_table SET User_name = '{0}' WHERE Incident_num = {1};".format(user_name,
                                                                                                            incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[0] + (user_name,) + original_record[2:]

        elif username:
            # Update database
            update_command = "UPDATE incident_table SET Username = '{0}' WHERE Incident_num = {1};".format(username,
                                                                                                           incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:2] + (username,) + original_record[3:]

        elif incident_description:
            # Update database
            update_command = "UPDATE incident_table SET Incident_Description = '{0}' WHERE Incident_num = {1};".format(
                incident_description, incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:4] + (incident_description,) + original_record[5:]

        elif account_num:
            # Update database
            update_command = "UPDATE incident_table SET Account = '{0}' WHERE Incident_num = {1};".format(
                account_num, incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:3] + (account_num,) + original_record[4:]

        elif status:
            # Update database
            update_command = "UPDATE incident_table SET Status = '{0}' WHERE Incident_num = {1};".format(
                status, incident_num)
            mycursor.execute(update_command)
            mydb.commit()

            # Update dictionary
            original_record = self.incident_dict[incident_num]
            self.incident_dict[incident_num] = original_record[:5] + (status,)

        else:
            return

        mycursor.close()
