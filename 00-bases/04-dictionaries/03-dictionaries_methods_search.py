
user = {
    'name': 'Ricardo',
    'age': 29,
    'greet': 'Hola Mundo',
    'numbers': [1, 2, 3]
}

# .get(), Return the value for key if key is in the dictionary, else default (Nonw).
print(user.get('name'))
print(user.get('invalidKey', 'defaultValue'))

# in
# values(), an object providing a view on D's values
print(user.values())
# print('Ricardo' in user)
# print('Ricardo' in user.keys())
# print('Hola Ricardo' in user.values())

# items(), a set-like object providing a view on D's items
print(user.items())
