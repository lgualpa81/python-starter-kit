
# set1.union(set2)
set1 = {1, 2, 3}
set2 = {4, 5, 6}

# .union, Return the union of sets as a new set.
union_set = set1.union(set2)
print(union_set)  # {1, 2, 3, 4, 5, 6}

# .intersection, Return the intersection of two sets as a new set.
# set1.intersection(set2)
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
intersection = set1.intersection(set2)
print(intersection)  # {3, 4}

# .difference, Return the difference of two or more sets as a new set.
# set1.difference(set2)
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
difference = set2.difference(set1)
print(difference)  # {5, 6}
