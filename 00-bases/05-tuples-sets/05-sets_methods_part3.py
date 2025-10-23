
# .symmetric_difference, Return the symmetric difference of two sets as a new set.
# set1.symmetric_difference(set2)
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

symmetric_difference = set1.symmetric_difference(set2)
print(symmetric_difference)  # {1, 2, 5, 6}

# issubset, Test whether every element in the set is in other.
# set1.issubset(set2) True o False
set1 = {1, 2}
set2 = {1, 2, 3, 4}
print(set2.issubset(set1))  # False

# issuperset, Test whether every element in other is in the set
# set1.issuperset(set2)
set1 = {1, 2, 3, 4}
set2 = {1, 2}
print(set2.issuperset(set1))  # False
