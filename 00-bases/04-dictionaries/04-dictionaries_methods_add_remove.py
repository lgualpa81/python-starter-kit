
user = {
    'name': 'Ricardo',
    'age': 29,
    'greet': 'Hola Mundo',
    'numbers': [1, 2, 3]
}

# .copy(), a shallow copy of D

user_copy = user.copy()
user_copy['age'] = 20
print("user", user)
print("user_copy", user_copy)

# .pop(), remove specified key and return the corresponding value.
user.pop('age')
print("pop", user)

# .popitem()
user.popitem()
print("popitem", user)

# .update()
user.update({'name': 'Fernando'})
user.update({'cats': 2})
print("update", user)

# .append()
user['skills'] = user.get('skills', [])
user['skills'].append('Python')
user['skills'].append('Django')
print("append", user)
