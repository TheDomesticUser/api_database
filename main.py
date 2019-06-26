import json
import requests
import re
from data_transfer import DataTransfer

#    VALUES (10, 'Clementina DuBuque', 'Moriah.Stanton', 'Rey.Padberg@karina.biz', 
# '(Kattie Turnpike, Suite 198, Lebsackbury, 31428-2261, 
# (Kattie Turnpike, Suite 198, Lebsackbury, 31428-2261, (-38.2386, 57.2232))', '024-648-3804', 'ambrose.net', 
# '(Hoeger LLC, Centralized empowering task-force, target end-to-end models)')

# This function converts all string types (str), null values (NoneType), and dictionary types (dict) to VARCHAR 
# with a length depending on the variable type
def convertVarsToVarchar(string):
    string = re.sub(r'(?:\bstr\b|\bNoneType\b)', 'VARCHAR(150)', string)
    string = re.sub(r'\bdict\b', 'VARCHAR(2000)', string)

    return string

# This function returns quotations around the argument if it is a string or dictionary
def insertQuotations(arg):
    if re.search(r'(?:^[0-9]+\.[0-9]+$|^[0-9]+$|true|false)', str(arg).lower()) and \
        re.search(r'^[^(].+[^)]$', str(arg)):
        return arg
    return f'\'{arg}\''

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

# {
#     "address": {
#         "street": "Skiles Walks",
#         "suite": "Suite 351",
#         "city": "Roscoeview",
#         "zipcode": "33263",
#         "geo": {
#         "lat": "-31.8129",
#         "lng": "62.5342"
#         }
#     },
#     "phone": "(254)954-1289",
#     "website": "demarco.info",
#     "company": {
#         "name": "Keebler LLC",
#         "catchPhrase": "User-centric fault-tolerant solution",
#         "bs": "revolutionize end-to-end systems"
#     }
# }

databaseName = input('Please input the database name you would like to store your information in.\n')
tableName = input('Please input the name you would like for your newly created table.\n')
url = input('Please input the url containing JSON contents.\n')

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

# Convert all str's and dict's to VARCHAR(1000) in values
values = convertVarsToVarchar(values)

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
        dictValue += f'{insertQuotations(objectSeparator(value))}, '
    # Remove the comma and extra whitespace at the end of dictValue
    dictValue = dictValue[:-2]
    
    # Prepare the SQL statement
    insertDataStatement = f'''
    INSERT INTO {databaseName}.{tableName}({keys})
    VALUES ({dictValue})
    '''

    # Execute the statement
    dataTransfer.insertData(insertDataStatement)