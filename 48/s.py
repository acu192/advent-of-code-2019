game = """
##.#.
.#.##
.#?..
#..#.
.##.."""

empty_game = """
.....
.....
..?..
.....
....."""



game = [list(line) for line in game.strip().split('\n')]

empty_game = [list(line) for line in empty_game.strip().split('\n')]

levels = {0: game}

for i in range(1, 301):
    levels[i] = empty_game
    levels[-i] = empty_game

del game
del empty_game


dirs = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]


def step(levels):
    new = {k: [list(row) for row in game] for k, game in levels.items()}

    for k, game in levels.items():
        if k < -201 or k > 201:   # HACK
            continue

        for y, row in enumerate(game):
            for x, val in enumerate(row):
                c = 0

                for dy, dx in dirs:
                    ny = y + dy
                    nx = x + dx

                    if ny < 0 or ny >= len(game):
                        otherk = k + 1
                        if ny < 0:
                            othery, otherx = 1, 2
                        else:
                            othery, otherx = 3, 2
                        if levels[otherk][othery][otherx] == '#':
                            c += 1

                    elif nx < 0 or nx >= len(game[ny]):
                        otherk = k + 1
                        if nx < 0:
                            othery, otherx = 2, 1
                        else:
                            othery, otherx = 2, 3
                        if levels[otherk][othery][otherx] == '#':
                            c += 1

                    elif game[ny][nx] == '?':
                        otherk = k - 1
                        if dy == 1:
                            ys, xs = [0] * 5, range(5)
                        elif dy == -1:
                            ys, xs = [4] * 5, range(5)
                        elif dx == 1:
                            ys, xs = range(5), [0] * 5
                        elif dx == -1:
                            ys, xs = range(5), [4] * 5
                        for othery, otherx in zip(ys, xs):
                            if levels[otherk][othery][otherx] == '#':
                                c += 1

                    elif game[ny][nx] == '#':
                        c += 1

                if game[y][x] == '#':
                    if c != 1:
                        new[k][y][x] = '.'
                elif game[y][x] == '.':
                    if c in (1, 2):
                        new[k][y][x] = '#'
                else:
                    pass

    return new


for i in range(200):
    levels = step(levels)


#for k in sorted(levels.keys()):
for k in [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]:
    game = levels[k]
    print('Level', k)
    for row in game:
        print(''.join(row))
    print('\n')


c = 0

for k, game in levels.items():
    for row in game:
        for val in row:
            if val == '#':
                c += 1

print(c)

