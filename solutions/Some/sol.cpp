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
using ll = long long;

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
int many(vector<unordered_map<int, int>> &edges, int n, const int s,
         const int t) {

  vector<int> dist(n);

  for (int i = 0; i < n; i++) {
    dist[i] = INF;
  }

  dist[s] = 0;

  for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < edges.size(); j++) {
      const int u = j;
      for (const auto &to : edges[j]) {
        const int v = to.first;
        const int w = to.second;
        if (dist[u] + w < dist[v] and dist[u] != INF) {
          dist[v] = dist[u] + w;
          dbg(u, v, w, dist[v]);
        }
      }
    }
  }

  for (int j = 0; j < edges.size(); j++) {
    const int u = j;
    for (const auto &to : edges[j]) {
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

// Taken from openpitmining solution
ll edmonsKarp(vector<unordered_map<int, int>> &edges, int N, int s, int t) {
  ll sum = 0;
  dbg(edges);

  while (true) {
    queue<tuple<int, int, int>> st;
    st.push({s, s, INF});
    unordered_set<int> visited;
    unordered_map<int, int> parent;
    int mn = INF;
    int sinkPar = INT_MIN;
    while (st.size() > 0) {
      auto cur = st.front();
      st.pop();
      if (visited.contains(get<0>(cur)))
        continue;
      visited.insert(get<0>(cur));
      mn = min(mn, get<2>(cur));

      if (get<0>(cur) == t) {
        sinkPar = get<1>(cur);
        // dbg(cur);
        break;
      }

      dbg(edges);
      dbg(visited, st);

      parent[get<0>(cur)] = get<1>(cur);

      for (auto edge : edges[get<0>(cur)]) {
        if (edge.second <= 0 or visited.contains(edge.first))
          continue;
        dbg(cur, edge, st);
        st.push({edge.first, get<0>(cur), edge.second});
      }
    }
    // dbg(sinkPar);
    if (mn == INF or sinkPar == INT_MIN) {
      break;
    }

    edges[sinkPar][t] -= mn;
    edges[t][sinkPar] += mn;
    while (sinkPar != s) {
      dbg(mn);
      auto myPar = parent[sinkPar];
      dbg(myPar);
      edges[myPar][sinkPar] -= mn;
      edges[sinkPar][myPar] += mn;
      sinkPar = myPar;
    }
    sum += mn;
    dbg(edges);
    // return sum;
  }
  return sum;
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

  vector<unordered_map<int, int>> edges(n);
  int u, v;
  string uIn, vIn, edge;

  bool directed = true;

  for (int c = 0; c < m; c++) {
    cin >> uIn >> edge >> vIn;
    u = convert[uIn];
    v = convert[vIn];

    if (edge == "--") {
      directed = false;
      edges[v][u] = isRed[v] ? -1 : 0;
    }

    edges[u][v] = isRed[u] ? -1 : 0;
  }

  if (directed) {
    auto res = many(edges, n, s, t);
    dbg(res);
    if (res == -2) {
      cout << '?';
    } else {
      res += isRed[t] ? 1 : 0;
      cout << (res > 0 ? "true" : "false");
    }
  } else {

    for (int u = 0; u < n; u++)
      for (auto &[v, w] : edges[u])
        w = 1;
    vector<unordered_map<int, int>> graph(2 * n + 2);
    for (int u = 0; u < n; u++) {
      const int uOut = u + n;
      graph[u][uOut] = 1;
      graph[uOut] = edges[u];
    }

    const int sMark = 2 * n;
    const int tMark = 2 * n + 1;
    graph[sMark][s] = 1;
    graph[s][sMark] = 1;
    graph[sMark][t] = 1;
    graph[t][sMark] = 1;

    for (int v = 0; v < n; v++) {
      if (not isRed[v])
        continue;

      auto g = graph;

      g[tMark][v] = 2;
      g[v][tMark] = 2;

      auto res = edmonsKarp(g, n, sMark, tMark);
      if (res == 2) {
        cout << "true";
        return 0;
      }
    }
    cout << "false";
  }
}
