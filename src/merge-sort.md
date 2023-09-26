# Сортировка слиянием

> Merge sort - рекурсивный алгоритм сортировки, разбивающий основной массив на подмассивы, сортирующий их и собирающий всё обратно в отсортированном виде

Сложность: ***O(n log(n))***

## Преимущества алгоритма
1. Стабильный алгоритм
2. Сложность алгоритма в худшем случае - O(n log(n)), следовательно, он хорош для больших массивов
3. Алгоритм параллелен - его можно спокойно ускорить, разбив действия на разные потоки процессора

## Недостатки алгоритма
1. Требователен к памяти
2. Не всегда оптимален для маленьких массивов

## Реализация алгоритма №1

```cpp
void merge(int* a, int left, int mid, int right) {
  int subArrayOne = mid - left + 1;
  int subArrayTwo = right - mid;

  // Создание временных массивов
  int *leftArray = new int[subArrayOne], *rightArray = new int[subArrayTwo];

  // Копирование данных в подмассивы
  for (auto i = 0; i < subArrayOne; i++) {
    leftArray[i] = a[left + i];
  }

  for (auto j = 0; j < subArrayTwo; j++) {
    rightArray[j] = a[mid + 1 + j];
  }

  int indexOfSubArrayOne = 0, indexOfSubArrayTwo = 0, indexOfMergedArray = left;

  // Соединение временных массивов в наш изначальный
  while (indexOfSubArrayOne < subArrayOne && indexOfSubArrayTwo < subArrayTwo) {
    if (leftArray[indexOfSubArrayOne] <= rightArray[indexOfSubArrayTwo]) {
      a[indexOfMergedArray] = leftArray[indexOfSubArrayOne];
      indexOfSubArrayOne++;
    } else {
      a[indexOfMergedArray] = rightArray[indexOfSubArrayTwo];
      indexOfSubArrayTwo++;
    }
    indexOfMergedArray++;
  }

  // Копирование оставшихся элементов левого ммассива, если они остались
  while (indexOfSubArrayOne < subArrayOne) {
    a[indexOfMergedArray] = leftArray[indexOfSubArrayOne];
    indexOfSubArrayOne++;
    indexOfMergedArray++;
  }

  // Копирование оставшихся элементов правого ммассива, если они остались
  while (indexOfSubArrayTwo < subArrayTwo) {
    a[indexOfMergedArray] = rightArray[indexOfSubArrayTwo];
    indexOfSubArrayTwo++;
    indexOfMergedArray++;
  }

  // Удалить массивы и очистить память
  delete[] leftArray;
  delete[] rightArray;
}

// begin отвечает за левый индекс, end - за правый
void mergeSort(int* array, int begin, int end) {
  if (begin >= end) return;

  int mid = begin + (end - begin) / 2;

  // Сортировка и соединение массива
  mergeSort(array, begin, mid);
  mergeSort(array, mid + 1, end);
  merge(array, begin, mid, end);
}
```

## Реализация алгоритма №2

Используем глобальный массив, вместо временных `leftArray` и `rightArray`.

```cpp
int* B;

// Рекурсивная часть сортировки
void mergeSortRec(int* a, int size) {
  if (size < 2) {
    return;
  }

  int M = size / 2;

  // Вызов рекурсии
  mergeSortRec(a, M);
  mergeSortRec(a + M, size - M);

  // Копируем данный в левый и правый массивы
  for (int k = 0, i = 0, j = M; k < size; ++k) {
    // Записываем меньшее значение в k-й элемент массива B
    if (j >= size || i < M && a[i] < a[j]) {
      B[k] = a[i++];
    } else {
      B[k] = a[j++];
    }
  }  // Если один из массивов закончится, то просто запишется остаток другого
     // массива

  // Копируем данные в исходный массив
  for (int i = 0; i < size; i++) {
    a[i] = B[i];
  }
}

// Функция, вызывающая сортировку
void mergeSort(int* a, int size) {
  B = new int[size];

  if (B == nullptr) return;

  mergeSortRec(a, size);

  delete[] B;
}
```

> Запуск функции сортировки `mergeSort(arr, 0, size - 1);`

## Ввод

```bash 
4
49 12 -3 15
```

## Работа алгоритма

1. Разбиение массива { 49 12 -3 15 } на два подмассива { 49 12 } и { -3 15 }
2. Разбиение подмассивов на части { 49 } и { 12 }, { -3 } и { 15 }
3. Сборка отсортированных подмассивов: { 12 49 } и { -3 15 }
4. Сборка массива из подмассивов: { -3 12 15 49 }

## Вывод

```bash 
-3 12 15 49
```