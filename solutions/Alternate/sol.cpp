#include <bits/stdc++.h>
#include <queue>
#include <ranges>
#include <stack>
#include <unordered_map>
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
	string s, t;
	cin >> s >> t;
	unordered_map<string, bool> isRed;
	cin >> ws;
	string node, inp;
	bool red;
	for (int c = 0; c < n; c++) {
		getline(cin, inp);
		red = false;
		size_t spaceIndex = 0;
		if ((spaceIndex = inp.find(" ")) != std::string::npos) {
			red = true;
			node = inp.substr(0, spaceIndex);
		} else {
			node = inp;
		}
		isRed[node] = red;
	}

	unordered_map<string, vector<string>> edges;
	string u, v, edge;

	for (int c = 0; c < m; c++) {
		cin >> u >> edge >> v;

		if ((isRed[u] and isRed[v]) or (not isRed[u] and not isRed[v]))
			continue;

		if (edge == "--")
			edges[v].push_back(u);

		edges[u].push_back(v);
	}

	stack<string> st;
	st.push(s);
	bool found_path = false;
	while (not st.empty() and not found_path) {
		string cur = st.top();
		st.pop();
		for (auto edge : edges[cur]) {
			if (edge == t) {
				found_path = true;
				break;
			}
			st.push(edge);
		}
	}

	cout << (found_path ? "true" : "false");
}
