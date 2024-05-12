"""
Порівняти ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових файлів (стаття 1, стаття 2).
 Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті,
  та іншого — вигаданого (вибір підрядків за вашим бажанням).
  На основі отриманих даних визначити найшвидший алгоритм для кожного тексту окремо та в цілому.
"""
import timeit

with open("article_1", "r", encoding="utf-8") as file:
    text1 = file.read()

with open("article_2", "r", encoding="utf-8") as file:
    text2 = file.read()


# Алгоритми пошуку підрядка
def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


def rabin_karp_search(text, pattern):
    # Довжини основного рядка та підрядка пошуку
    pattern_length = len(pattern)
    text_length = len(text)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    pattern_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:pattern_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, pattern_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(text_length - pattern_length + 1):
        if pattern_hash == current_slice_hash:
            if text[i:i + pattern_length] == pattern:
                return i

        if i < text_length - pattern_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + pattern_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def measure_time(algorithm, text, pattern):
    start_time = timeit.default_timer()
    algorithm(text, pattern)
    return timeit.default_timer() - start_time


def search_in_article(text_name, text, real_pattern, fake_pattern):
    for algorithm in [boyer_moore_search, kmp_search, rabin_karp_search]:
        real_time = measure_time(algorithm, text, real_pattern)
        fake_time = measure_time(algorithm, text, fake_pattern)
        print(f"Алгоритм: {algorithm.__name__}, Текст: {text_name}")
        print(f"Час для дійсного підрядка: {real_time}")
        print(f"Час для вигаданого підрядка: {fake_time}")
        print()


real_pattern = "Тому основне завдання програміста - аналізувати і вирішувати проблеми"
fake_pattern = "nonexistent_pattern"

search_in_article("article_1", text1, real_pattern, fake_pattern)

real_pattern = "Структуры данных и алгоритмы."
fake_pattern = "nonexistent_pattern"
search_in_article("article_2", text2, real_pattern, fake_pattern)
