game = """
##.#.
.#.##
.#...
#..#.
.##.."""


game = [list(line) for line in game.strip().split('\n')]


def state(game):
    i = 0
    total = 0
    for y, row in enumerate(game):
        for x, val in enumerate(row):
            if val == '#':
                score = (1 << i)
                total += score
            i += 1
    return total


seen = set()

seen.add(state(game))


dirs = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]


def step(game):
    new = [list(row) for row in game]
    for y, row in enumerate(game):
        for x, val in enumerate(row):
            c = 0
            for dy, dx in dirs:
                ny = y + dy
                nx = x + dx
                if ny < 0 or ny >= len(game):
                    continue
                if nx < 0 or nx >= len(game[ny]):
                    continue
                if game[ny][nx] == '#':
                    c += 1
            if game[y][x] == '#':
                if c != 1:
                    new[y][x] = '.'
            else:
                if c in (1, 2):
                    new[y][x] = '#'
    return new


while True:
    game = step(game)
    s = state(game)
    if s in seen:
        print(s)
        break
    seen.add(s)

