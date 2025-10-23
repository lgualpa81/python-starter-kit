from typing import List
Vector = List[float]

numbers = list(range(20))  # 0..19
print(numbers)
# join, Concatenate any number of strings.
sentence = ' '.join(['Hola', 'Mundo', 'desde', 'un', 'join'])
print(sentence)
total = sum(numbers)
mayor = max(numbers)
menor = min(numbers)
elements = len(numbers)

print(total, mayor, menor, elements)

# list comprehension
"""
Con frecuencia, vamos a querer transformar una lista en otra distinta
seleccionando solo determinados elementos, transformando elementos o
haciendo ambas cosas. La forma pitónica de hacer esto es con list
comprehensions, o comprensiones de listas:
"""
even_numbers = [x for x in range(5) if x % 2 == 0]  # [0, 2, 4]
squares = [x * x for x in range(5)]  # [0, 1, 4, 9, 16]
even_squares = [x * x for x in even_numbers]  # [0, 4, 16]

print(even_numbers, squares, even_numbers)

square_dict = {x: x * x for x in range(5)}
print(square_dict)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
square_set = {x * x for x in [1, -1]}
print(square_set)  # {1}

# Si no necesitamos el valor de la lista, es habitual utilizar un guion bajo como variable:
zeros = [0 for _ in even_numbers]
print(zeros)  # [0, 0, 0]

# Una comprensión de lista puede incluir varios for:
pairs = [
    (x, y)
    for x in range(5)
    for y in range(5)
]
# [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), ... (4, 2), (4, 3), (4, 4)]
print(pairs)

# Queremos todos los pares (x, y) de dos listas, pero solo si la suma es par.
X = [1, 2, 3]
Y = [4, 5, 6]

print([(x, y) for x in X for y in Y if (x + y) % 2 == 0])
# [(1, 5), (2, 4), (2, 6), (3, 5)]

# Transponer matriz
matriz = [
    [1, 2, 3],
    [4, 5, 6]
]
print([[fila[i] for fila in matriz] for i in range(len(matriz[0]))])
# [
#    [1, 4],
#    [2, 5],
#    [3, 6]
# ]

# sumar vectores sin sum
v1 = [1, 2, 3]
v2 = [4, 5, 6]
print([a + b for a, b in zip(v1, v2)])
# [5, 7, 9]

# matriz identidad nxn
n = 4
print([[1 if i == j else 0 for j in range(n)] for i in range(n)])

# [
#    [1, 0, 0, 0],
#    [0, 1, 0, 0],
#    [0, 0, 1, 0],
#    [0, 0, 0, 1]
# ]


def dot(v: Vector, w: Vector) -> float:
    """Computes v_1 * w_1 + ... + v_n * w_n"""
    # assert len(v) == len(w), "vectors must be same length"
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


print(dot([1, 2, 3], [4, 5, 6]))  # 1 * 4 + 2 * 5 + 3 * 6 = 32
