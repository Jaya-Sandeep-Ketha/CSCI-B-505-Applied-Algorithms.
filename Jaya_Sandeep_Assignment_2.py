import random
import time
import unittest

#----------------------Defining Merge Sort-------------------------------------------------#
def merge_sort(arr):
    # Check if the input array has more than one element
    if len(arr) > 1:
        # Find the middle of the array
        mid = len(arr) // 2
        # Split the array into two halves
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sort the left and right halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Initialize counters for merging
        i = j = k = 0

        # Merge the two sorted halves back into the original array
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        
        # Check for any remaining elements in the left and right halves
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def merge_sort_plus(my_array, k):
    # Base case: Return the array if it's already sorted or empty
    if len(my_array) <= 1:
        return my_array
    
    # Use the regular merge_sort function for k=2
    if k == 2:
        merge_sort(my_array)

    elif k == 3:
        third = len(my_array) // 3
        if len(my_array) <= 2:
            # If there are only 2 elements, swap them if necessary
            if my_array[0] > my_array[1]:
                my_array[0], my_array[1] = my_array[1], my_array[0]
            return my_array

        # Divide the array into three parts
        left_third = my_array[:third]
        middle_third = my_array[third:2 * third]
        right_third = my_array[2 * third:]

        # Recursively sort the three sub-arrays
        merge_sort_plus(left_third, k)
        merge_sort_plus(middle_third, k)
        merge_sort_plus(right_third, k)

        # Initialize counters for merging
        i = j = l = n = 0

        # Merge the three sorted sub-arrays back into the original array
        while i < len(left_third) or j < len(middle_third) or l < len(right_third):
            min_left = left_third[i] if i < len(left_third) else float('inf')
            min_middle = middle_third[j] if j < len(middle_third) else float('inf')
            min_right = right_third[l] if l < len(right_third) else float('inf')

            min_val = min(min_left, min_middle, min_right)

            # Place the minimum value in the merged array
            if min_val == min_left:
                my_array[n] = left_third[i]
                i += 1
            elif min_val == min_middle:
                my_array[n] = middle_third[j]
                j += 1
            else:
                my_array[n] = right_third[l]
                l += 1

            n += 1

    elif k == 4:
        fourth = len(my_array) // 4
        if len(my_array) <= 3:
            for i in range(len(my_array)):
                min_index = i
                for j in range(i + 1, len(my_array)):
                    if my_array[j] < my_array[min_index]:
                        min_index = j
                my_array[i], my_array[min_index] = my_array[min_index], my_array[i]

        else:
            # Divide the array into four sub-arrays
            left_fourth = my_array[:fourth]
            middle_left_fourth = my_array[fourth:2 * fourth]
            middle_right_fourth = my_array[2 * fourth:3 * fourth]
            right_fourth = my_array[3 * fourth:]

            # Recursively sort the four sub-arrays
            merge_sort_plus(left_fourth, k)
            merge_sort_plus(middle_left_fourth, k)
            merge_sort_plus(middle_right_fourth, k)
            merge_sort_plus(right_fourth, k)

            # Initialize counters for merging
            i = j = l = m = n = p = 0

            # Merge the four sorted sub-arrays back into the original array
            while i < len(left_fourth) or j < len(middle_left_fourth) or l < len(middle_right_fourth) or m < len(right_fourth):
                min_left = left_fourth[i] if i < len(left_fourth) else float('inf')
                min_middle_left = middle_left_fourth[j] if j < len(middle_left_fourth) else float('inf')
                min_middle_right = middle_right_fourth[l] if l < len(middle_right_fourth) else float('inf')
                min_right = right_fourth[m] if m < len(right_fourth) else float('inf')

                 # Find the minimum value among the elements from the four sub-arrays
                min_val = min(min_left, min_middle_left, min_middle_right, min_right)

                # Place the minimum value in the merged array
                if min_val == min_left:
                    my_array[n] = left_fourth[i]
                    i += 1
                elif min_val == min_middle_left:
                    my_array[n] = middle_left_fourth[j]
                    j += 1
                elif min_val == min_middle_right:
                    my_array[n] = middle_right_fourth[l]
                    l += 1
                else:
                    my_array[n] = right_fourth[m]
                    m += 1

                n += 1

    return my_array

#---------------------------------Definining Random Quick Sort----------------------------------------------#  
def random_qs_plus(my_array, k):
    # Condition to check if the count of unique values is less than 2
    if len(set(my_array)) < 2:
        return my_array
    
    # Print warning for invalid 'k' values
    if k < 2 or k > 4:
        print("Enter valid k value between 2 to 4") 

    # Base case: return the array if it's empty or has one element
    if len(my_array) <= 1:
        return my_array  

    if k == 2:
        # Choose a random pivot element from the array
        pivot = random.choice(my_array)
        # Partition the array into elements less than or equal to the pivot and elements greater than the pivot
        left = [x for x in my_array if x <= pivot]
        right = [x for x in my_array if x > pivot]
        # Recursively sort and concatenate the left and right partitions
        return random_qs_plus(left, k) + random_qs_plus(right, k)

    elif k == 3:
      if len(my_array) <=2:
        # If there are two or fewer elements, swap them if necessary to ensure sorting
        if my_array[0]>my_array[1]:
          my_array[0], my_array[1] = my_array[1], my_array[0]

        return my_array

      else:
        # Choose two random pivots and sort them
        pivot_1, pivot_2 = random.sample(my_array, 2)

        if pivot_1 > pivot_2:
          pivot_1, pivot_2 = pivot_2, pivot_1

        # Partition the array into elements less than or equal to pivot_1, between pivot_1 and pivot_2, and greater than pivot_2
        left = [x for x in my_array if x <= pivot_1]
        middle = [x for x in my_array if pivot_1 < x <= pivot_2]
        right = [x for x in my_array if x > pivot_2]
        # Recursively sort and concatenate the partitions
        return random_qs_plus(left, k) + random_qs_plus(middle, k) + random_qs_plus(right, k)

    elif k == 4:
      if len(my_array)<=3:
        n = len(my_array)
        for i in range(n):
          for j in range(0, n-i-1):
            if my_array[j] > my_array[j+1]:
              my_array[j], my_array[j+1] = my_array[j+1], my_array[j]

        return my_array

      else:
        # Choose three random pivots and sort them
        pivot_1, pivot_2, pivot_3 = random.sample(my_array, 3) 

        # Compare and swap values to ensure pivot_1 <= pivot_2 <= pivot_3
        if pivot_1 > pivot_2:
          pivot_1, pivot_2 = pivot_2, pivot_1
        if pivot_2 > pivot_3:
          pivot_2, pivot_3 = pivot_3, pivot_2
        if pivot_1 > pivot_2:
          pivot_1, pivot_2 = pivot_2, pivot_1
        # Partition the array into elements less than or equal to pivot_1, between pivot_1 and pivot_2, between pivot_2 and pivot_3, and greater than pivot_3
        left = [x for x in my_array if x <= pivot_1]
        middle1 = [x for x in my_array if pivot_1 < x <= pivot_2]
        middle2 = [x for x in my_array if pivot_2 < x <= pivot_3]
        right = [x for x in my_array if x > pivot_3]
        # Recursively sort and concatenate the partitions
        return random_qs_plus(left, k) + random_qs_plus(middle1,k) + random_qs_plus(middle2, k) + random_qs_plus(right, k)

#---------------------------------------------------UNIT TESTING----------------------------------------------------------------------------------#
#-------- Creating a Sorting_Algorithms_Test class for unit testing of algorithms.-----------------------------------------------------------#
class Sorting_Algorithms_Test(unittest.TestCase):
    def setUp(self):
      # Initializing an empty array for testing
      self.empty_array = []

      # Initializing a single-element array for testing
      self.single_element_array = [17]

      # Initializing a sorted array for testing
      self.sorted_array = list(range(1, 17001))

      # Initializing a reversed sorted array for testing
      self.reverse_sorted_array = list(range(17000, 0, -1))

      # Initializing a random array for testing
      self.random_array = self.sorted_array.copy()
      random.shuffle(self.random_array)

      #Initializing a negative array for testing
      self.negative_array = self.sorted_array.copy()
      for i in self.negative_array:
        self.negative_array[i] = self.negative_array[i] * -1

      random.shuffle(self.negative_array)

      # Initializing a random decimal array for testing
      # Specify the length of the array
      array_length = 100
      # Generate an array of random decimal values between 0 and 1000
      self.random_decimal_array = [random.uniform(0, 1000) for _ in range(array_length)]
      self.sorted_decimal_array = sorted(self.random_decimal_array)
      

    #----------------------------------------------------------Randomized Quick Sort Test Cases for k = 2-------------------------------------------------------#
    def test_random_qs_empty_array_k2(self):
      # Testing by sorting an empty array
      sorted_array = random_qs_plus(self.empty_array, 2)
      self.assertEqual(sorted_array, [])

    def test_random_qs_single_element_array_k2(self):
      # Testing by sorting a single-element array
      sorted_array = random_qs_plus(self.single_element_array, 2)
      self.assertEqual(sorted_array, [17])

    def test_random_qs_sorted_array_k2(self):
      # Testing by sorting an already sorted array
      sorted_array = random_qs_plus(self.sorted_array, 2)
      self.assertEqual(sorted_array, list(range(1, 17001)))

    def test_random_qs_reverse_sorted_array_k2(self):
      # Testing by sorting a reverse sorted array
      sorted_array = random_qs_plus(self.reverse_sorted_array, 2)
      self.assertEqual(sorted_array, list(range(1, 17001)))

    def test_random_qs_random_array_k2(self):
      # Testing by sorting a random array
      sorted_array = random_qs_plus(self.random_array, 2)
      self.assertEqual(sorted_array, sorted(self.random_array))

    def test_random_qs_negative_array_k2(self):
      # Testing by sorting a negative array
      sorted_array = random_qs_plus(self.negative_array, 2)
      self.assertEqual(sorted_array, sorted(self.negative_array))

    def test_random_qs_decimal_array_k2(self):
      # Testing by sorting a decimal array
      sorted_array = random_qs_plus(self.random_decimal_array, 2)
      self.assertEqual(sorted_array, self.sorted_decimal_array)

    #----------------------------------------------------------Randomized Quick Sort Test Cases for k = 3-------------------------------------------------------#
    def test_random_qs_empty_array_k3(self):
      # Testing by sorting an empty array
      sorted_array = random_qs_plus(self.empty_array, 3)
      self.assertEqual(sorted_array, [])

    def test_random_qs_single_element_array_k3(self):
      # Testing by sorting a single-element array
      sorted_array = random_qs_plus(self.single_element_array, 3)
      self.assertEqual(sorted_array, [17])

    def test_random_qs_sorted_array_k3(self):
      # Testing by sorting an already sorted array
      sorted_array = random_qs_plus(self.sorted_array, 3)
      self.assertEqual(sorted_array, list(range(1, 17001)))

    def test_random_qs_reverse_sorted_array_k3(self):
      # Testing by sorting a reverse sorted array
      sorted_array = random_qs_plus(self.reverse_sorted_array, 3)
      self.assertEqual(sorted_array, list(range(1, 17001)))

    def test_random_qs_random_array_k3(self):
      # Testing by sorting a random array
      sorted_array = random_qs_plus(self.random_array, 3)
      self.assertEqual(sorted_array, sorted(self.random_array))

    def test_random_qs_negative_array_k3(self):
      # Testing by sorting a negative array
      sorted_array = random_qs_plus(self.negative_array, 3)
      self.assertEqual(sorted_array, sorted(self.negative_array))

    def test_random_qs_decimal_array_k3(self):
      # Testing by sorting a decimal array
      sorted_array = random_qs_plus(self.random_decimal_array, 3)
      self.assertEqual(sorted_array, self.sorted_decimal_array)


    #----------------------------------------------------------Randomized Quick Sort Test Cases for k = 4-------------------------------------------------------#
    def test_random_qs_empty_array_k4(self):
      # Testing by sorting an empty array
      sorted_array = random_qs_plus(self.empty_array, 4)
      self.assertEqual(sorted_array, [])

    def test_random_qs_single_element_array_k4(self):
      # Testing by sorting a single-element array
      sorted_array = random_qs_plus(self.single_element_array, 4)
      self.assertEqual(sorted_array, [17])

    def test_random_qs_sorted_array_k4(self):
      # Testing by sorting an already sorted array
      sorted_array = random_qs_plus(self.sorted_array, 4)
      self.assertEqual(sorted_array, list(range(1, 17001)))

    def test_random_qs_reverse_sorted_array_k4(self):
      # Testing by sorting a reverse sorted array
      sorted_array = random_qs_plus(self.reverse_sorted_array, 4)
      self.assertEqual(sorted_array, list(range(1, 17001)))

    def test_random_qs_random_array_k4(self):
      # Testing by sorting a random array
      sorted_array = random_qs_plus(self.random_array, 4)
      self.assertEqual(sorted_array, sorted(self.random_array))

    def test_random_qs_negative_array_k4(self):
      # Testing by sorting a negative array
      sorted_array = random_qs_plus(self.negative_array, 4)
      self.assertEqual(sorted_array, sorted(self.negative_array))

    def test_random_qs_decimal_array_k4(self):
      # Testing by sorting a decimal array
      sorted_array = random_qs_plus(self.random_decimal_array, 4)
      self.assertEqual(sorted_array, self.sorted_decimal_array)
      
  #----------------------------------------------------------Merge Sort Test Cases for k = 2-------------------------------------------------------#
    def test_merge_sort_empty_array_k2(self):
      # Testing by sorting an empty array
        merge_sort_plus(self.empty_array, 2)
        self.assertEqual(self.empty_array, [])

    def test_merge_sort_single_element_array_k2(self):
      # Testing by sorting a single-element array
        merge_sort_plus(self.single_element_array, 2)
        self.assertEqual(self.single_element_array, [17])
    
    def test_merge_sort_sorted_array_k2(self):
        # Testing by sorting an already sorted array
        merge_sort_plus(self.sorted_array, 2)
        self.assertEqual(self.sorted_array, list(range(1, 17001)))

    def test_merge_sort_reverse_sorted_array_k2(self):
        # Testing by sorting a reverse sorted array
        merge_sort_plus(self.reverse_sorted_array, 2)
        self.assertEqual(self.reverse_sorted_array, list(range(1, 17001)))

    def test_merge_sort_random_array_k2(self):
        # Testing by sorting a random array
        merge_sort_plus(self.random_array, 2)
        self.assertEqual(self.random_array, sorted(self.random_array))

    def test_merge_sort_negative_array_k2(self):
        # Testing by sorting a negative array
        merge_sort_plus(self.negative_array, 2)
        self.assertEqual(self.negative_array, sorted(self.negative_array))

    def test_merge_sort_decimal_array_k2(self):
        # Testing by sorting a decimal array
        merge_sort_plus(self.random_decimal_array, 2)
        self.assertEqual(self.random_decimal_array, self.sorted_decimal_array)
    #-------------------------------------------------------------Merge Sort Test Cases for k = 3-------------------------------------------------------#

    def test_merge_sort_empty_array_k3(self):
      # Testing by sorting an empty array
      merge_sort_plus(self.empty_array, 3)
      self.assertEqual(self.empty_array, [])

    def test_merge_sort_single_element_array_k3(self):
      # Testing by sorting a single-element array
      merge_sort_plus(self.single_element_array, 3)
      self.assertEqual(self.single_element_array, [17])

    def test_merge_sort_sorted_array_k3(self):
      # Testing by sorting an already sorted array
      merge_sort_plus(self.sorted_array, 3)
      self.assertEqual(self.sorted_array, list(range(1, 17001)))

    def test_merge_sort_reverse_sorted_array_k3(self):
      # Testing by sorting a reverse sorted array
      merge_sort_plus(self.reverse_sorted_array, 3)
      self.assertEqual(self.reverse_sorted_array, list(range(1, 17001)))

    def test_merge_sort_random_array_k3(self):
      # Testing by sorting a random array
      merge_sort_plus(self.random_array, 3)
      self.assertEqual(self.random_array, sorted(self.random_array))

    def test_merge_sort_negative_array_k3(self):
      # Testing by sorting a negative array
      merge_sort_plus(self.negative_array, 3)
      self.assertEqual(self.negative_array, sorted(self.negative_array))

    def test_merge_sort_decimal_array_k3(self):
      # Testing by sorting a decimal array
      merge_sort_plus(self.random_decimal_array, 3)
      self.assertEqual(self.random_decimal_array, self.sorted_decimal_array)

  #-------------------------------------------------------Merge Sort Test Cases for k = 4-------------------------------------------------------#
    def test_merge_sort_empty_array_k4(self):
        # Testing by sorting an empty array
        merge_sort_plus(self.empty_array, 4)
        self.assertEqual(self.empty_array, [])

    def test_merge_sort_single_element_array_k4(self):
        # Testing by sorting a single-element array
        merge_sort_plus(self.single_element_array, 4)
        self.assertEqual(self.single_element_array, [17])

    def test_merge_sort_sorted_array_k4(self):
        # Testing by sorting an already sorted array
        merge_sort_plus(self.sorted_array, 4)
        self.assertEqual(self.sorted_array, list(range(1, 17001)))

    def test_merge_sort_reverse_sorted_array_k4(self):
        # Testing by sorting a reverse sorted array
        merge_sort_plus(self.reverse_sorted_array, 4)
        self.assertEqual(self.reverse_sorted_array, list(range(1, 17001)))

    def test_merge_sort_random_array_k4(self):
        # Testing by sorting a random array
        merge_sort_plus(self.random_array, 4)
        self.assertEqual(self.random_array, sorted(self.random_array))

    def test_merge_sort_negative_array_k4(self):
        # Testing by sorting a negative array
        merge_sort_plus(self.negative_array, 4)
        self.assertEqual(self.negative_array, sorted(self.negative_array))

    def test_merge_sort_decimal_array_k4(self):
        # Testing by sorting a decimal array
        merge_sort_plus(self.random_decimal_array, 4)
        self.assertEqual(self.random_decimal_array, self.sorted_decimal_array)
        
if __name__ == '__main__':
  # Creating a test suite
  test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(Sorting_Algorithms_Test)
  # Running the tests
  unittest.TextTestRunner().run(test_suite)