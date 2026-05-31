"""Алгоритмы сортировок с записью действий в массив actions."""

def bubble_sort_rec(arr, actions):
    """Сортировка пузырьком."""

    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            actions.append(('compare', j, j + 1))
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                actions.append(('swap', j, j + 1))

def selection_sort_rec(arr, actions):
    """Сортировка выборкой."""

    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            actions.append(('compare', j, min_idx))
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            actions.append(('swap', i, min_idx))

def insertion_sort_rec(arr, actions):
    """Сортировка вставками."""

    n = len(arr)
    for i in range(1, n):
        j = i
        while j > 0 and arr[j] < arr[j - 1]:
            actions.append(('compare', j, j - 1))
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            actions.append(('swap', j, j - 1))
            j -= 1

SORT_ALGORITHMS = {
    "Bubble": bubble_sort_rec,
    "Insertion": insertion_sort_rec,
    "Selection": selection_sort_rec
}
SORT_TYPES = list(SORT_ALGORITHMS.keys())
