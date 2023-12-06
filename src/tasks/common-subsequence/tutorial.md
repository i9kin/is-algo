1. Двумерное $dp[i][j]$ &mdash; количество подходящих подпоследовательностей, если рассмотреть префикс $i$ в $S$ и префикс $j$ в $T$.
2. Начальные значения состояний &mdash; $dp[0][0] = 1$ (пустое множество подходит)
3. Считаем опять двумя циклами, $dp[i][j]$:

* $\sum_{i' < i, j' < j} dp[i'][j'] + 1$ если $S_i = T_j$, 
* $0$ иначе.
4. Ответ &mdash; $\sum_{i<N,j<M} dp[i][j]$ 

Маленькая оптимизация. $dp[0][0] = 1$, чтобы было решение за $O(n \times m)$ надо сделать оптимизацию префиксных сумм, так как мы для подсчёта $\sum_{i' < i, j' < j} dp[i'][j']$ делаем запрос суммы на прямоугольники $(0, 0) - (i - 1, j - 1)$.

```cpp
cin >> n >> m;
vector<int> s(n), t(m);
for (int i = 0; i < n; i++) cin >> s[i];
for (int i = 0; i < m; i++) cin >> t[i];

vector<vector<int>> dp(n + 1, vector<int>(m + 1));
vector<vector<int>> sum(n + 1, vector<int>(m + 1));

dp[0][0] = 1;
sum[0][0] = 1;

for (int i = 0; i <= n; i++) sum[i][0] = 1;
for (int j = 0; j <= m; j++) sum[0][j] = 1;

for (int i = 1; i <= n; i++) {
  for (int j = 1; j <= m; j++) {
    if (s[i - 1] == t[j - 1]) {
      dp[i][j] = sum[i - 1][j - 1];
    }
    sum[i][j] = add(dp[i][j],
                    sub(add(sum[i - 1][j], sum[i][j - 1]), sum[i - 1][j - 1]));
  }
}
cout << sum[n][m];
```