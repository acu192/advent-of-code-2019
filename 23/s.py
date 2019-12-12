moons = [
        dict(x=14, y=4, z=5, vx=0, vy=0, vz=0),
        dict(x=12, y=10, z=8, vx=0, vy=0, vz=0),
        dict(x=1, y=7, z=-10, vx=0, vy=0, vz=0),
        dict(x=16, y=-5, z=3, vx=0, vy=0, vz=0),
]


#moons = [
#        dict(x=-1, y=0, z=2, vx=0, vy=0, vz=0),
#        dict(x=2, y=-10, z=-7, vx=0, vy=0, vz=0),
#        dict(x=4, y=-8, z=8, vx=0, vy=0, vz=0),
#        dict(x=3, y=5, z=-1, vx=0, vy=0, vz=0),
#]


import itertools


def step():
    for m1, m2 in itertools.combinations(moons, 2):
        m1['vx'] += (1 if m1['x'] < m2['x'] else -1) if m1['x'] != m2['x'] else 0
        m2['vx'] += (1 if m1['x'] > m2['x'] else -1) if m1['x'] != m2['x'] else 0
        m1['vy'] += (1 if m1['y'] < m2['y'] else -1) if m1['y'] != m2['y'] else 0
        m2['vy'] += (1 if m1['y'] > m2['y'] else -1) if m1['y'] != m2['y'] else 0
        m1['vz'] += (1 if m1['z'] < m2['z'] else -1) if m1['z'] != m2['z'] else 0
        m2['vz'] += (1 if m1['z'] > m2['z'] else -1) if m1['z'] != m2['z'] else 0

    for m1 in moons:
        m1['x'] += m1['vx']
        m1['y'] += m1['vy']
        m1['z'] += m1['vz']


for i in range(1000):
    step()


t = 0

for m in moons:
    pot = abs(m['x']) + abs(m['y']) + abs(m['z'])
    kin = abs(m['vx']) + abs(m['vy']) + abs(m['vz'])
    t += pot * kin

print(moons)

print(t)

