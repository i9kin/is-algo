Пусть все запросы были с одинаковым $x$. Тогда в массиве все элементы не равные $x$ нас не интересует. 

Рассмотрим массив из индексов на которых числа равны $x$. Тогда запрос можно трансформировать в новый "есть ли в этом массиве числа в диапазоне $[l, r]$". Это можно сделать одним бинпоиском. Найдём первое число, которое не меньше $l$ и проверим, что оно не больше $r$.

Такой массив для каждого числа можно построить используя словарь, но на самом деле можно воспользоваться бинпоиском. Сделаем массив уникальных чисел $b$(сортировка + удаление повторяющихся). Сделаем вектор векторов, где $i$-ый вектор хранит все индексы равные $b[i]$.

```cpp
void solve() {
  int n;
  cin >> n;
  vector<int> a(n);
  for (int i = 0; i < n; i++) {
    cin >> a[i];
  }
  auto b = a;
  {
    sort(b.begin(), b.end());
    b.resize(unique(b.begin(), b.end()) - b.begin());
  }
  vector<vector<int>> pos(b.size());
  for (int i = 0; i < n; i++) {
    int j = lower_bound(b.begin(), b.end(), a[i]) - b.begin();
    pos[j].push_back(i);
  }

  int q;
  cin >> q;
  while (q--) {
    int l, r, x;
    cin >> l >> r >> x;
    l--, r--;
    int j = lower_bound(b.begin(), b.end(), x) - b.begin();
    if (b[j] != x) {
      cout << 0;
      continue;
    }
    auto& ind = pos[j];
    auto it = lower_bound(ind.begin(), ind.end(), l);
    if (it == ind.end()) {
      cout << 0;
      continue;
    }
    cout << ((*it) <= r);
  }
}
```