
list1 = [1, 2, 3, 4, 2, 3, 4, 5, 1, 2, 5, 6, 2, 4, 9, 10]
tuple1 = tuple(list1)
print(list1)  # [1, 2, 3, 4, 2, 3, 4, 5, 1, 2, 5, 6, 2, 4, 9, 10]
print(tuple1)  # (1, 2, 3, 4, 2, 3, 4, 5, 1, 2, 5, 6, 2, 4, 9, 10)

set1 = set(tuple1)
print(set1)  # {1, 2, 3, 4, 5, 6, 9, 10}


list_tuple = [('a', 1), ('b', 2), ('c', 3)]
dictionary = dict(list_tuple)
print(dictionary)  # {'a': 1, 'b': 2, 'c': 3}
