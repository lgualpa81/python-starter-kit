"""
Unpacking lists in Python is a feature that allows us to extract values from a list into 
variables or other data structures. This technique is useful for various situations, 
including assignments, function arguments and iteration. 
"""
# Unpacking list elements into variables
# Python 3 introduced the * operator, which enables us to capture multiple values in one variable.
# This is especially useful when we don't know the exact number of elements in the list or
# when we only want to extract a few elements.
a, b, c, d, *other, e = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print(a)  # 1
print(b)  # 2
print(c)  # 3
print(d)  # 4
print(other)  # [5, 6, 7, 8]
print(e)  # 9

# Unpacking Nested Lists
# We can also unpack lists that contain nested lists (lists within lists).
# The same unpacking rules apply but we may need to unpack multiple levels of nesting.
# Nested list
li = [1, [2, 3], 4]

# Unpacking nested list
a, (b, c), d = li

print(a)
print(b)
print(c)
print(d)

"""
Packing
A menudo, necesitaremos empaquetar (zip) dos o más iterables juntos. La
función zip transforma varios iterables en uno solo de tuplas de función
correspondiente
NOTA: Si las listas tienen distintas longitudes, zip se detiene tan pronto como
termina la primera lista.
"""
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]
zipped = [pair for pair in zip(list1, list2)]
print(zipped)  # [('a', 1), ('b', 2), ('c', 3)]

# desempaquetar
pairs = [("a", 1), ("b", 2), ("c", 3)]
letters, numbers = zip(*pairs)
print(letters, numbers)  # ('a', 'b', 'c') (1, 2, 3)
