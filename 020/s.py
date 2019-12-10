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


def sort_slopes(slopes):
    a = [(y, x) for y, x in slopes if y < 0 and x >= 0]
    b = [(y, x) for y, x in slopes if y >= 0 and x > 0]
    c = [(y, x) for y, x in slopes if y > 0 and x <= 0]
    d = [(y, x) for y, x in slopes if y <= 0 and x < 0]

    assert len(a) + len(b) + len(c) + len(d) == len(slopes)

    def key(val):
        y, x = val
        if x != 0:
            return y / x
        else:
            return y * 9999999999

    a = sorted(a, key=lambda v: key(v))
    b = sorted(b, key=lambda v: key(v))
    c = sorted(c, key=lambda v: key(v))
    d = sorted(d, key=lambda v: key(v))

    c = c[-1:] + c[:-1]   # hack

    return a + b + c + d


with open('../019/input', 'rt') as f:
    galaxy = [list(l.strip()) for l in f.readlines()]


x_size = len(galaxy[0])
y_size = len(galaxy)

# A slope is y/x  (rise/run)
pos_slopes = set([reduce(y, x) for y in range(0, y_size+1) for x in range(0, x_size+1)])

slopes = set(list(pos_slopes) + [(-y, x) for y, x in pos_slopes] + [(y, -x) for y, x in pos_slopes] + [(-y, -x) for y, x in pos_slopes])  # !!!

slopes = sort_slopes(slopes)


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


def shoot(y, x, slope):
    while True:
        y += slope[0]
        x += slope[1]
        if y < 0 or y >= len(galaxy):
            return False, None, None
        if x < 0 or x >= len(galaxy[y]):
            return False, None, None
        if galaxy[y][x] == '#':
            galaxy[y][x] = '.'
            return True, y, x


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

_, best_y, best_x = max(counts)

count = 0

done = False

while not done:
    for slope in slopes:
        did_shoot, ay, ax = shoot(best_y, best_x, slope)
        if did_shoot:
            count += 1
            if count == 200:
                print(ay, ax, ax*100 + ay)
                done = True
                break

