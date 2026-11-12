n, m, r = map(int, input().split())
s, t = input().split()

R = set()
Edges = []
Dist = {}


for i in range(n):
    vertex = input()
    if "*" in vertex:
        v, _ = vertex.split(" ")
        R.add(v)
        Dist[v] = 1
    else:
        Dist[vertex] = 1

for i in range(m):
    u, typ, v = input().split(" ")
    if typ == "->":
        directed = True
        if u in R:
            Edges.append((u, v, -1))
        else:
            Edges.append((u, v, 0))
    else:
        Edges.append((u, v, 0))
        Edges.append((v, u, 0))


def bellman_ford(Dist, Edges):
    Dist[s] = 0

    for i in range(n):
        for u, v, w in Edges:
            if Dist[u] + w < Dist[v]:
                if i == n-1:
                    return 1
                Dist[v] = Dist[u] + w
    return Dist[t]

res = bellman_ford(Dist, Edges)
if res == 1:
    print("contains negative cycle")
else:
    print(res*-1)


