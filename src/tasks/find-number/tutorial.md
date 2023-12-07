Сделаем bfs по состояниям дп.


1. $(mod, s)$ &mdash; хранит минимальное в виде строки, которое имеет остаток $mod$ от деление на $d$ и сумму цифр $s$.
2. $(0, 0) = ""$
3. Из текущего состояния $(mod, sum)$ мы переходим во все состояние $(mod', sum')$ если дописываем последнее число $x=0\dots9$. 
Понятно, что $sum' = sum + x$ и $mod' = (mod \times 10 + x) \% d$.
4. ответ хранится в состояние $(0, s)$.

Это не самое обычное $dp$.

Запустим обычный bfs из состояния $(0, 0)$. Максимально состояний у нас $d \times s$, так как состояния, для которых $sum > s$ мы не рассматриваем. Получается ДП только считаем мы тут не последовательно, а вширь используя BFS.

Дополнительно прямо в очереди можно хранить числа вместе с состояниями.

```cpp
void solve() {
  int k, s;
  cin >> k >> s;

  queue<pair<pair<int, int>, string>> q;  // {{mod, sum}, string}
  vector<vector<bool>> used(k, vector<bool>(s + 1, false));
  used[0][0] = true;
  q.push({{0, 0}, ""});

  while (!q.empty()) {
    int mod = q.front().first.first;
    int sum = q.front().first.second;

    string num = q.front().second;
    q.pop();

    if (sum > s) continue;

    if (mod == 0 && sum == s) {
      cout << num;
      return;
    }

    for (int i = 0; i < 10; i++) {
      int mod_ = (mod * 10 + i) % k;
      int sum_ = sum + i;
      if (sum_ > s) continue;

      if (!used[mod_][sum_]) {
        used[mod_][sum_] = true;
        q.push({{mod_, sum_}, num + (char)(i + '0')});
      }
    }
  }
  cout << -1;
}
```