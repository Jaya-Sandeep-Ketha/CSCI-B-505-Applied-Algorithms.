import random
import time
import matplotlib.pyplot as plt

def det_partition(my_array, my_lb, my_ub):
    my_pivot = my_array[my_lb]
    array_start = my_lb
    array_end = my_ub
    while array_start < array_end:
        while array_start <= my_ub and my_array[array_start] <= my_pivot:
            array_start += 1
        while my_array[array_end] > my_pivot:
            array_end -= 1
        if array_start < array_end:
            my_array[array_start], my_array[array_end] = my_array[array_end], my_array[array_start]
    my_array[my_lb], my_array[array_end] = my_array[array_end], my_array[my_lb]
    return array_end

def find_median(my_array):
    n = len(my_array)
    target_index = n // 2
    my_lb = 0
    my_ub = n - 1
    while True:
        pivot_loc = det_partition(my_array, my_lb, my_ub)

        if target_index == pivot_loc:
            return my_array[pivot_loc]
        elif target_index < pivot_loc:
            my_ub = pivot_loc - 1
        else:
            my_lb = pivot_loc + 1
            target_index -= pivot_loc + 1

# Benchmarking code
input_sizes = list(range(0, 10001, 300))
deterministic_sort_sorted_times = []
deterministic_sort_random_times = []

for size in input_sizes:
    sorted_array = list(range(1, size + 1))
    random_array = sorted_array.copy()
    random.shuffle(random_array)
    
    start_time = time.time()
    _ = find_median(sorted_array)
    end_time = time.time()
    deterministic_sort_sorted_times.append(end_time - start_time)
        
    start_time = time.time()
    _ = find_median(random_array)
    end_time = time.time()
    deterministic_sort_random_times.append(end_time - start_time)

# Creating a plot
plt.figure(figsize=(10, 6))
plt.plot(input_sizes, deterministic_sort_sorted_times, label='Median Deterministic Sort (Sorted)')
plt.plot(input_sizes, deterministic_sort_random_times, label='Median Deterministic Sort (Random)')

# Adding labels and legend
plt.xlabel('Input Size')
plt.ylabel('Execution Time (seconds)')
plt.legend()

# Show the plot
plt.show()
