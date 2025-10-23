"""
The enumerate() function takes a collection (e.g. a tuple) and returns it as an enumerate object.
The enumerate() function adds a counter as the key of the enumerate object.
"""
# for index, char in enumerate('Devtalles'):
#    print(index, char)
#    """
#    0 D
#    1 e
#    2 v
#    3 t
#    4 a
#    5 l
#    6 l
#    7 e
#    8 s
#    """

# for index, number in enumerate([1, 2, 3, 4, 5]):
#    print(index, number)
#    """
#    0 1
#    1 2
#    2 3
#    3 4
#    4 5
#    """

for index, number in enumerate(list(range(50))):
    print(index, number)
    if number == 30:
        print("Aquí estoy")

x = ('apple', 'banana', 'cherry')
y = enumerate(x)

print(list(y))  # [(0, 'apple'), (1, 'banana'), (2, 'cherry')]
