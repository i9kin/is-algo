> Решение авторское жадное.

Опять не комбинаторное ДП.

Обозначим строку, которую мы ищем, за $s'$.

1. Двуменное $dp[i][k]$ &mdash; минимальное количество замен, чтобы $s'$ на префиксе $i$ был валидный и $s'_i = k$ 
2. Начальное значение $dp[0][s_0] = 0$, так как мы не заменяли, и $1$ для всех остальных случаев.
3.  Пусть мы выбрали, что $s'_i = k$, значит по условию $s'_{i-1} \ne k$. Значит из всех состояний $dp[i-1][\ne k]$ минимальный.
4. Ответ минимальное значение из $dp[n-1][.]$.

Это медленно $O(n \times k^2)$.

Соптимизируем до $O(n \times k)$ поддерживая префиксные минимумы для состояния $dp[i-1]$. И тогда выбор оптимального состояния, через которое мы обновим $dp[i][k]$ будет за $o(1)$

```cpp

void solve() {
  int n, k;
  cin >> n >> k;
  vector<vector<int>> ans(k, vector<int>(n));
  vector<vector<int>> p(k, vector<int>(n));

  vector<int> pref(k);
  vector<int> suf(k);

  for (int _ = 0; _ < n; _++) {
    char c;
    cin >> c;

    if (_ == 0) {
      ans[c - 'A'][0] = 0;
      p[c - 'A'][0] = -1;

      for (int i = 0; i < k; i++) {
        if (i != c - 'A') {
          ans[i][0] = 1;
          p[i][0] = -1;
        }
      }
    } else {
      for (int x = 0; x < k; x++) {
        if (x == 0) {
          ans[x][_] = ans[suf[x + 1]][_ - 1];
          p[x][_] = suf[x + 1];
        } else if (x == k - 1) {
          ans[x][_] = ans[pref[x - 1]][_ - 1];
          p[x][_] = pref[x - 1];
        } else {
          int a = pref[x - 1];
          int b = suf[x + 1];

          if (ans[a][_ - 1] > ans[b][_ - 1]) swap(a, b);

          ans[x][_] = ans[a][_ - 1];
          p[x][_] = a;
        }

        if (x != c - 'A') {
          ans[x][_]++;
        }
      }
    }

    pref[0] = 0;
    for (int i = 1; i < k; i++) {
      if (ans[i][_] < ans[pref[i - 1]][_]) {
        pref[i] = i;
      } else {
        pref[i] = pref[i - 1];
      }
    }

    suf[k - 1] = k - 1;
    for (int i = k - 2; i >= 0; i--) {
      if (ans[i][_] < ans[suf[i + 1]][_]) {
        suf[i] = i;
      } else {
        suf[i] = suf[i + 1];
      }
    }
  }

  pair<int, int> b = {INT_MAX, -1};
  for (int i = 0; i < k; i++) {
    b = min(b, {ans[i][n - 1], i});
  }
  cout << b.first << '\n';

  string res;
  char c = b.second;
  for (int i = n - 1; i >= 0; i--) {
    res += (char)(c + 'A');
    c = p[c][i];
  }

  reverse(res.begin(), res.end());
  cout << res;
}

```