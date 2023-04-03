import time
import threading

def sleep_sort(numbers):
    def output(x):
        time.sleep(x/100)
        print(x)

    threads = []
    for num in numbers:
        thread = threading.Thread(target=output, args=(num,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    numbers = [10, 3, 6, 7, 8, 1, 2, 9, 5,12, 21,45,12,52345,6,123,23,41,4,21,3,423,423,5,21,352, 4]
    sleep_sort(numbers)