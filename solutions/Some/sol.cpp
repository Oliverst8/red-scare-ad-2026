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
int many(unordered_map<string, unordered_map<string, int>> &edges, int n,
         const string s, const string t, vector<string> verticies) {
  unordered_map<string, int> dist;

  for (const auto &vertex : verticies) {
    dist[vertex] = INF;
  }

  dist[s] = 0;

  for (int i = 0; i < n - 1; i++) {
    for (const auto &vertex : edges) {
      const string u = vertex.first;
      for (const auto &to : vertex.second) {
        const string v = to.first;
        const int w = to.second;
        if (dist[u] + w < dist[v] and dist[u] != INF) {
          dist[v] = dist[u] + w;
          dbg(u, v, w, dist[v]);
        }
      }
    }
  }

  for (const auto &vertex : edges) {
    string u = vertex.first;
    for (const auto &to : vertex.second) {
      string v = to.first;
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
ll edmonsKarp(unordered_map<string, unordered_map<string, int>> &edges, int N,
              string s, string t) {
  ll sum = 0;
  dbg(edges);

  while (true) {
    queue<tuple<string, string, int>> st;
    st.push({s, s, INF});
    unordered_set<string> visited;
    unordered_map<string, string> parent;
    int mn = INF;
    string sinkPar = "";
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
    if (mn == INF or sinkPar == "") {
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
  string s, t;
  cin >> s >> t;
  unordered_map<string, bool> isRed;
  cin >> ws;
  string node, inp;
  bool red;
  vector<string> verticies;
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
    verticies.push_back(node);
    isRed[node] = red;
  }
  dbg(isRed);

  unordered_map<string, unordered_map<string, int>> edges;
  string u, v, edge;
  bool directed = true;

  for (int c = 0; c < m; c++) {
    cin >> u >> edge >> v;

    if (edge == "--") {
      directed = false;
      edges[v][u] = isRed[v] ? -1 : 0;
    }

    edges[u][v] = isRed[u] ? -1 : 0;
  }

  if (directed) {
    auto res = many(edges, n, s, t, verticies);
    dbg(res);
    if (res == -2) {
      cout << '?';
    } else {
      res += isRed[t] ? 1 : 0;
      cout << (res > 0 ? "true" : "false");
    }
  } else {
    for (auto &[u, neighbors] : edges)
      for (auto &[v, w] : neighbors)
        w = 1;
    unordered_map<string, unordered_map<string, int>> graph;
    for (auto &[u, neighbors] : edges) {
      const string uOut = u + "Ø";
      graph[u][uOut] = 1;
      graph[uOut] = neighbors;
    }

    const string sMark = "Ø";
    const string tMark = "Å";
    graph[sMark][s] = 1;
    graph[s][sMark] = 1;
    graph[sMark][t] = 1;
    graph[t][sMark] = 1;

    for (auto &[v, red] : isRed) {
      if (not red)
        continue;

      auto g = graph;

      g[tMark][v] = 2;
      g[v][tMark] = 2;

      auto res = edmonsKarp(g, n, sMark, tMark);
      cout << (res == 2 ? "true" : "false");
      if (res == 2)
        return 0;
    }
    cout << "false";
  }
}
