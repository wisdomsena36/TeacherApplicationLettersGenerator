# ASSIGNMENT 6
# 5-1. Conditional Tests: Write a series of conditional tests. Print a statement
# describing each test and your
# prediction for the results of each test. Your code should look something like this:
#
# car = 'subaru'
# print("Is car == 'subaru'? I predict True.")
# print(car == 'subaru')
# # print("\nIs car == 'audi'? I predict False.")
# print(car == 'audi')
# name = 'kofi'
# print(name == 'kofi')
# print(name == 'ama')
# print(name == name)
#
# •	 Look closely at your results, and make sure you understand why each line
# evaluates to True or False.
#
# •	 Create at least 10 tests. Have at least 5 tests evaluate to True and another
# 5 tests evaluate to False.
# print('kofi' == 'kofi')
# print('ama' == 'ama')
# print(23 == 23)
# print('car' == 'car')
# print('name' == 'Name')
# 13 ....<... 18
# age = 13
# if age >= 18:
#     print('You can vote')
# else:
#     print('You can not vote')
#
# 5-2. More Conditional Tests: You don’t have to limit the number of tests you
# create to 10. If you want to try more comparisons, write more tests and add them
# to conditional_tests.py. Have at least one True and one False result for each of the following:
# •	 Tests for equality and inequality with strings
#
# •	 Tests using the lower() function
#
# •	 Numerical tests involving equality and inequality, greater than and less than,
#   greater than or equal to, and less than or equal to
#
# •	 Tests using the and keyword and the or keyword
#
# •	 Test whether an item is in a list
#
# •	Test whether an item is not in a list

# mark = -89
#
# if mark >= 80:
#     print("A+")
# elif mark >= 79:
#     print("A-")
# elif mark >= 70:
#     print("B+")
# elif mark >= 60:
#     print("B")
# elif mark >= 50:
#     print("C")
# elif mark >= 49:
#     print("D")
# else:
#     print("F")

# numbers = [2, 4, 6, 8, 10]
#
# if 7 in numbers:
#     print('The number is in the list')
# else:
#     print('The number is not in the list')

# age = 16
# country = 'Ghana'
#
# if age >= 18 or country == 'Togo':
#     print('You can vote')
# else:
#     print('You can not vote')

# Dictionaries
# student = {'name': 'Kofi', 'age': 17, 'index no': 42112345, 'level': 300}
# print(student['name'])
# print(student['age'])
# print(student['index no'])
# print(student['level'])
#
# # student['level'] = 200
# # print(student['level'])
# student['program'] = "BSc IT"
# print(student)
# print('Name: ' + student['name'])
# print('Age: ', student['age'])
#
# del student['level']
# del student['name']
# print(student)

#Looping through a Dictionary
student = {'name': 'Kofi', 'age': 17, 'index no': 42112345, 'level': 300, 'grade': [76, 81, 90]}

for v in student['grade']:
    print(str(v))