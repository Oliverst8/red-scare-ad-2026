#include <bits/stdc++.h>
#include <queue>
#include <ranges>
#include <stack>
#include <unordered_map>
#include <unordered_set>
using namespace std;

#ifdef LOCAL
#define dbg(...)                                                               \
	println(stderr, "[L{}] {} = {:n}", __LINE__, #__VA_ARGS__,             \
		forward_as_tuple(__VA_ARGS__))
#else
#define dbg(...)
#endif

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

	vector<vector<int>> edges(n);
	int u, v;
	string uIn, vIn, edge;

	for (int c = 0; c < m; c++) {
		cin >> uIn >> edge >> vIn;
		u = convert[uIn];
		v = convert[vIn];

		if ((isRed[u] and isRed[v]) or (not isRed[u] and not isRed[v]))
			continue;

		if (edge == "--")
			edges[v].push_back(u);

		edges[u].push_back(v);
	}

	stack<int> st;
	st.push(s);
	bool found_path = false;
	unordered_set<int> visited;
	while (not st.empty() and not found_path) {
		int cur = st.top();
		visited.insert(cur);
		st.pop();
		for (auto edge : edges[cur]) {
			if (edge == t) {
				found_path = true;
				break;
			}
			if (visited.contains(edge))
				continue;
			st.push(edge);
		}
	}

	cout << (found_path ? "true" : "false");
}
