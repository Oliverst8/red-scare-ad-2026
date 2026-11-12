from collections import deque

n, m, r = map(int, input().split())
s, t = input().split()

V = {}
G = {}

for i in range(n):
    vertex = input()
    if "*" in vertex:
        v, _ = vertex.split(" ")
        V[v] = True
        G[v] = []
    else:
        V[vertex] = False
        G[vertex] = []

for i in range(m):
    u, typ, v = input().split(" ")
    if (V[u] and u not in (s,t)) or (V[v] and v not in (s,t)):
        continue
    G[u].append(v)
    if typ[1] != '>':
        G[v].append(u)


def bfs(start, end):
    q = deque()
    path = {}
    q.append(start)
    path[start] = 0
    visited = set()
    visited.add(start)

    while q:
        u = q.popleft()
        
        for v in G[u]:
            if v not in visited:
                visited.add(v)
                path[v] = path[u] + 1
                q.append(v)
            if v == end:
                return path[end]
    return None

print(bfs(s, t))
