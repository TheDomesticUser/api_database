import mysql.connector

class DataTransfer:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='incorrect')
        self.cursor = self.conn.cursor()
    def __del__(self):
        self.conn.close()
    def insertData(self, sqlCommand):
        try:
            self.cursor.execute(sqlCommand)
            self.conn.commit()
        except:
            print(f'Failed to execute SQL command: {sqlCommand}')