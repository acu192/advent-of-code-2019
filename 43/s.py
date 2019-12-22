from collections import defaultdict
from itertools import count


steps = []


with open('input', 'rt') as f:
    for line in f:
        line = line.strip()
        params = line.split(' ')
        if line.startswith('cut'):
            steps.append(('cut', int(params[-1])))
        elif line.startswith('deal into'):
            steps.append(('reverse', None))
        elif line.startswith('deal with'):
            steps.append(('inc', int(params[-1])))
        else:
            assert False


#steps = [('cut', 6), ('inc', 7), ('reverse', None)]


cards = list(range(10007))
#cards = list(range(10))

for step, n in steps:
    if step == 'cut':
        cards = cards[n:] + cards[:n]

    elif step == 'reverse':
        cards = cards[::-1]

    elif step == 'inc':
        cards_copy = cards[:]
        for i, c in enumerate(cards_copy):
            p = (i * n) % len(cards)
            cards[p] = c

for i, c in enumerate(cards):
    if c == 2019:
        print(i)

