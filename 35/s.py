from collections import deque


CAN_VISIT = set('.abcdefghijklmnopqrstuvwxyz')

KEYS = set('abcdefghijklmnopqrstuvwxyz')

DOORS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

DIRS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]



def run():
    with open('input', 'rt') as f:
        m = [list(line.strip()) for line in f]

    x, y = [(x, y) for y, row in enumerate(m) for x, val in enumerate(row) if m[y][x] == '@'][0]

    for row in m:
        print(''.join(row))
    print('\n\n')

    close_dead_ends(m)   # Not required, but makes things faster.

    for row in m:
        print(''.join(row))
    print('\n\n')

    m[y][x] = '.'

    key_locs = set([(kx, ky) for ky, row in enumerate(m) for kx, val in enumerate(row) if m[ky][kx] in KEYS])

    door_locs = {m[dy][dx].lower(): (dx, dy) for dy, row in enumerate(m) for dx, val in enumerate(row) if m[dy][dx] in DOORS}

    print('Final answer:', solve_full_search(m, x, y, key_locs, door_locs, 0, 9999999999999999, [None], {}))


def is_dead_end(m, x, y):
    closed = sum(1 if m[y+dy][x+dx] == '#' else 0 for dx, dy in DIRS)
    return closed == 3


def close_dead_ends(m):
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            if val == '.' and is_dead_end(m, x, y):
                close_em(m, x, y)


def close_em(m, x, y):
    m[y][x] = '#'

    for dx, dy in DIRS:
        if m[y+dy][x+dx] == '.':
            if is_dead_end(m, x+dx, y+dy):
                close_em(m, x+dx, y+dy)


def solve_full_search(m, x, y, key_locs, door_locs, dist_here, min_so_far, curr_key_order, cache):
    if len(key_locs) == 0:
        return dist_here

    most_recent = curr_key_order[-1]

    cache_key = (most_recent,) + tuple(sorted(key_locs))

    if cache_key in cache:
        #print('Using cache', cache_key, cache[cache_key])
        return dist_here + cache[cache_key]

    avail_keys = find_keys(m, x, y)   # They'll come back sorted by distance already.

    min_on_this_path = 999999999999999

    for i, (k, kx, ky, key_dist) in enumerate(avail_keys):
        #if dist_here + key_dist >= min_so_far:   <--- BREAKS THE CACHE; DON'T DO THIS
        #    break
        m[ky][kx] = '.'
        if k in door_locs:
            dx, dy = door_locs[k]
            m[dy][dx] = '.'
        key_locs.remove((kx, ky))
        curr_key_order.append((kx, ky))
        val_here = solve_full_search(m, kx, ky, key_locs, door_locs, dist_here + key_dist, min_so_far, curr_key_order, cache)
        key_locs.add((kx, ky))
        curr_key_order.pop()
        if val_here < min_so_far:
            min_so_far = val_here
            print('NEW MIN', min_so_far)
        if val_here < min_on_this_path:
            min_on_this_path = val_here
        m[ky][kx] = k
        if k in door_locs:
            dx, dy = door_locs[k]
            m[dy][dx] = k.upper()

    cache[cache_key] = min_on_this_path - dist_here
    #print('Cached', cache_key, min_on_this_path - dist_here)
    return min_on_this_path


def find_keys(m, x, y):
    q = deque()
    visited = set()

    q.append((x, y, 0))
    visited.add((x, y))

    avail_keys = []

    while len(q) > 0:

        x, y, dist = q.popleft()

        if m[y][x-1] in CAN_VISIT and (x-1, y) not in visited:
            visited.add((x-1, y))
            if m[y][x-1] in KEYS:
                k = m[y][x-1]
                avail_keys.append((k, x-1, y, dist+1))
            else:
                q.append((x-1, y, dist+1))

        if m[y][x+1] in CAN_VISIT and (x+1, y) not in visited:
            visited.add((x+1, y))
            if m[y][x+1] in KEYS:
                k = m[y][x+1]
                avail_keys.append((k, x+1, y, dist+1))
            else:
                q.append((x+1, y, dist+1))

        if m[y-1][x] in CAN_VISIT and (x, y-1) not in visited:
            visited.add((x, y-1))
            if m[y-1][x] in KEYS:
                k = m[y-1][x]
                avail_keys.append((k, x, y-1, dist+1))
            else:
                q.append((x, y-1, dist+1))

        if m[y+1][x] in CAN_VISIT and (x, y+1) not in visited:
            visited.add((x, y+1))
            if m[y+1][x] in KEYS:
                k = m[y+1][x]
                avail_keys.append((k, x, y+1, dist+1))
            else:
                q.append((x, y+1, dist+1))

    return avail_keys


if __name__ == '__main__':
    run()

