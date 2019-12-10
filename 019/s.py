def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def reduce(a, b):
    if a == 0:
        return 0, 1
    if b == 0:
        return 1, 0
    c = gcd(a, b)
    return a // c, b // c


with open('input', 'rt') as f:
    galaxy = [l.strip() for l in f.readlines()]


x_size = len(galaxy[0])
y_size = len(galaxy)

# A slope is y/x  (rise/run)
pos_slopes = set([reduce(y, x) for y in range(0, y_size+1) for x in range(0, x_size+1)])

slopes = set(list(pos_slopes) + [(-y, x) for y, x in pos_slopes] + [(y, -x) for y, x in pos_slopes] + [(-y, -x) for y, x in pos_slopes])  # !!!


def can_see(y, x, slope):
    while True:
        y += slope[0]
        x += slope[1]
        if y < 0 or y >= len(galaxy):
            return False
        if x < 0 or x >= len(galaxy[y]):
            return False
        if galaxy[y][x] == '#':
            return True


counts = []

for y in range(y_size):
    for x in range(x_size):
        if galaxy[y][x] != '#':
            continue
        count = 0
        for slope in slopes:
            if can_see(y, x, slope):
                count += 1
        counts.append((count, y, x))

print(max(counts))

#print(counts)

