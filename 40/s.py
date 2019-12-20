from collections import defaultdict, deque


with open('../39/input', 'rt') as f:             # <-- also try 'input3' for debugging
    maze = [list(l.strip('\n')) for l in f]


for row in maze:
    print(''.join(row))


ALPHA = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


PORTAL_LOCS = defaultdict(list)


DIRS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]


def record_portal(y, x):
    if maze[y][x+1] in ALPHA:
        portal = maze[y][x] + maze[y][x+1]
        maze[y][x] = ' '
        maze[y][x+1] = ' '
        if x > 0 and maze[y][x-1] == '.':
            side = 'outer' if x+2 >= len(maze[y]) else 'inner'
            PORTAL_LOCS[portal].append((y, x-1, side))
        elif maze[y][x+2] == '.':
            side = 'outer' if x == 0 else 'inner'
            PORTAL_LOCS[portal].append((y, x+2, side))
    elif maze[y+1][x] in ALPHA:
        portal = maze[y][x] + maze[y+1][x]
        maze[y][x] = ' '
        maze[y+1][x] = ' '
        if y > 0 and maze[y-1][x] == '.':
            side = 'outer' if y+2 >= len(maze) else 'inner'
            PORTAL_LOCS[portal].append((y-1, x, side))
        elif maze[y+2][x] == '.':
            side = 'outer' if y == 0 else 'inner'
            PORTAL_LOCS[portal].append((y+2, x, side))


for y, row in enumerate(maze):
    for x, c in enumerate(row):
        if c in ALPHA:
            record_portal(y, x)


COOR_TO_PORTAL = {(y, x): (portal, side) for portal, coor_list in PORTAL_LOCS.items() for y, x, side in coor_list}


for row in maze:
    print(''.join(row))


START = (PORTAL_LOCS['AA'][0][:2], 0)   # (y, x), level
END   = (PORTAL_LOCS['ZZ'][0][:2], 0)   # (y, x), level

print(START, END)


q = deque()
v = set()

q.append((START, 0))   # ((y, x), level), dist
v.add(START)           # (y, x), level

prev = {}              # map to the previous location

while len(q) > 0:
    ((curr_y, curr_x), level), dist = q.popleft()

    assert maze[curr_y][curr_x] == '.'

    if ((curr_y, curr_x), level) == END:
        break

    if (curr_y, curr_x) in COOR_TO_PORTAL:
        portal_name, portal_side = COOR_TO_PORTAL[(curr_y, curr_x)]

        portal_works = True
        if level == 0 and portal_side == 'outer':
            portal_works = False

        if portal_works:
            other_locs = PORTAL_LOCS[portal_name]
            if len(other_locs) > 1:
                not_me_locs = [loc for loc in other_locs if loc[:2] != (curr_y, curr_x)]
                assert len(not_me_locs) == 1
                next_y, next_x, next_side = not_me_locs[0]
                next_level = (level + 1) if portal_side == 'inner' else (level - 1)
                next_loc = ((next_y, next_x), next_level)
                if next_loc not in v:
                    q.append((next_loc, dist+1))
                    v.add(next_loc)
                    prev[next_loc] = ((curr_y, curr_x), level)

    for dy, dx in DIRS:
        x = curr_x + dx
        y = curr_y + dy

        loc = ((y, x), level)

        if loc in v:
            continue

        if maze[y][x] == '.':
            q.append((loc, dist+1))
            v.add(loc)
            prev[loc] = ((curr_y, curr_x), level)


steps = [END]

while True:
    s = steps[-1]
    if s not in prev:
        break
    p = prev[s]
    steps.append(p)

steps = steps[::-1]

print('STEPS TAKEN ((y, x), level)')

for s in steps:
    print(s)

print(len(steps) - 1, 'total steps')

