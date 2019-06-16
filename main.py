import json
import requests
import re
from data_transfer import DataTransfer

# This function converts all string types (str) to VARCHAR(1000)
def convertStringToVarchar(string):
    pattern = r'\bstr\b'
    return re.sub(pattern, 'VARCHAR(1000)', string)

# This function returns quotations around the argument if it is a string
def insertQuotations(arg):
    if re.search(r'(?:[0-9]?\.[0-9]+|^[0-9]+$|true|false)', str(arg).lower()):
        return arg
    return f'\'{arg}\''

databaseName = input('Please input the database name you would like to store your information in.')
tableName = input('Please input the name you would like for your newly created table.')
url = input('Please input the url containing JSON contents')

# Get the url JSON contents in the inputted user url
url_contents = requests.get(url).json()

# Get the info of the first url content object and store them in a dictionary
propertyList = url_contents[0]

# Create a values string that is compatible with the SQL CREATE TABLE VALUES syntax
values = ''
for key, value in propertyList.items():
    values += f'\t{key} {type(value).__name__},\n'

# Remove the comma and newline at the end of values
values = values[:-2]

# Convert all str's to VARCHAR(1000) in values
values = convertStringToVarchar(values)

# Create the SQL command for creating the table
createTableCommand = f'''
CREATE TABLE {databaseName}.{tableName}
(
{values}
)
'''

# Start the connection with MYSQL
dataTransfer = DataTransfer('localhost', 3306, 'root', 'incorrect')

# Create the table
dataTransfer.insertData(createTableCommand)

############################## INSERT THE JSON DATA INTO THE TABLE ########################################

keys = ''

# Iterate through the url contents with index 0, getting the keys and separating them with commas
for key in propertyList:
    keys += f'{key}, '

# Remove the extra comma and whitespace at the end of keys
keys = keys[:-2]

# Iterate through the url_contents, getting their values and adding them in the MYSQL database
for data in url_contents:
    dictValue = ''
    for value in data.values():
        dictValue += f'{insertQuotations(value)}, '
    # Remove the comma and extra whitespace at the end of dictValue
    dictValue = dictValue[:-2]
    
    # Prepare the SQL statement
    insertDataStatement = f'''
    INSERT INTO {databaseName}.{tableName}({keys})
    VALUES ({dictValue})
    '''

    # Execute the statement
    dataTransfer.insertData(insertDataStatement)