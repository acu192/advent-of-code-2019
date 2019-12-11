
def never_decrease(i):
    l = len(i)
    for a, b in zip(i[0:l-1], i[1:]):
        if b < a:
            return False
    return True

def two_adjacent(i):
    i = [None] + list(i) + [None]
    l = len(i)
    for a, b, c, d in zip(i[0:l-3], i[1:l-2], i[2:l-1], i[3:]):
        if b == c and a != b and c != d:
            return True
    return False

c = 0

for i in range(197487, 673252):
    i = str(i)
    if never_decrease(i) and two_adjacent(i):
        c += 1

print(c)
