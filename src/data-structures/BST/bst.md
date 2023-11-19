# Двоичное дерево поиска

Бинарное дерево поиска (англ. binary search tree, `BST`) &mdash; структура данных для работы с упорядоченными множествами.

> `BST` &mdash; это всего-лишь большой класс структур данных, которые основаны на одной идеи, поддерживать некоторое бинарное дерево. 

```tree 
8 3 1 6 4 7 10 14 13
```

Название состоит из двух важных частей &mdash; `бинарное дерево` и `поиск`. Первое указывает на вид структуры данных, а второе на возможность удобного поиска в ней.

```admonish success title="Напоминание"
[Дерево](https://ru.wikipedia.org/wiki/%D0%94%D0%B5%D1%80%D0%B5%D0%B2%D0%BE_(%D1%82%D0%B5%D0%BE%D1%80%D0%B8%D1%8F_%D0%B3%D1%80%D0%B0%D1%84%D0%BE%D0%B2)) &mdash; это связный ациклический граф. 

Бинарное дерево &mdash; дерево в котором, у каждой вершины не более двух детей.
```

Представим, что числа из множества являются вершинами (как на картинке). Например, даже для множества $\{1, 3, 5, 8\}$ можно построить очень много бинарных деревьев. Пусть для некоторой перестановки мы поочерёдно вставляем её элементы в дерево, например $p = [a_0, a_2, a_3, a_1]$. Таких перестановок $4!$ и почти все из них будут давать разные деревья.

<div class="center">
<div class="angry-grid">
<div id="item-0">```tree
1 3 5 8 
[0,1,2,3]
```</div>
<div id="item-1">```tree
1 3 8 5 
[0,1,3,2]
```</div>
<div id="item-2">```tree
1 5 3 8 
[0,2,1,3],[0,2,3,1]
```</div>
<div id="item-3">```tree
1 8 3 5 
[0,3,1,2]
```</div>
<div id="item-4">```tree
1 8 5 3 
[0,3,2,1]
```</div>
<div id="item-5">```tree
3 1 5 8 
[1,0,2,3],[1,2,0,3],[1,2,3,0]
```</div>
<div id="item-6">```tree
3 1 8 5 
[1,0,3,2],[1,3,0,2],[1,3,2,0]
```</div>
<div id="item-7">```tree
5 1 3 8 
[2,0,1,3],[2,0,3,1],[2,3,0,1]
```</div>
<div id="item-8">```tree
5 3 1 8 
[2,1,0,3],[2,1,3,0],[2,3,1,0]
```</div>
<div id="item-9">```tree
8 1 3 5 
[3,0,1,2]
```</div>
<div id="item-10">```tree
8 1 5 3 
[3,0,2,1]
```</div>
<div id="item-11">```tree
8 3 1 5 
[3,1,0,2],[3,1,2,0]
```</div>
<div id="item-12">```tree
8 5 1 3 
[3,2,0,1]
```</div>
<div id="item-13">```tree
8 5 3 1 
[3,2,1,0]
```</div>
</div>
</div>

Все `bst` удовлетворяют такому свойству : для каждого узла бинарного дерева с ключом $k$, все узлы в левом поддереве должны иметь ключи, меньшие $k$, а в правом поддереве большие $k$. Из определение следует, что дерево задаёт множество, так как не хранит одинаковые числа по несколько раз.

## Представление в памяти

Существует два способа :

1. Чаще всего дерево представляют в памяти как динамически создаваемая структура с явными указателями на своих детей. Вершина при создании не имеет детей, поэтому в конструкторе `node` поля `l` и `r` мы инициализируем пустыми ссылками.

```cpp
struct node {
  node *l, *r;
  int x;
  node(int x) : x(x), l(nullptr), r(nullptr){};
};
```

2. Все узлы дерева хранятся в массиве. Поля детей имеют тип `int` и явно указывают позицию в массиве, где хранится узел ребёнка. Стоит дополнительно написать конструктор по умолчанию, чтобы компилятор понял, какими объектами заполнить массив.

Может показаться, что этот способ не удобный, но скоро вы всё поймёте =)

```cpp
struct node {
  int l, r, x;
  node(int x) : x(x), l(-1), r(-1){};
  node() : x(0), l(-1), r(-1){};
  // или node() = default;
};

node mem[100000];
// code
assert(mem[239].l != -1);
cout << mem[mem[239].l].x;
```

Чтобы создать новый узел, стоит вернуть переменную, которая указывает на только-что созданный элемент. Просто замените `new node(x)` на `new_node(x)`.

```cpp
int pos = 0;

int new_node(const T& x) {
  mem[pos] = T(x);
  return pos++;
}
```

Теперь все проверки вида `!= nullptr` нужно заменить на `!= -1`. * Вообще можно хранить $0$ и все проверки писать, как `if (v) { ... }`.

~~~admonish title="Первый способ с глобальным массивом"

Чтобы создать новый узел, стоит вернуть память под `pos`, и подвинуть `pos`.

```cpp
struct node {
  node *l, *r;
  int x;
  node(int x) : x(x), l(nullptr), r(nullptr){};
  node() = default;
};

node mem[100000];
int pos = 0;

node* new_node(const T& x) {
  mem[pos] = T(x);
  return &mem[pos++];
}
```
~~~

```admonish warning title="Оптимизация с глобальным массивом"

Реализация вторым способом или первым с массивом является оптимальной. Так как память выделяется сразу большим куском, а не при каждом вызов `new`. Хотя это выглядит логичной оптимизацией, которая ускорит программу значительно, но это не совсем так. Можно прочитать обсуждения [тут](https://www.quora.com/How-much-faster-is-static-memory-allocation-compared-to-dynamic-memory-allocation-in-C).

Грубо говоря пример 1 с массивом даст прирост производительности по времени в $3-5\%$. Но тут вступает в дело размер указателей на детей. На самом деле указатель на современных машинах занимает $8$ байт, а `int` всего $4$. На самом можно $32$ битный компилятором.
```

## Реализация функций

Базовые функции над деревом:

Которые изменяют дерево

1. `insert(x)` &mdash; вставить в дерево значение `x`.
2. `delete(x)` &mdash; удалить из дерева значение `x`.

Которые не изменяют дерево

1. `find(x)` &mdash; найти вершину в дереве к ключом `x`.
2. `find_min/find_max()` &mdash; найти вершину с минимальным/максимальным ключом.

Все функции ниже легко реализовать используя рекурсивный алгоритм. Реализуем рекурсивную функцию спуска по дереву, которая возвращает `node*`.

Для функций, которые **не** изменяют дерево, будем возвращать `node`-у нужную нам.

Для функций, которые изменяют дерево, будем возвращать `node`-у текущего поддерева в валидном состояние (все элементы в этом поддереве находятся в корректном состояние и элемент, который надо было вставить, уже вставлен или удалён, если надо было удалить). Значит при запуске таких функций надо писать `root = insert/delete(root, ...)`. 

`v` &mdash; текущая вершина, корень текущего поддерева.

## Поиск

Преимущество бинарных деревьев поиска в том, что в них можно легко производить поиск элементов. Если поиск удобный, то и другие операции просты и выражаются через поиск или имеют похожую логику.

Рекурсивная функция, которая спускается по дереву в нужную сторону, используя свойство бинарного дерева. 

Если текущая вершина пустая (`v == nullptr`) (значит мы спустились в неё по пустому указателю), то мы ничего не нашли. В таком случае логичнее вернуть `nullptr`. Если ключ текущей вершины совпадает с ключом поиска (или любое другое условие, по которому можно искать в нашем дереве) то вернём текущую вершину. Иначе, нам стоит перейти в ребёнка, ключ которого меньше ключа поиска.

```cpp
node* find(node* v, int x) {
  if (v == nullptr) return nullptr;
  if (v->x == x) return v;
  if (v->x < x) {
    return find(v->l, x);
  } else {
    return find(v->r, x);
  }
}
```

## Минимум/Максимум

Из-за структуры BST, минимум находится в самом левом элементе дерева. Максимум &mdash; в самом правом.

```cpp
node* get_min(node* v) {
  if (v != nullptr && v->l != nullptr) {
    return get_min(v->l);
  }
  return v;
}
```  

## Добавление

Операция вставки работает аналогично поиску элемента. Тут мы подвешиваем вершину за лист, а не вставляем внутрь. Мы спускаемся по дереву, чтобы найти пустое место для вершины и вставить в это место. 

Если текущая вершина пустая (`v == nullptr`), то сюда и надо вставить. Для этого вернём корректное состояния поддерева, а именно один новый элемент. 

При спуске в детей стоит сохранить состояние дерева, поэтому пишем `v->l = insert(v->l, x)` или `v->r = insert(v->r, x)`. Если мы находимся в вершине, ключ которой равен `x`, то вставлять ничего не надо, значит вернём текущую вершину.

```cpp
node* insert(node* v, T x) {
  if (v == nullptr) {
    return new node(x);
  } else if (x < v->x) {
    v->l = insert(v->l, x);
  } else if (x > v->x) {
    v->r = insert(v->r, x);
  }
  return v;
}
```


## Удаление

Операция удаления работает аналогично поиску элемента. Мы спускаемся по дереву, пока не встретим элемент, который стоит удалить. 

Для текущей вершины существует $4$ случая : детей у вершины нет, есть только левый ребёнок, есть только правый ребёнок, есть и левый и правый ребёнок.

В случае, если у вершины нет детей, стоит вернуть пустое поддерево &mdash; `nullptr`.

В случае, если есть только левый ребёнок, то для удаления текущей вершины, надо левого ребёнка сделать корнем текущего поддерева. В случае, если есть только правый ребёнок &mdash; аналогично.

В случае, если у вершины есть оба ребёнка, существует способ, который можно выразить через самого себя, то есть **рекурсивно**. Этот способ заключается в замене текущей вершины, на минимальную, из правого поддерева и **рекурсивное** удаление из правого поддерева, элемента, который теперь встречается два раза, а именно нового значения в корне.

Аналогично можно взять максимум из левого поддерева и удалить из левого поддерева.

```cpp
node* remove(node* v, T k) {
  if (!v) return v;
  if (k < v->x) {
    v->l = remove(v->l, k);
    return v;
  }
  if (v->x < k) {
    v->r = remove(v->r, k);
    return v;
  }
  if (v->l && v->r) {
    v->x = get_min(v->r)->x;
    v->r = remove(v->r, v->x);
  } else {
    if (v->l) {
      v = v->l;
    } else if (v->r) {
      v = v->r;
    } else {
      v = nullptr;
    }
  }
  return v;
}
```

## Задачи

### Восстановление дерева по результату preorder обхода

preorder &mdash; обход в котором сначала посещается и выводится корневой узел, затем левое и правое поддеревья.

По такому обходу однозначно можно восстановить дерево. В принципе я его написал, что красиво выводить картинки.

Существует очень простое решение. Пусть дан обход $a = [a_0, a_1, \dots, a_n]$. Очевидно, что $a_0$ является корнем дерева, так как мы его вывели ранее, чем все остальные вершины. Все элементы меньшие $a_0$ будут в левом поддереве, а все остальные в правом. Причём обход имеет вид $[<a_0, \dots, < a_0, > a_0, \dots, > a_0]$. Значит можно найти первый элемент, больший $a_0$ и рекурсивно решить для двух частей, которые разделяются этим элементом.

Для нахождения следующего большего числа, можно воспользоваться обычным алгоритмом со стеком.


```cpp
node* build(int l, int r) {
  if (l > r) {
    return nullptr;
  }
  int p = nxt[l];
  node* res = new node(a[l]);
  res->l = build(l + 1, p - 1);
  res->r = build(p, r);
  return res;
}
```


## Асимптотика

Все операции над деревом такие, как вставка, удаление, поиск элементов &mdash; работают в среднем $O(\log n)$, где $n$ &mdash; количество вершин в дереве.

```admonish tile="Доказательство средней сложности"

* Если вы знаете строгое доказательство, то напишите мне и получите денежное вознаграждение.

Средняя асимптотика алгоритма считается с использованием математического ожидания. Однако, пропустим строгое доказательство, и просто будем ссылаться на какие-то факты. 

Дерево, построенное путём вставки случайной перестановки чисел от $1$ до $n$, имеет в среднем глубину $2 \log n$ для любой вершины в дереве. Доказательство можете прочитать в [википедии](https://en.wikipedia.org/wiki/Random_binary_tree#Expected_depth_of_a_node).

При использовании BST редко удаётся только вставлять и искать без изменения дерева, путём удаления некоторых вершин. Это ограничивает непосредственное применение случайных двоичных деревьев. Однако разработчики алгоритмов разработали структуры данных, которые позволяют выполнять вставки и удаления в дереве двоичного поиска, на каждом шаге сохраняя в качестве инварианта свойство, согласно которому форма дерева является случайной величиной с тем же распределением, что и случайное двоичное дерево поиска.
```

В худшем случае за высоту дерева. Это означает, что дерево без некоторой "ребалансировки" после некоторых вставок или удалений, может иметь высоту $n$, где $n$ количество вершин в дереве. 

Сохранение сбалансированности дерева поиска и его высоты, ограниченной $O(\log n)$, является ключевым условием полезности бинарного дерева поиска. Этого можно достичь с помощью механизмов "самобалансировки" при операциях обновления дерева, призванных поддерживать высоту дерева на уровне $\log n$. 

Деревья могут иметь разные механизмы самобалансировки, такие как :
1. Сбалансированные по высоте.
2. [Сбалансированные по весу деревья](https://en.wikipedia.org/wiki/Weight-balanced_tree) &mdash; не будем рассматривать в виду того, что на википедии приведён пример, но название структуре данных не дано. Если вы любите `Haskell` то изучите.

Существует несколько самобалансирующихся по высоте бинарных деревьев поиска : AVL, декартово, красно чёрное, $2-3$, Splay.


Худшее дерево для нас это бамбук &mdash; дерево с наибольшей возможной высотой. Высота бамбука равна количеству вершин в дереве. Вот бамбуки из примера в самом начале статьи :


~~~admonish collapsible=true title="бамбуки"
<div class="center">
<div class="angry-grid">
<div id="item32-0">```tree
0 1 2 3 
[0,1,2,3]
```</div>
<div id="item32-1">```tree
0 1 3 2 
[0,1,3,2]
```</div>
<div id="item32-2">```tree
0 3 1 2 
[0,3,1,2]
```</div>
<div id="item32-3">```tree
0 3 2 1 
[0,3,2,1]
```</div>
<div id="item32-4">```tree
3 0 1 2 
[3,0,1,2]
```</div>
<div id="item32-5">```tree
3 2 1 0 
[3,2,1,0]
```</div>
</div>
</div>
~~~

# Код

Не пугайтесь, я написал код используя шаблоны, чтобы потом легко использовать структуру. Для спуска по дереву, мы всегда проверяем ключи используя операторы `<`,`=`, `>`, так как `>` реализуется через `<` изменив порядок аргументов. Поэтому я ещё передал две функции (`equal` и `less`) в шаблон структуры.

> `recursive_free` сделан для очистки всех `node`, которых мы создаём через `new`. Хотя надо делать `free`, но поверьте надо делать `delete`, как минимум все мои анализаторы падают при `free`. `valgrind --leak-check=full ./a.out` выдаёт `==11816== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
` Это не особо нужно вам, просто очистит память, может быть полезно при `ML`.

~~~admonish collapsible=true title="код"
```cpp
template <typename T>
struct node {
 public:
  T key{};
  short int height = 0;
  node* left = nullptr;
  node* right = nullptr;

  node(T k) {
    key = k;
    left = nullptr;
    right = nullptr;
  }
};

template <typename T, bool (*eq_comparator)(const T&, const T&),
          bool (*less_comparator)(const T&, const T&)>
struct Tree {
  using node_t = node<T>;
  node_t* root;

  Tree() { root = nullptr; }

  void recursive_free(node_t* v) {
    if (!v) return;
    recursive_free(v->left);
    recursive_free(v->right);
    delete v;
  }

  ~Tree() { recursive_free(root); }

  node_t* get_min(node_t* v) {
    if (v != nullptr && v->left != nullptr) {
      return get_min(v->left);
    }
    return v;
  }

  node_t* insert(node_t* v, const T& x) {
    if (v == nullptr) {
      return new node_t(x);
    } else if (less_comparator(x, v->key)) {
      v->left = insert(v->left, x);
    } else if (less_comparator(v->key, x)) {
      v->right = insert(v->right, x);
    } else {
      v->key = x;
    }
    return v;
  }

  node_t* remove(node_t* v, const T& k) {
    if (!v) return v;
    if (less_comparator(k, v->key)) {
      v->left = remove(v->left, k);
    } else if (less_comparator(v->key, k)) {
      v->right = remove(v->right, k);
    } else if (v->left && v->right) {
      v->key = get_min(v->right)->key;
      v->right = remove(v->right, v->key);
    } else {
      if (v->left) {
        v = v->left;
      } else if (v->right) {
        v = v->right;
      } else {
        v = nullptr;
      }
    }
    return v;
  }

  node_t* search(node_t* v, const T& k) const {
    if (!v || eq_comparator(v->key, k)) {
      return v;
    }
    if (k < v->key) {
      return search(v->left, k);
    } else {
      return search(v->right, k);
    }
  }

  void insert(const T& x) { root = insert(root, x); }

  void erase(const T& x) { root = remove(root, x); }

  bool contains(const T& x) const { return search(root, x) != nullptr; }
};

```

Использование 

```cpp
template <typename T>
inline bool _equal(const T& a, const T& b) {
  return a == b;
}

template <typename T>
inline bool _less(const T& a, const T& b) {
  return a < b;
}

int main() {
  Tree<int, _equal<int>, _less<int>> t;
  t.insert(7);
  t.insert(4);
  assert(t.contains(7));
  return 0;
}
```
~~~


# Словарь

Словарь (dict) &mdash; полезная структура данных, **отсортированный** набор ключ-значение. В отличие от массивов, которые индексируются диапазоном чисел, словари индексируются ключами. Во многих языках, такая структура данных уже существует в стандартной библиотеки.
Не стоит путать с [Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) в  `python3` или с [`std::unordered_map`](https://en.cppreference.com/w/cpp/container/unordered_map) в `c++`, так как всё это хэшмаппа (хэштаблица) (**неупорядоченный** набор ключ-значений). Хэшмаппа использует другую идею &mdash; хэш-функцию.

В  `c++` стандартный словарь &mdash; [`std::map`](https://en.cppreference.com/w/cpp/container/map).

> Keys are sorted by using the comparison function Compare. Search, removal, and insertion operations have logarithmic complexity. Maps are usually implemented as Red–black trees. ([std::map](https://en.cppreference.com/w/cpp/container/map))

> Ключи уникальные &mdash; действительно похоже на множество =)

Основные операции словаря :

Поиск :

1. `iterator find(Key k)` &mdash; возвращает итератор на элемент, который ищет элемент с ключом равным `k`. (`.end()` если не находит) 
2. `iterator lower_bound/upper_bound(Key k)`  &mdash; аналогично `find`-у и обычному `lower_bound`-у.

Модификация :

1. `iterator insert(value_type v)` &mdash; вставляет элемент. Элемент &mdash; пара из ключа и значения.
2. `iterator erase(value_type v)` &mdash; аналогично удаляет.

Итератор, который возвращается, по сути не особо нужен.

Оператор `[]`

1. `value_type& operator[] (const key_type& k)` &mdash; возвращает значение по ключу, которое **можно** изменить.
2. `value_type operator[] (const key_type& k)` &mdash; возвращает значение по ключу, которое **нельзя** изменить.

~ Два раза определён `[]`, так как существует различные применения, когда вы пишите `cout << m["mykey"]` и когда вы пишите `m["mykey"] = 123`. Для первого надо написать `V operator[](const K &key)`, для второго `V operator[](const K &key)` соответственно. Это `c++` =) 

# Реализация словаря

Немного подумав, можно построить двоичное дерево поиска, где `node`, хранит и ключ и значение.

Для всех функций поиска и взятия элемента (`[]`), нужно спускаться в дереве по ключам, а значение мы храним как доп поле в `node`-е. Я построю дерево на элементах пар ключ-значение, и напишу своё сравнение, лишь по ключу.

Итераторы оставлю на подумать. Для неё надо написать свою обёртку над итераторами, и функцию для поиска следующего ключа в дереве (собственно я не написал это в статье про дерево, так как это не очень сложно). + особо и не надо

```cpp
template <typename K, typename V>
struct Map {
  using T = std::pair<K, V>;

  inline static bool equal(const T& a, const T& b) {
    return a.first == b.first;
  }  // сравниваем только ключи

  inline static bool less(const T& a, const T& b) { return a.first < b.first; }

  Tree<T, equal, less> mem;

  V& operator[](const K& key) {
    auto ptr = mem.search(mem.root, {key, {}});
    if (ptr == nullptr) {
      mem.insert({key, {}});
      ptr = mem.search(mem.root, {key, {}});
    }
    return ptr->key.second;
  }

  V operator[](const K& key) const {
    return mem.search(mem.root, {key, {}})->key.second;
  }

  bool contains(const K& key) const { return mem.contains({key, {}}); }
};
```

В `V& operator[](const K &key)`, есть проверка, когда ключа нет, для этого надо вставить `node`-у в дерево, и сделать поиск по новой, в таком случае у нас будет валидный указатель.

# Применение 

В реальной жизни пишут самобалансирующиеся деревья. В `stl` есть уже существующее дерево &mdash; `std::set`.