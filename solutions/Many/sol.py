from collections import deque

n, m, _ = map(int, input().split())
s, t = input().split()

R = set()
Edges = []
Dist = {}

Adjacency = {}

directed = False

for i in range(n):
    vertex = input()
    if "*" in vertex:
        v, _ = vertex.split(" ")
        R.add(v)
        Dist[v] = 1
        Adjacency[v] = []
    else:
        Dist[vertex] = 1
        Adjacency[vertex] = []

for i in range(m):
    u, typ, v = input().split(" ")
    if typ == "->":
        directed = True
        if v in R:
            Edges.append((u, v, -1))
        else:
            Edges.append((u, v, 0))
    else:
        Adjacency[u].append(v)
        Adjacency[v].append(u)


def bellman_ford(Dist, Edges):
    Dist[s] = -1 if s in R else 0

    for i in range(n):
        for u, v, w in Edges:
            if Dist[u] != 1 and Dist[u] + w < Dist[v]:
                if i == n-1:
                    print("contains negative cycle")
                    exit(0)
                Dist[v] = Dist[u] + w
    return Dist[t]

def BFS(Adjacency):
    Visited = set()
    Number_of_red_on_path = {s: -1 if s in R else 0}
    q = deque()
    Visited.add(s)
    q.append(s)
    while q:
        curr = q.popleft()
        for e in Adjacency[curr]:
            if e not in Visited:
                Adjacency[e].remove(curr)
                Visited.add(e)
                q.append(e)
                if e in R:
                    Number_of_red_on_path[e] = Number_of_red_on_path[curr] - 1
                else:
                    Number_of_red_on_path[e] = Number_of_red_on_path[curr]
            else:
                print("not tree")
                exit(0)
    if t not in Number_of_red_on_path:
        print("-1")
        exit(0)
    return Number_of_red_on_path[t]

if directed:
    res = bellman_ford(Dist, Edges)
else:
    res = BFS(Adjacency)

print(res*-1)


