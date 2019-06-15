import json
import requests
from data_transfer import DataTransfer

databaseName = input('Please input the database name.')
url = input('Please input the url containing JSON contents')

# Get the url contents in the inputted url JSON details
url_contents = requests.get(url).json()

# Append all of the url content properties into a list
propertyList = [key for key in url_contents[0]]

# Initialize an DataTransfer object, starting a connection with MYSQL
dataTransfer = DataTransfer()

# # Create a table
# createTableCommand = f'''
# CREATE TABLE {databaseName}
# VALUES
# (

# )
# '''

print(propertyList)