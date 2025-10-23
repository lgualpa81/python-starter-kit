
x = [1, 2, 3]

print(type(x))  # <class 'list'>
print(dir(x))  # Show attributes of an object.
print(hasattr(x, '__len__'))  # True
print(getattr(x, 'append'))
# <built-in method append of list object at 0x7ba458dacb40>
print(callable(x.append))  # True
print(id(x))  # Return the identity of an object.
