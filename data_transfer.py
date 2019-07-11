import mysql.connector

class DataTransfer:
    def __init__(self, hostInput, portInput, userInput, passwordInput):
        self.errorLogFileName = 'errors.txt'
        self.conn = mysql.connector.connect(host=hostInput, port=portInput, user=userInput, password=passwordInput)
        self.cursor = self.conn.cursor()

        # Erase all of the contents in errors.txt. Errors will be logged there if an SQL command error occurs
        open(self.errorLogFileName, mode='w+').close()
    def __del__(self):
        self.conn.close()
    def insertData(self, sqlCommand):
        try:
            self.cursor.execute(sqlCommand)
            self.conn.commit()
        except:
            # Print out that the SQL command execution has failed, and advise the user to examine the errors text file
            print(f'SQL command execution has failed. Check {self.errorLogFileName}.')

            # Open the file errors.txt and output the errors there
            with open(self.errorLogFileName, mode='a') as errorFile:
                errorFile.write(f'{sqlCommand}execution has failed.')