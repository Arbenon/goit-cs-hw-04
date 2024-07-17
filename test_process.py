import multiprocessing
import time
from collections import defaultdict

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(file, keywords, queue):
    results = defaultdict(list)
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file)
        queue.put(results)
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Функція для обробки файлів у процесі
def process_files(files, keywords, queue):
    for file in files:
        search_keywords_in_file(file, keywords, queue)

# Основна функція для багатопроцесорного пошуку
def multiprocessing_search(files, keywords, num_processes):
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    processes = []
    files_per_process = len(files) // num_processes

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = None if i == num_processes - 1 else (i + 1) * files_per_process
        process = multiprocessing.Process(target=process_files, args=(files[start_index:end_index], keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = defaultdict(list)
    while not queue.empty():
        result = queue.get()
        for keyword, files in result.items():
            results[keyword].extend(files)

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

    num_processes = 4  # Кількість процесів

    start_time = time.time()
    results = multiprocessing_search(files, keywords, num_processes)
    end_time = time.time()

    print(f'Multiprocessing search took {end_time - start_time:.2f} seconds')
    print(results)
