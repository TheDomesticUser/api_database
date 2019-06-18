import requests

def objectSeparator(val, string=''):
    if type(val).__name__ == 'dict':
        # Iterate each of the values in the object
        string += f'{val.keys[0]} {val.values[0]}'
    return string

url_contents = requests.get('https://api.github.com/users').json()[0]

for key, value in url_contents.items():
    print(key, value)