links = 0

graph = {}

planets = set()

with open('input', 'rt') as f:
    for line in f:
        line = line.strip()
        a, b = line.split(')')   # b orbits a
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[b].add(a)
        planets.add(b)
        planets.add(a)

solved = {}

for p in planets:
    if len(graph[p]) == 0:
        solved[p] = 0

print(solved)

while len(solved) < len(planets):
    for p in planets:
        for t in graph[p]:
            if t not in solved:
                break
        else:  # <-- no break
            # SOLVED A NEW ONE!
            s = 0
            for t in graph[p]:
                s += solved[t]
            solved[p] = s + len(graph[p])
            #print(p, s, len(graph[p]))

print(sum(solved.values()))

