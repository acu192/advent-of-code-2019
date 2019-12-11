
def never_decrease(i):
    l = len(i)
    for a, b in zip(i[0:l-1], i[1:]):
        if b < a:
            return False
    return True

def two_adjacent(i):
    l = len(i)
    for a, b in zip(i[0:l-1], i[1:]):
        if a == b:
            return True
    return False

c = 0

for i in range(197487, 673252):
    i = str(i)
    if never_decrease(i) and two_adjacent(i):
        c += 1

print(c)
