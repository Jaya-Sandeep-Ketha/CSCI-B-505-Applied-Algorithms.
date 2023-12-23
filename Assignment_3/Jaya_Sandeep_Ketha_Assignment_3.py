# Submitted by: Jaya Sandeep, Ketha
# Programming Assignment 3
# References:
#               https://leetcode.com/problems/longest-increasing-subsequence/
#               https://interviewbit.com/blog/longest-increasing-subsequence/
#               https://cp-algorithms.com/sequences/longest_increasing_subsequence.html
#               https://takeuforward.org/data-structure/longest-bitonic-subsequence-dp-46/
#               https://www.codingninjas.com/studio/library/longest-bitonic-subsequence

# ------------------------------- Longest Increasing Subsequence ---------------------------------------------------
def LIS(A):
    n = len(A)
    
    # Check for empty input
    if n == 0:
        return 0, []

    # Initialize an array to store the tail elements of active subsequences.
    tail_elements = [0] * n
    tail_elements[0] = A[0]
    
    # Initialize the length of the longest increasing subsequence
    B_length = 1

    # Initialize an array to store the actual LIS.
    B = [[] for _ in range(n)]
    B[0].append(A[0])

    # Iterate through the input array
    for i in range(1, n):
        if A[i] < tail_elements[0]:
            # If the current number is smaller than the smallest tail element, update the smallest tail element and replace the B with the current number.
            tail_elements[0] = A[i]
            B[0] = [A[i]]
        elif A[i] > tail_elements[B_length - 1]:
            # If the current number is larger than the largest tail element, extend the LIS by adding the current number.
            tail_elements[B_length] = A[i]
            B[B_length] = B[B_length - 1][:]  # Copy the B
            B[B_length].append(A[i])
            B_length += 1
        else:
            # Binary search to find the position to insert the current number in the tail_elements array
            left, right = 0, B_length - 1
            while left < right:
                mid = left + (right - left) // 2
                if tail_elements[mid] < A[i]:
                    left = mid + 1
                else:
                    right = mid
            # Update the tail_elements and B arrays accordingly
            tail_elements[left] = A[i]
            B[left] = B[left - 1][:]  # Copy the B
            B[left].append(A[i])

    # Return B itself
    return B[B_length - 1]

# ------------------------------------------------ INC/DEC Function ---------------------------------------------------------
def INC_DEC(A):
    if not A:
        return [], []

    arr_length = len(A)
    inc_subseq_length = [1] * arr_length  # Initialize an array to store the length of the longest increasing subsequence ending at each index
    dec_subseq_length = [1] * arr_length  # Initialize an array to store the length of the longest decreasing subsequence ending at each index
    prev_inc_subseq = [-1] * arr_length  # Initialize an array to store the previous index for the increasing subsequence
    prev_dec_subseq = [-1] * arr_length  # Initialize an array to store the previous index for the decreasing subsequence

    # Compute the length of the longest increasing subsequence ending at each index
    for i in range(1, arr_length):
        for j in range(i):
            if A[i] > A[j] and inc_subseq_length[i] < inc_subseq_length[j] + 1:
                inc_subseq_length[i] = inc_subseq_length[j] + 1
                prev_inc_subseq[i] = j

    # Compute the length of the longest decreasing subsequence ending at each index
    for i in range(arr_length - 2, -1, -1):
        for j in range(arr_length - 1, i, -1):
            if A[i] > A[j] and dec_subseq_length[i] < dec_subseq_length[j] + 1:
                dec_subseq_length[i] = dec_subseq_length[j] + 1
                prev_dec_subseq[i] = j

    max_len = 0
    max_len_idx = -1

    # Find the index with the maximum length of INC/DEC subsequence
    for i in range(arr_length):
        if max_len < inc_subseq_length[i] + dec_subseq_length[i] - 1:
            max_len = inc_subseq_length[i] + dec_subseq_length[i] - 1
            max_len_idx = i

    # Reconstruct the INC/DEC subsequence
    inc_seq = []
    dec_seq = []

    # Reconstruct increasing subsequence
    idx = max_len_idx
    while idx != -1:
        inc_seq.append(A[idx])
        idx = prev_inc_subseq[idx]
    inc_seq = inc_seq[::-1]

    # Reconstruct decreasing subsequence
    idx = max_len_idx
    while idx != -1:
        dec_seq.append(A[idx])
        idx = prev_dec_subseq[idx]
    dec_seq = dec_seq[1:] if len(dec_seq) > 1 else []

    # Combine increasing and decreasing subsequences
    result_seq = inc_seq + dec_seq

    return result_seq

# ----------------------------------------------- Test Cases -------------------------------------------------------
# test cases for the built-in unit test framework
import unittest
class Test(unittest.TestCase):
    def testLis(self):
        self.assertEqual(LIS([1, 5, 6]), [1, 5, 6])
        print("Longest Increasing Subsequence:\n")
        lis = LIS([1, 5, 6])
        print(f"Input Sequence: {[1, 5, 6]}")
        print(f"Output Sequence: {lis}")
        print(f"Length of Sequence: {len(lis)}\n")

        self.assertEqual(LIS([1, 5, 6, 4]), [1, 5, 6])
        lis = LIS([1, 5, 6, 4])
        print(f"Input Sequence: {[1, 5, 6, 4]}")
        print(f"Output Sequence: {lis}")
        print(f"Length of Sequence: {len(lis)}\n")

        self.assertEqual(LIS([1, 5, 6, 2, 3, 4, 7]), [1, 2, 3, 4, 7])
        lis = LIS([1, 5, 6, 2, 3, 4, 7])
        print(f"Input Sequence: {[1, 5, 6, 2, 3, 4, 7]}")
        print(f"Output Sequence: {lis}")
        print(f"Length of Sequence: {len(lis)}\n")

        self.assertIn(LIS([1, 5, 2, 6, 3, 7, 4, 9, 8, 10]), [[1, 5, 6, 7, 9, 10], [1, 2, 3, 4, 8, 10]])
        lis = LIS([1, 5, 2, 6, 3, 7, 4, 9, 8, 10])
        print(f"Input Sequence: {[1, 5, 2, 6, 3, 7, 4, 9, 8, 10]}")
        print(f"Output Sequence: {lis}")
        print(f"Length of Sequence: {len(lis)}\n")

        self.assertIn(LIS([0, 4, 2, 8, 22, 12, 3, 6, 5]), [[0, 2, 3, 5], [0, 2, 8, 22], [0, 2, 8, 12],  [0, 4, 8, 22]] )
        lis = LIS([0, 4, 2, 8, 22, 12, 3, 6, 5])
        print(f"Input Sequence: {[0, 4, 2, 8, 22, 12, 3, 6, 5]}")
        print(f"Output Sequence: {lis}")
        print(f"Length of Sequence: {len(lis)}\n")

    def testDec(self):
        self.assertEqual(INC_DEC([1, 5, 3]), ([1, 5, 3]))
        print("Longest Increasing & Decreasing Subsequence:\n")
        result = INC_DEC([1, 5, 3])
        print(f"Input Sequence: {[1, 5, 3]}")
        print(f"Output Sequence: {result}")
        print(f"Length of Sequence: {len(result)}\n")

        self.assertEqual(INC_DEC([1, 5, 6, 4]), ([1, 5, 6, 4]))
        result = INC_DEC([1, 5, 6, 4])
        print(f"Input Sequence: {[1, 5, 6, 4]}")
        print(f"Output Sequence: {result}")
        print(f"Length of Sequence: {len(result)}\n")

        self.assertEqual(INC_DEC([1, 5, 6, 3, 9, 4, 10, 2]), ([1, 5, 6, 9, 4, 2]))
        result = INC_DEC([1, 5, 6, 3, 9, 4, 10, 2])
        print(f"Input Sequence: {[1, 5, 6, 3, 9, 4, 10, 2]}")
        print(f"Output Sequence: {result}")
        print(f"Length of Sequence: {len(result)}\n")

        self.assertEqual(INC_DEC([1, 100, 200, 300, 80, 77, 70, 40, 30 , 120, 400, 500, 600, 700, 405, 800, 5, 4]), ([1, 100, 200, 300, 80, 77, 70, 40, 30, 5, 4]))
        result = INC_DEC([1, 100, 200, 300, 80, 77, 70, 40, 30 , 120, 400, 500, 600, 700, 405, 800, 5, 4])
        print(f"Input Sequence: {[1, 100, 200, 300, 80, 77, 70, 40, 30 , 120, 400, 500, 600, 700, 405, 800, 5, 4]}")
        print(f"Output Sequence: {result}")
        print(f"Length of Sequence: {len(result)}\n")

if __name__ == '__main__':
    # Creating a test suite
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)
    # Running the tests
    unittest.TextTestRunner().run(test_suite)