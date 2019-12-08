with open('../001/input', 'rt') as f:
    vals = [int(l) for l in f]


def calc(val):
    fuel = val // 3 - 2
    total = fuel
    while fuel > 0:
        fuel = fuel // 3 - 2
        if fuel > 0:
            total += fuel
    return total


fuel = [calc(val) for val in vals]

print(sum(fuel))

