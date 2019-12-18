from collections import deque


KEYS = set('abcdefghijklmnopqrstuvwxyz')

DIRS = [
    (-1, 0),  # dx, dy
    (1, 0),   # dx, dy
    (0, -1),  # dx, dy
    (0, 1),   # dx, dy
]


def run():
    with open('input', 'rt') as f:
        m = [list(line.strip()) for line in f]

    for row in m:
        print(''.join(row))
    print('\n\n')

    x, y = [(x, y) for y, row in enumerate(m) for x, val in enumerate(row) if m[y][x] == '@'][0]

    m[y][x] = '.'

    n_keys = len([(kx, ky) for ky, row in enumerate(m) for kx, val in enumerate(row) if m[ky][kx] in KEYS])

    print('Final answer:', bfs(m, x, y, n_keys))


def bfs(m, x, y, n_keys):
    q = deque()
    visited = set()

    q.append((x, y, 0, ()))   # curr_x, curr_y, curr_dist, curr_set_of_found_keys
    visited.add((x, y, ()))   # seen_x, seen_y, having_this_set_of_keys

    while len(q) > 0:

        x, y, dist, keys_so_far = q.popleft()

        for dx, dy in DIRS:

            nx = x + dx  # "new x"
            ny = y + dy  # "new y"

            v = m[ny][nx]

            v_key = (nx, ny, keys_so_far)

            if (v == '.' or v.lower() in keys_so_far or v in keys_so_far) and v_key not in visited:
                # We hit a new '.', or we hit a door we can open, or we hit a key we already picked up.
                # ... and we haven't visited this particulare state-of-the-world yet.
                visited.add(v_key)
                q.append((nx, ny, dist+1, keys_so_far))

            elif v in KEYS and v not in keys_so_far:
                # We found a new key!
                keys_so_far_here = tuple(sorted(keys_so_far + (v,)))
                v_key = (nx, ny, keys_so_far_here)
                visited.add(v_key)
                q.append((nx, ny, dist+1, keys_so_far_here))
                if len(keys_so_far_here) == n_keys:
                    return dist+1  # WE'RE DONE

    return 99999999999999


if __name__ == '__main__':
    run()

