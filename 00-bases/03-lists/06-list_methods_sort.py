
letters = ['a', 'b', 'm', 'o', 'c', 'z', 'g', 'd', 'e']
print(letters)
# sort(), Sort the list in ascending order and return None.
letters.sort()

# sorted(), Return a new list containing all items from the iterable in ascending order.
new_letters = sorted(letters)
print(new_letters)
# print(new_letters)
# print(new_letters)

# new_letters = letters[:]  # List Slicing
# copy(), Return a shallow copy of the list.
new_letters = letters.copy()
new_letters.sort()

# Reverse
letters.reverse()
print(letters)
