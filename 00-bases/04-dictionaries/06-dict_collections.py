from collections import defaultdict, Counter
document = ["A", "paragraph", "is", "a", "group", "of", "sentences", "that",
            "are", "connected", "by", "a", "common", "theme", "idea", "or", "topic"]
# word_counts = {}
# for word in document:
#     word = word.lower()
#     if word in word_counts:
#         word_counts[word] += 1
#     else:
#         word_counts[word] = 1

# for word in document:
#     word = word.lower()
#     try:
#         word_counts[word] += 1
#     except KeyError:
#         word_counts[word] = 1

# for word in document:
#    word = word.lower()
#    previous_count = word_counts.get(word, 0)
#    word_counts[word] = previous_count + 1

# default dict
"""
Todo esto es muy poco manejable, razón por la cual defaultdict es útil.
Un defaultdict es como un diccionario normal, excepto que, cuando se
intenta buscar una clave que no contiene, primero añade un valor para ella
utilizando una función de argumento cero suministrada al crearla. Para
utilizar diccionarios defaultdicts, es necesario importarlos de collections
"""
# word_counts = defaultdict(int)
# int() produce 0
# for word in document:
#     word_counts[word] += 1
# print(word_counts)

# Counters
c = Counter([0, 1, 2, 0])
# print(c)  # Counter({0: 2, 1: 1, 2: 1})
# Convertimos todas las palabras a minúsculas
lowercased_document = [word.lower() for word in document]
word_counts = Counter(lowercased_document)

for word, count in word_counts.most_common():
    print(word, count)
