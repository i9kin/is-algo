$h < i < j; y_h \ge y_i; y_i \le y_j$

$(h, i)$ и $(i, j)$ интересные пары

$dp_i = min(max(dp_j, dist(i, j)))$

$o(n)$ из за количества интересных пар

```cpp

struct pt {
  int x, y;

  pt() {}

  pt(int x, int y) : x(x), y(y) {}
};

int n;
vector<pt> a;

void solve() {
  cin >> n;
  vector<ll> dp(n, LLONG_MAX);
  a.assign(n, {});
  for (auto& [x, y] : a) cin >> x >> y;
  dp[0] = 0;
  stack<int> s;
  s.push(0);
  for (int i = 1; i < n; i++) {
    while (!s.empty()) {
      auto W = max(
          dp[s.top()],
          1LL * abs(a[i].x - a[s.top()].x) * abs(a[i].x - a[s.top()].x) +
              1LL * abs(a[i].y - a[s.top()].y) * abs(a[i].y - a[s.top()].y));
      dp[i] = min(dp[i], W);
      if (a[s.top()].y > a[i].y) break;
      s.pop();
    }
    s.push(i);
  }
  cout << sqrtl(dp[n - 1]);
}
```
