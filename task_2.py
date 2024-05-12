"""
Реалізувати двійковий пошук для відсортованого масиву з дробовими числами.
Написана функція для двійкового пошуку повинна повертати кортеж, де першим елементом є кількість ітерацій, потрібних
для знаходження елемента. Другим елементом має бути "верхня межа" — це найменший елемент,
який є більшим або рівним заданому значенню.
"""


def binary_search1(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1

        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1

        # інакше x присутній на позиції і повертаємо його
        else:
            return mid

    # якщо елемент не знайдений
    return -1

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iterations = 0

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1

        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1

        # інакше x присутній на позиції і повертаємо його
        else:
            return (iterations, arr[mid])

    # якщо елемент не знайдений, повертаємо кортеж з кількістю ітерацій та "верхньою межею"
    if high >= 0 and high < len(arr):
        upper_bound = arr[high] if arr[high] >= x else arr[high + 1] if high + 1 < len(arr) else None
        return (iterations, upper_bound)
    else:
        return (iterations, None)

# Приклад використання:
arr = [0.1, 0.5, 0.7, 1.2, 1.4, 2.0, 2.5, 3.1, 4.0]
target = 1.3

iterations, upper_bound = binary_search(arr, target)
print("Кількість ітерацій:", iterations)
print("Верхня межа:", upper_bound)