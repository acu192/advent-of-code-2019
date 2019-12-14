
formulas = {}  # map name to (amt_produced, input_list)

with open('../27/input', 'rt') as f:
    for line in f:
        line = line.strip()
        in_, out = line.split(' => ')
        in_list = []
        for thing in in_.split(', '):
            amt, name = thing.split(' ')
            amt = int(amt)
            in_list.append((amt, name))
        amt, name = out.split(' ')
        amt = int(amt)
        assert name not in formulas
        formulas[name] = (amt, in_list)


print(formulas['FUEL'])


def solve(name, amount, excess):
    if name == 'ORE':
        return amount

    batch_size, in_list = formulas[name]
    batches = (amount + batch_size-1) // batch_size

    ore_total = 0

    for sub_amount, sub_name in in_list:
        if excess[sub_name] >= sub_amount * batches:
            ore_here = 0
            excess[sub_name] -= sub_amount * batches
        else:
            e = excess[sub_name]
            excess[sub_name] = 0
            ore_here = solve(sub_name, sub_amount * batches - e, excess)
        ore_total += ore_here

    excess[name] += batches * batch_size - amount

    return ore_total


from collections import defaultdict
import itertools


total_ore_we_have = 1000000000000


for i in itertools.count():  # find power-of-two range
    try_ = 2 ** i

    excess = defaultdict(int)

    total_ore = solve('FUEL', try_, excess)
    if total_ore > total_ore_we_have:
        min_, max_ = 2 ** (i-1), 2 ** i
        print('found range', min_, max_)
        break

    print(try_, total_ore)

    #print(excess)


while True:  # binary search!
    mid = (min_ + max_) // 2

    excess = defaultdict(int)

    total_ore = solve('FUEL', mid, excess)
    print(mid, 'FUEL requires', total_ore, 'ORE')

    if total_ore > total_ore_we_have:
        max_ = mid
    elif total_ore < total_ore_we_have:
        min_ = mid
    else:
        break

    if max_ - min_ <= 1:
        break

