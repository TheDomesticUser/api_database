import mysql.connector

class DataTransfer:
    def __init__(self, hostInput, portInput, userInput, passwordInput):
        self.conn = mysql.connector.connect(host=hostInput, port=portInput, user=userInput, password=passwordInput)
        self.cursor = self.conn.cursor()
    def __del__(self):
        self.conn.close()
    def insertData(self, sqlCommand):
        try:
            self.cursor.execute(sqlCommand)
            self.conn.commit()
        except:
            print(f'{sqlCommand}execution has failed.')