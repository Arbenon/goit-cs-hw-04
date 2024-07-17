import threading
import time
from collections import defaultdict

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(file, keywords, results):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file)
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Функція для обробки файлів у потоці
def process_files(files, keywords, results):
    for file in files:
        search_keywords_in_file(file, keywords, results)

# Основна функція для багатопотокового пошуку
def threaded_search(files, keywords, num_threads):
    results = defaultdict(list)
    threads = []
    files_per_thread = len(files) // num_threads

    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = None if i == num_threads - 1 else (i + 1) * files_per_thread
        thread = threading.Thread(target=process_files, args=(files[start_index:end_index], keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  # Список ваших файлів
    keywords = []

    print("Введіть ключові слова. Введіть 'STOP' для завершення введення.")
    while True:
        keyword = input("Введіть ключове слово: ")
        if keyword.upper() == 'STOP':
            break
        keywords.append(keyword)

    num_threads = 4  # Кількість потоків

    start_time = time.time()
    results = threaded_search(files, keywords, num_threads)
    end_time = time.time()

    print(f'Threaded search took {end_time - start_time:.2f} seconds')
    print(dict(results))
