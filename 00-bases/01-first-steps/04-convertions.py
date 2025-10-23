
value = 100
type_value = type(value)
# print(value)
# print(type_value) #<class 'int'>

# Int a Str
value = str(100) + 'Hola'
type_value = type(value)
# print(value)
# print(type_value)

# Str a Int
value = int('100')
type_value = type(value)
print(value)
print(type_value)

# Str a Float
value = float('100')
type_value = type(value)
print(value)
print(type_value)

# int a Float
value = float(100)
type_value = type(value)
print(value)  # 100.0
print(type_value)  # <class 'float'>
