import mysql.connector

class DataTransfer:
    def __init__(self, hostInput, portInput, userInput, passwordInput):
        self.errorLogFileName = 'errors.txt'
        self.conn = mysql.connector.connect(host=hostInput, port=portInput, user=userInput, password=passwordInput)
        self.cursor = self.conn.cursor()
    def __del__(self):
        self.conn.close()
    def insertData(self, sqlCommand):
        try:
            # Clear all of the contents in the error text file. If there is an error, it will be written in the except block
            open(self.errorLogFileName, mode='w').close()

            self.cursor.execute(sqlCommand)
            self.conn.commit()
        except:
            # Print out that the SQL command execution has failed, and advise the user to examine the errors text file
            print(f'SQL command execution has failed. Check {self.errorLogFileName}.')

            # Open the file errors.txt and output the errors there
            with open(self.errorLogFileName, mode='w') as errorFile:
                errorFile.write(f'{sqlCommand}execution has failed.')