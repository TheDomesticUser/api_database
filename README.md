# api_database
How the program works:
1. User is prompted by the program to input the name of the database they would like to create
2. User is prompted by the program to input a web link containing JSON data
3. Program grabs all of the JSON contents, storing them in a variable for manipulation
4. A MYSQL database with the inputted name and its property values is created

The program calculates the length of each key that is a string/dictionary with the highest amount of characters, and is used as the VARCHAR length upon declaration in the CREATE TABLE syntax.

All functions are at the beginning of main.py