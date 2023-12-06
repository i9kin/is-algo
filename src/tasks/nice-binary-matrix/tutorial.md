Не комбинаторное дп.

Случаи $min(n, m) > 3$ отсекаются так как, если если матрица 4x4 это 4 матрицы 2x2. Чётное != 4 * нечётное [Я чекал тесты и в разборе не написанно, про тесты вида 10000 3 их просто нет, но там просто надо матрицу перевернуть]

Попробуем написать решение для `узкой` матрицы. 

Давайте строить матрицу ответа по столбцам.

Дп по префиксу, но с маской (поэтому крутая идея). 

1. Двуменное $dp[i][mask]$ &mdash; минимальное количество ячеек, которое нужно изменить, чтобы сделать матрицу на префиксе $i$ хорошей, где состояние $i$-того слолбца кодируется $mask$ :) 
2. Начальные значение посчитаем для всех $dp[0][mask]$ равное количеству ячеек в первом столбце, которые не равны нашей маске.
3. Пересчёт. Кода мы строим $i$-ый столбец с маской $cur_{mask}$ достаточно перебрать состояния предыдущего столбца $prev_{mask}$ и проверить, что матрица вида $prev_{mask}$ и $cur_{mask}$ (соседние $(i - 1)$ и $i$ состояния столбцов).
Стоимость построить на $i$-том столбце значения $mask$ это просто количество $1$ в выражение 

$$def_{mask} \oplus cur_{mask}$$, где $def_{mask}$ &mdash; изначальная маска столбца 

4. Ответ &mdash; минимальное значение $dp[m - 1][mask]$, по любым маскам.

$$O(m \times 2^{2^n}+n \times m)$$

```cpp
void solve() {
  int n, m;
  cin >> n >> m;

  if (min(n, m) > 3) {
    cout << -1;
    return;
  }
  if (min(n, m) == 1) {
    cout << 0;
    return;
  }

  vector<int> COL(m);
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      char x;
      cin >> x;
      if (x == '1') {
        COL[j] += (1 << i);
      }
    }
  }
  auto diff = [&](int a, int b) { return __builtin_popcount(a ^ b); };

  auto submatrix_check = [&](int maskL, int maskR) {
    int cnt0 = 0;

    // 2x2
    for (int i = 0; i < 2; i++) cnt0 += ((maskL >> i) & 1) + ((maskR >> i) & 1);
    if (cnt0 % 2 == 0) return false;

    // 3x3
    if (n == 3) {
      cnt0 = 0;
      for (int i = 1; i < 3; i++)
        cnt0 += ((maskL >> i) & 1) + ((maskR >> i) & 1);
      if (cnt0 % 2 == 0) return false;
    }
    return true;
  };

  vector<vector<int>> dp(m, vector<int>(1 << n, 1e9));

  for (int mask = 0; mask < (1 << n); mask++) {
    dp[0][mask] = diff(mask, COL[0]);
  }

  for (int i = 1; i < m; i++) {
    for (int cur_mask = 0; cur_mask < (1 << n); cur_mask++) {
      for (int prev_mask = 0; prev_mask < (1 << n); prev_mask++) {
        if (submatrix_check(cur_mask, prev_mask)) {
          dp[i][cur_mask] = min(dp[i][cur_mask],
                                dp[i - 1][prev_mask] + diff(cur_mask, COL[i]));
        }
      }
    }
  }
  int ans = 1e9;
  for (int mask = 0; mask < (1 << n); mask++) {
    ans = min(ans, dp[m - 1][mask]);
  }
  cout << ans;
}
```