links = 0

graph = {}

planets = set()

with open('../011/input', 'rt') as f:
    for line in f:
        line = line.strip()
        a, b = line.split(')')   # b orbits a
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[b].add(a)
        graph[a].add(b)
        planets.add(b)
        planets.add(a)

from collections import deque

q = deque()
visited = set()

q.append(('YOU', -2))
visited.add('YOU')

while len(q) > 0:
    curr, d = q.popleft()
    if curr == 'SAN':
        print(d)
        break
    for n in graph[curr]:
        if n not in visited:
            q.append((n, d+1))
            visited.add(n)

