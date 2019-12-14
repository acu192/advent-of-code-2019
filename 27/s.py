
formulas = {}  # map name to (amt_produced, input_list)

with open('input', 'rt') as f:
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

excess = defaultdict(int)

total_ore = solve('FUEL', 1, excess)

print(total_ore)

print(excess)

