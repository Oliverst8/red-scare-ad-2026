#include <bits/stdc++.h>
#include <climits>
#include <cstdlib>
#include <queue>
#include <ranges>
#include <stack>
#include <string>
#include <unordered_map>
#include <unordered_set>
using namespace std;

#ifdef LOCAL
#define dbg(...)                                                               \
  println(stderr, "[L{}] {} = {:n}", __LINE__, #__VA_ARGS__,                   \
          forward_as_tuple(__VA_ARGS__))
#else
#define dbg(...)
#endif

const int INF = INT_MAX;

// BellmanFord implemented from
// https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
int many(vector<vector<pair<int, int>>> &edges, int n, const int s,
         const int t) {
  vector<int> dist(n);

  for (int i = 0; i < n; i++) {
    dist[i] = INF;
  }

  dist[s] = 0;

  for (int i = 0; i < n - 1; i++) {
    for (int u = 0; u < edges.size(); u++) {
      for (const auto &to : edges[u]) {
        const int v = to.first;
        const int w = to.second;
        if (dist[u] + w < dist[v] and dist[u] != INF) {
          dist[v] = dist[u] + w;
          dbg(u, v, w, dist[v]);
        }
      }
    }
  }

  for (int u = 0; u < edges.size(); u++) {
    for (const auto &to : edges[u]) {
      int v = to.first;
      int w = to.second;
      if (dist[u] != INF and dist[u] + w < dist[v]) {
        dbg("HERE");
        return -2;
      }
    }
  }

  return dist[t] == INF ? -1 : abs(dist[t]);
}

int main() {
  cin.tie(0)->sync_with_stdio(0);
  int n, m, r;
  cin >> n >> m >> r;
  string sIn, tIn;
  cin >> sIn >> tIn;
  vector<bool> isRed(n);
  cin >> ws;
  string node, inp;
  bool red;
  unordered_map<string, int> convert;
  for (int c = 0; c < n; c++) {
    getline(cin, inp);
    red = false;
    size_t starIndex = 0;
    if ((starIndex = inp.find("*")) != std::string::npos) {
      red = true;
      node = inp.substr(0, starIndex - 1);
    } else {
      node = inp;
    }
    convert[node] = c;
    isRed[c] = red;
  }
  int s = convert[sIn];
  int t = convert[tIn];
  dbg(isRed);

  vector<vector<pair<int, int>>> edges(n);
  int u, v;
  string uIn, vIn, edge;

  for (int c = 0; c < m; c++) {
    cin >> uIn >> edge >> vIn;
    u = convert[uIn];
    v = convert[vIn];

    if (edge == "--")
      edges[v].push_back({u, isRed[v] ? -1 : 0});

    edges[u].push_back({v, isRed[u] ? -1 : 0});
  }

  auto res = many(edges, n, s, t);
  dbg(res);
  if (res == -2) {
    cout << '?';
  } else {
    res += isRed[t] and res >= 0 ? 1 : 0;
    cout << res;
  }
}
