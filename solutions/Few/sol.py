
import heapq

n, m, r = map(int, input().split())

s, t = input().split()

R = set()

G = {}

for i in range(n):
    line = input().split()
    if len(line) > 1:
        R.add(line[0])
    G[line[0]] = set()

for i in range(m):
    line = input().split()
    if line[1] == "--":
        first = line[0]
        second = line[2]

        w0 = 1 if first in R else 0
        w2 = 1 if second in R else 0

        G[first].add((w2, second))
        G[second].add((w0, first))
    else:
        G[line[0]].add((1 if line[2] in R else 0, line[2]))

print(G)

queue = []
heapq.heapify(queue)

count = 1 if s in R else 0

for e in G[s]:
    print(e)
    heapq.heappush(queue, (e[0] + count, e[1]))

visited = set()


while(len(queue) > 0):
    w, node = heapq.heappop(queue)
    count = w
    if node == t:
        break
    visited.add(node)

    for e in G[node]:
        w_new, node_new = e
        if node_new in visited:
            continue
        else:
            heapq.heappush(queue, (w_new + count, node_new))

print(count)