n, m, r = map(int, input().split())
s, t = map(int, input().split())

R = set()
Edges = []

for i in range(n):
    vertex = input()
    if "*" in vertex:
        v, _ = vertex.split(" ")
        R.add(int(v))


for i in range(m):
    u, typ, v = input().split(" ")
    u = int(u)
    v = int(v)
    if typ == "->":
        if u in R:
            Edges.append((u, v, -1))
        else:
            Edges.append((u, v, 0))
    else:
        print("only works for DAG")


def bellman_ford():
    dist = [1] * n
    dist[s] = 0

    for i in range(n):
        for u, v, w in Edges:
            if dist[u] + w < dist[v]:
                if i == n-1:
                    return 1
                dist[v] = dist[u] + w
    return dist[t]

res = bellman_ford()
if res == 1:
    print("contains negative cycle")
else:
    print(res*-1)


