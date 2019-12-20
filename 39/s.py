from collections import defaultdict, deque


with open('input', 'rt') as f:
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
            PORTAL_LOCS[portal].append((y, x-1))
        elif maze[y][x+2] == '.':
            PORTAL_LOCS[portal].append((y, x+2))
    elif maze[y+1][x] in ALPHA:
        portal = maze[y][x] + maze[y+1][x]
        maze[y][x] = ' '
        maze[y+1][x] = ' '
        if y > 0 and maze[y-1][x] == '.':
            PORTAL_LOCS[portal].append((y-1, x))
        elif maze[y+2][x] == '.':
            PORTAL_LOCS[portal].append((y+2, x))


for y, row in enumerate(maze):
    for x, c in enumerate(row):
        if c in ALPHA:
            record_portal(y, x)


COOR_TO_PORTAL = {coor: portal for portal, coor_list in PORTAL_LOCS.items() for coor in coor_list}


for row in maze:
    print(''.join(row))


START = PORTAL_LOCS['AA'][0]
END = PORTAL_LOCS['ZZ'][0]

print(START, END)


q = deque()
v = set()

q.append((START, 0))
v.add(START)

while len(q) > 0:
    (curr_y, curr_x), dist = q.popleft()

    if (curr_y, curr_x) == END:
        print('FOUND IT; dist =', dist)
        break

    if (curr_y, curr_x) in COOR_TO_PORTAL:
        portal_name = COOR_TO_PORTAL[(curr_y, curr_x)]
        other_locs = PORTAL_LOCS[portal_name]
        if len(other_locs) > 1:
            transport_loc = [loc for loc in other_locs if loc != (curr_y, curr_x)][0]
            if transport_loc not in v:
                q.append((transport_loc, dist+1))
                v.add(transport_loc)

    for dy, dx in DIRS:
        x = curr_x + dx
        y = curr_y + dy

        if (y, x) in v:
            continue

        if maze[y][x] == '.':
            q.append(((y, x), dist+1))
            v.add((y, x))

