import json
import requests
import re
from data_transfer import DataTransfer

# This function converts all string types (str), null values (NoneType), and dictionary types (dict) to VARCHAR 
# with a length depending on the variable type
def convertVarsToVarchar(string):
    string = re.sub(r'(?:\bstr\b|\bNoneType\b)', 'VARCHAR(150)', string) # The VARCHAR length can be any value
    string = re.sub(r'\bdict\b', 'VARCHAR(2000)', string) # The VARCHAR length can be any value

    return string

# This function adds a backslash to every single quotation in the string. Used in the insertQuotations(arg) function
def insertBackslashToSingleQuotation(string):
    buffer = ''
    for char in string:
        if char == '\'':
            buffer += '\\'
        buffer += char
    return buffer

# This function returns quotations around the argument if it is a string or dictionary
def insertQuotations(arg):
    if re.search(r'(?:^[0-9]+\.[0-9]+$|^[0-9]+$|true|false)', str(arg).lower()) and \
        re.search(r'^[^(].+[^)]$', str(arg)):
        return arg
    return f'\'{insertBackslashToSingleQuotation(str(arg))}\''

# This function takes the nested object inside the parent object and separates each of the properties through commas
def objectSeparator(val, string=''):
    if type(val).__name__ == 'dict':
        string += '('
        
        # Iterate through each of the value s in the dictionary, checking if they are also a dictionary
        for keyIter, valueIter in val.items():
            string += f'{keyIter}: {objectSeparator(valueIter)}, '
        
        # Remove the extra whitespace and comma at the end
        string = string[:-2]
        string += ')'
    else:
        return val
    return string

databaseName = input('Please input the database name you would like to store your information in.\n')
tableName = input('Please input the name you would like for your newly created table.\n')
url = input('Please input the url containing JSON contents.\n')

# Get the url JSON contents in the inputted user url
url_contents = requests.get(url).json()

###################################### CREATE THE TABLE #######################################################

values = ''
keySet = set()

# Iterate through the dictionaries inside the list, and appending their keys to the key list set
for dictionary in url_contents:
    for key in dictionary:
        keySet.add(key)
print(keySet)
# # Iterate through the key sets, appending the key name and type of the key to the value string


# # Remove the comma and newline at the end of values
# values = values[:-2]

# # Convert all str's and dict's to VARCHAR(1000) in values
# values = convertVarsToVarchar(values)

# # Create the SQL command for creating the table
# createTableCommand = f'''
# CREATE TABLE {databaseName}.{tableName}
# (
# {values}
# )
# '''

# # Start the connection with MYSQL
# dataTransfer = DataTransfer('localhost', 3306, 'root', 'incorrect')

# # Create the table
# dataTransfer.insertData(createTableCommand)

# ############################## INSERT THE JSON DATA INTO THE TABLE ########################################

# keys = ''

# # Iterate through the url contents with index 0, getting the keys and separating them with commas
# for key in propertyList:
#     keys += f'{key}, '

# # Remove the extra comma and whitespace at the end of keys
# keys = keys[:-2]

# # Iterate through the url_contents, getting their values and adding them in the MYSQL database
# for data in url_contents:
#     dictValue = ''
#     for value in data.values():
#         dictValue += f'{insertQuotations(objectSeparator(value))}, '
#     # Remove the comma and extra whitespace at the end of dictValue
#     dictValue = dictValue[:-2]
    
#     # Prepare the SQL statement
#     insertDataStatement = f'''
#     INSERT INTO {databaseName}.{tableName}({keys})
#     VALUES ({dictValue})
#     '''

#     # Execute the statement
#     dataTransfer.insertData(insertDataStatement)