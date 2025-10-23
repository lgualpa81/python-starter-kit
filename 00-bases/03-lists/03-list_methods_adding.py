
# Métodos de adición

numbers_list = [1, 2, 3, 4, 5]
print(numbers_list)
# append, Append object to the end of the list.
numbers_list.append(100)
numbers_list.append(200)
print("append", numbers_list)
# Insert, Insert object before index.
numbers_list.insert(1, 200)
numbers_list.insert(3, 300)

print("insert", numbers_list)

# Extend,  is used to add all elements from an iterable to the end of a list, modifying the original list in place.
numbers_list.extend([11, 22, 33])

print("extend", numbers_list)
