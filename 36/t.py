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

    robot_locs = tuple([(x, y) for y, row in enumerate(m) for x, val in enumerate(row) if m[y][x] == '@'])

    for x, y in robot_locs:
        m[y][x] = '.'

    n_keys = len([(kx, ky) for ky, row in enumerate(m) for kx, val in enumerate(row) if m[ky][kx] in KEYS])

    print('Final answer:', bfs(m, robot_locs, n_keys))


def bfs(m, robot_locs, n_keys):
    q = deque()
    visited = set()

    active_robot = -1   # -1 means that any robot may become active; else it will be a robot index

    q.append((robot_locs, 0, (), active_robot))   # curr_robot_locations, curr_dist, curr_set_of_found_keys, active_robot
    visited.add((robot_locs, (), active_robot))   # curr_robot_locations, having_this_set_of_keys, active_robot

    while len(q) > 0:

        robot_locs, dist, keys_so_far, active_robot = q.popleft()

        if active_robot == -1:
            # Any robot may become active, so move them all one step (and thereby declaring the one that moves "active").
            robots_to_move = enumerate(robot_locs)

        else:
            # We have a known active robot, so move it only:
            robots_to_move = [(active_robot, robot_locs[active_robot])]

        for i, (x, y) in robots_to_move:

            for dx, dy in DIRS:

                nx = x + dx  # "new x"
                ny = y + dy  # "new y"

                v = m[ny][nx]

                if v == '#':
                    continue

                robot_locs_new = list(robot_locs)
                robot_locs_new[i] = (nx, ny)
                robot_locs_new = tuple(robot_locs_new)

                v_key = (robot_locs_new, keys_so_far, i)

                if (v == '.' or v.lower() in keys_so_far or v in keys_so_far) and v_key not in visited:
                    # We hit a new '.', or we hit a door we can open, or we hit a key we already picked up.
                    # ... and we haven't visited this particulare state-of-the-world yet.
                    visited.add(v_key)
                    q.append((robot_locs_new, dist+1, keys_so_far, i))

                elif v in KEYS and v not in keys_so_far:
                    # We found a new key!
                    # For the next step, any robot may become active (i.e. we put -1 as the active_robot).
                    keys_so_far_here = tuple(sorted(keys_so_far + (v,)))
                    v_key = (robot_locs_new, keys_so_far_here, -1)
                    visited.add(v_key)
                    q.append((robot_locs_new, dist+1, keys_so_far_here, -1))
                    if len(keys_so_far_here) == n_keys:
                        return dist+1  # WE'RE DONE

    return 99999999999999


if __name__ == '__main__':
    run()

