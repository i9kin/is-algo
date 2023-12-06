# AVL

Теорию прочитайте :

* [тут](https://habr.com/ru/articles/150732/)
* [тут](https://neerc.ifmo.ru/wiki/index.php?title=%D0%90%D0%92%D0%9B-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BE)

Отличие кода AVL от бинарного дерева поиска заключается лишь в **добавление** нового функционала поверх существующего кода :

1. Добавить поле `height` в `node`.
2. Добавить функции для вычисления баланса, и обновления его.
3. Добавить `rightRotation(v)` и `leftRotation(v)` &mdash; функции поворотов.
4. Добавить `balance(v)` &mdash; функция, которая вызывает, если надо, нужный поворот.
5. Вызвать функцию `return balance(v)` вместо `return v;` для всех функций, которые изменяют дерево, а именно `insert`, `remove`.


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
    height = 1;
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

  short int height(node_t* p) { return p ? p->height : 0; }

  short int balance_(node_t* p) { return height(p->right) - height(p->left); }

  void upd(node_t* p) {
    p->height = max(height(p->left), height(p->right)) + 1;
  }

  node_t* get_min(node_t* v) {
    if (v != nullptr && v->left != nullptr) {
      return get_min(v->left);
    }
    return v;
  }

  node_t* rightRotation(node_t* head) {
    node_t* newhead = head->left;
    head->left = newhead->right;
    newhead->right = head;
    upd(head), upd(newhead);
    return newhead;
  }

  node_t* leftRotation(node_t* head) {
    node_t* newhead = head->right;
    head->right = newhead->left;
    newhead->left = head;
    upd(head), upd(newhead);
    return newhead;
  }

  node_t* balance(node_t* p) {
    if (!p) return p;
    upd(p);
    if (balance_(p) == 2) {
      if (balance_(p->right) < 0) p->right = rightRotation(p->right);
      return leftRotation(p);
    }
    if (balance_(p) == -2) {
      if (balance_(p->left) > 0) p->left = leftRotation(p->left);
      return rightRotation(p);
    }
    return p;
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
    return balance(v);
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
    return balance(v);
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
~~~