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
const int null = -1;

// BellmanFord implemented from
// https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
int many(unordered_map<string, vector<pair<string, int>>> &edges, int n,
         const string s, const string t) {
  unordered_map<string, int> dist;
  unordered_map<string, string> predecessor;

  for (const auto &vertex : edges) {
    dist[vertex.first] = INF;
    predecessor[vertex.first] = null;
  }

  dist[s] = 0;

  for (int i = 0; i < n - 1; i++) {
    for (const auto &vertex : edges) {
      const string u = vertex.first;
      for (const auto &to : vertex.second) {
        const string v = to.first;
        const int w = to.second;
        if (dist[u] + w < dist[v]) {
          dist[v] = dist[u] + w;
          dbg(u, v, w, dist[v]);
          predecessor[v] = u;
        }
      }
    }
  }

  for (const auto &vertex : edges) {
    string u = vertex.first;
    for (const auto &to : vertex.second) {
      string v = to.first;
      int w = to.second;
      if (dist[u] + w < dist[v]) {
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
  string s, t;
  cin >> s >> t;
  unordered_map<string, bool> isRed;
  cin >> ws;
  string node, inp;
  bool red;
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
    isRed[node] = red;
  }
  dbg(isRed);

  unordered_map<string, vector<pair<string, int>>> edges;
  string u, v, edge;

  for (int c = 0; c < m; c++) {
    cin >> u >> edge >> v;

    if (edge == "--")
      edges[v].push_back({u, isRed[v] ? -1 : 0});

    edges[u].push_back({v, isRed[u] ? -1 : 0});
  }

  auto res = many(edges, n, s, t);
  dbg(res);
  if (res == -2) {
    cout << '?';
  } else {
    res += isRed[t] ? 1 : 0;
    cout << res;
  }
}
