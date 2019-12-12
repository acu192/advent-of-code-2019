moons = [
        dict(x=14, y=4, z=5, vx=0, vy=0, vz=0),
        dict(x=12, y=10, z=8, vx=0, vy=0, vz=0),
        dict(x=1, y=7, z=-10, vx=0, vy=0, vz=0),
        dict(x=16, y=-5, z=3, vx=0, vy=0, vz=0),
]


import itertools


def find_cycle_len(moons_1d):
    orig = [m['x'] for m in moons_1d]

    for i in itertools.count():

        for m1, m2 in itertools.combinations(moons_1d, 2):
            m1['vx'] += (1 if m1['x'] < m2['x'] else -1) if m1['x'] != m2['x'] else 0
            m2['vx'] += (1 if m1['x'] > m2['x'] else -1) if m1['x'] != m2['x'] else 0

        for m in moons_1d:
            m['x'] += m['vx']

        for m in moons_1d:
            if m['vx'] != 0:
                break
        else:   # no break
            now = [m['x'] for m in moons_1d]
            if orig == now:
                return i + 1


moons_1d_x = [{'x': m['x'], 'vx': m['vx']} for m in moons]
moons_1d_y = [{'x': m['y'], 'vx': m['vy']} for m in moons]
moons_1d_z = [{'x': m['z'], 'vx': m['vz']} for m in moons]

cycle_x = find_cycle_len(moons_1d_x)
print('cycle x', cycle_x)

cycle_y = find_cycle_len(moons_1d_y)
print('cycle y', cycle_y)

cycle_z = find_cycle_len(moons_1d_z)
print('cycle z', cycle_z)


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def lcm(a, b):
    return a * b / gcd(a, b)

print(lcm(lcm(cycle_x, cycle_y), cycle_z))

