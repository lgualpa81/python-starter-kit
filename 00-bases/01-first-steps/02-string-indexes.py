name = "Ricardo"
# print(name)  # Ricardo

# print(name[0])  # R
# print(name[1])  # i
# ...
# print(name[6])  # o

# Luis name[3]

# ¿Cómo obtener la última letra?
# print(name[-1])

# [Start:Stop] #El Stop no lo incluye
# Ricardo
# Ric
# print(name[0:3])

# [Start:Stop:stepover]
# Rc
# print(name[0:3:2])

# ¿Cómo puedo poner mi nombre al revés?
# [Start:Stop:stepover]
name_reverse = name[::-1]
print(name_reverse)
