# "Пузырьковая сортировка" (Bubble sort)

Самая простая из предложенных сортировок, представляющая собой перебор элементов массива и сравнение каждого с каждым

Сложность: *** до O(n^2)***

> Данной сортировкой пользуются крайне редко из-за скорости её работы, поскольку при обработке массива с большим количествоми элементов время может стремиться к бесконечности
> Более предпочтительными будут сортировки, представленные в других разделах этой темы


## Обычная версия алгоритма

```cpp
#include <iostream>

// Функция Swap меняет значения переменных местами
void Swap( int *Value1, int *Value2 ) {
    int tmp = *Value1;

    *Value1 = *Value2;
    *Value2 = tmp;
}

// Функция "пузырьковой сортировки"
void BubbleSort( int *Arr, int size ) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size - 1; j++) {
            if (Arr[j] > Arr[j + 1]) {
                Swap(&Arr[j], &Arr[j + 1]);
            }
        }
    }
}

int main( void ) {
    int size, *Array;

    std::cin >> size;

    Array = new int[size];           // Выделение памяти под динамический целочисленный массив размера size

    for (int i = 0; i < size; i++) { // Заполнение массива Array
        std::cin >> Array[i];         
    }

    BubbleSort(Array, size);         // Выполнение сортировки

    for (int i = 0; i < size; i++) { // Вывод отсортированного массива
        std::cout << Array[i] << ' ';
    }
}
```

## Ускоренная версия алгоритма

```cpp
#include <iostream>

// Функция Swap меняет значения переменных местами
void Swap( int *Value1, int *Value2 ) {
    int tmp = *Value1;

    *Value1 = *Value2;
    *Value2 = tmp;
}

// Функция "пузырьковой сортировки"
void BubbleSort( int *Arr, int size ) {
    for (int i = 0; i < size; i++) {
        bool is_any_swapped = false;

        for (int j = 0; j < size - 1; j++) {
            if (Arr[j] > Arr[j + 1]) {
                Swap(&Arr[j], &Arr[j + 1]);
                is_any_swapped = true;
            }
        }

        // Если ни один элемент не поменялся местами с соседом, значит, что массив уже отсортирован
        if (!is_any_swapped) {
            break;
        }
    }
}

int main( void ) {
    int size, *Array;

    std::cin >> size;

    Array = new int[size];           // Выделение памяти под динамический целочисленный массив размера size

    for (int i = 0; i < size; i++) { // Заполнение массива Array
        std::cin >> Array[i];         
    }

    BubbleSort(Array, size);         // Выполнение сортировки

    for (int i = 0; i < size; i++) { // Вывод отсортированного массива
        std::cout << Array[i] << ' ';
    }
}
```

## Пример работы алгоритма

Ввод:

```bash
5
1 9 45 7 -2
```

Вывод:
```bash
-2 1 7 9 45
```