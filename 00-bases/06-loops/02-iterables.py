numbers = [1, 2, 3, 4, 5]

# Iterables: Iterables, Listas, Diccionarios, Set, Tuplas
# Iterador: Objeto que recuerda su posición

# for number in numbers:
#     print(number)
iterator = iter(numbers)
print(iterator)  # <list_iterator object at 0x752b0f9e8370>
# next, Return the next item from the iterator.
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
print(next(iterator))  # 4
print(next(iterator))  # 5
# print(next(iterator))  # exception StopIteration

user = {
    'name': 'Ricardo',
    'age': 22,
    'can_swim': False
}

for key, value in user.items():
    print(key, value)
