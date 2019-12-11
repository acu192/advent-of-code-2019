with open('input', 'rt') as f:
    vals = [int(l) for l in f]

fuel = [val // 3 - 2 for val in vals]

print(sum(fuel))

