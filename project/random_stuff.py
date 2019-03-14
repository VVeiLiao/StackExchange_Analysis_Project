from collections import Counter
dict_1 = {'a' : 10, 'b' : 10, 'c' : 1}
dict_2 = {'a' : 5, 'b' : 5, 'd' : 1}
dict_3 = Counter(dict_1)
dict_3 = Counter(dict_3) + Counter(dict_2)

print(str(dict_3))
print(dict_3['a'])