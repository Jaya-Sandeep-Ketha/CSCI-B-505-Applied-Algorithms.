import re
from tabulate import tabulate
import unittest
import time

#----------------------------------------------------------------------------------------------------------------------------------------------
class Node:
    def __init__(self, key):
        self.key = key
        self.next = None

class ChainingHashSet:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.word_count = 0  # Track the number of words inserted

    def __len__(self):
        return len(self.table)

    def hash_function(self, key):
        key = key.lower()
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.size

    def add(self, key):
        index = self.hash_function(key)
        node = Node(key)
        # Check if the slot is empty
        if self.table[index] is None:
            self.table[index] = node
            self.word_count += 1
            return True      
        current = self.table[index]
        while current.next is not None:
            if current.key == key:
                return False
            current = current.next   
        if current.key == key:
            return False   
        current.next = node
        self.word_count += 1
        return True

    def contains(self, key):
        index = self.hash_function(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                return True
            current = current.next
        return False

    def stats(self):
        max_chain_length = 0
        used_slots = 0
        for slot in self.table:
            current_length = 0
            current = slot
            while current:
                current_length += 1
                current = current.next
            if current_length > max_chain_length:
                max_chain_length = current_length
            if slot is not None:
                used_slots += 1
        unused_slots = len(self.table) - used_slots
        return max_chain_length, unused_slots

#----------------------------------------------------------------------------------------------------------------------------------------------
class LinearProbingHashSet:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.visited_nodes = 0
        self.words_inserted = 0
        self.total_nodes_visited = 0  # Track total nodes visited during insertions
        self.successful_insertions = 0  # Track the count of successful insertions

    def __len__(self):
        return len(self.table)

    def hash_function(self, key):
        key = key.lower()
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.size

    def add(self, key):
        index = self.hash_function(key)
        initial_index = index
        nodes_visited = 0  # Track nodes visited for this insertion
        while self.table[index] is not None:
            nodes_visited += 1  # Increment nodes visited for each collision
            self.visited_nodes += 1
            index = (index + 1) % self.size
            if index == initial_index:
                return False  # Hash table is full, unable to insert more words
        self.table[index] = key
        self.words_inserted += 1
        self.successful_insertions += 1  # Increment successful insertions
        self.total_nodes_visited += nodes_visited  # Update total nodes visited
        return True

    def contains(self, key):
        index = self.hash_function(key)
        initial_index = index
        while self.table[index] is not None:
            if self.table[index] == key:
                return True
            index = (index + 1) % self.size
            if index == initial_index:
                return False  # Key not found in hash table
        return False  # Key not found in hash table

    def average_nodes_visited_per_insertion(self):
        return self.total_nodes_visited / self.successful_insertions if self.successful_insertions > 0 else 0

    def stats(self):
        used_slots = 0
        for slot in self.table:
            if slot is not None:
                used_slots += 1
        unused_slots = len(self.table) - used_slots
        return None, unused_slots

#----------------------------------------------------------------------------------------------------------------------------------------------
class QuadraticProbingHashSet:
    def __init__(self, size, quadratic_type):
        self.size = size
        self.table = [None] * size
        self.visited_nodes = 0
        self.words_inserted = 0
        self.quadratic_type = quadratic_type
        self.total_nodes_visited = 0  # Track total nodes visited during insertions
        self.successful_insertions = 0  # Track the count of successful insertions

    def __len__(self):
        return len(self.table)

    def hash_function(self, key):
        key = key.lower()
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.size

    def add(self, key):
        index = self.hash_function(key)
        initial_index = index
        i = 1
        nodes_visited = 0  # Track nodes visited for this insertion
        while self.table[index] is not None:
            nodes_visited += 1  # Increment nodes visited for each collision
            self.visited_nodes += 1
            if self.quadratic_type == "half":
                index = (initial_index + (i + i * i) // 2) % self.size
            elif self.quadratic_type == "zero_one":
                index = (initial_index + i * i) % self.size
            i += 1
            if index == initial_index:
                return False  # Hash table is full, unable to insert more words
        self.table[index] = key
        self.words_inserted += 1
        self.successful_insertions += 1  # Increment successful insertions
        self.total_nodes_visited += nodes_visited  # Update total nodes visited
        return True

    def contains(self, key):
        index = self.hash_function(key)
        initial_index = index
        i = 1
        while self.table[index] is not None:
            if self.table[index] == key:
                return True
            if self.quadratic_type == "half":
                index = (initial_index + (i + i * i) // 2) % self.size
            elif self.quadratic_type == "zero_one":
                index = (initial_index + i * i) % self.size
            i += 1
            if index == initial_index:
                return False  # Key not found in hash table
        return False  # Key not found in hash table

    def average_nodes_visited_per_insertion(self):
        return self.total_nodes_visited / self.successful_insertions if self.successful_insertions > 0 else 0

    def stats(self):
        used_slots = 0
        for slot in self.table:
            if slot is not None:
                used_slots += 1
        unused_slots = len(self.table) - used_slots
        return None, unused_slots

#----------------------------------------------------------------------------------------------------------------------------------------------
# Processing text from file
def processing(text, n):
    # Function to preprocess text and extract words
    def preprocess_text(text_list):
        text = ' '.join(text_list)
        text = text.lower()
        words = re.findall(r'\b[a-zA-Z0-9]+\b', text)
        return words

    # Preprocess text and extract words
    words = preprocess_text(text)

    unique_words = []
    seen = set()
    for word in words:
        if word not in seen:
            unique_words.append(word)
            seen.add(word)

    def insert_words(hash_table, n, words):
        words_inserted = set()  # Track words already inserted
        words_count = 0  # Track number of words inserted
        nodes_visited = []  # Track nodes visited for each insertion
        start_time = time.time()  # Record the start time
        for word in words:

            # Check if the word is already inserted
            if word in words_inserted:
                continue

            # Check if it's only chaining (assuming chaining relies on unused slots)
            if hasattr(hash_table, 'hash_type') and hash_table.hash_type == 'Chaining':
                # Check if there are no more empty slots or if time limit is exceeded
                if hash_table.unused_slots() == 0 or time.time() - start_time > 3600:  # 60 minutes = 3600 seconds
                    break

            nodes_before_insert = getattr(hash_table, 'visited_nodes', 0) # Count nodes visited before insertion
            inserted = hash_table.add(word) # Attempt to insert into the hash table
            nodes_after_insert = getattr(hash_table, 'visited_nodes', 0) # Count nodes visited after insertion
            nodes_visited.append(nodes_after_insert - nodes_before_insert) # Calculate nodes visited for this insertion

            # If unable to insert, stop inserting further
            if not inserted:
                break

            # Update tracking variables
            words_inserted.add(word)
            words_count += 1

        max_chain_length, unused_slots = hash_table.stats() if hasattr(hash_table, 'stats') else (0, 0)

    #----------------------------------------------------------------------------------------------------------------------------------------------
    # Create instances of hash tables
    hash_table_chaining = ChainingHashSet(n)
    hash_table_linear = LinearProbingHashSet(n)
    hash_table_quadratic_half = QuadraticProbingHashSet(n, "half")
    hash_table_quadratic_zero_one = QuadraticProbingHashSet(n, "zero_one")
    #----------------------------------------------------------------------------------------------------------------------------------------------
    insert_words(hash_table_chaining, n, words)
    insert_words(hash_table_linear, n, words)
    insert_words(hash_table_quadratic_half, n, words)
    insert_words(hash_table_quadratic_zero_one, n, words)

    def check_insertion_status(hash_table, intended_words, actual_words):
        intended_count = len(intended_words)
        inserted_count = actual_words
        if intended_count != inserted_count:
            max_chain_length, unused_slots = hash_table.stats()
            if unused_slots > 0:
                return "Failed"
        return "Success"
    #----------------------------------------------------------------------------------------------------------------------------------------------
    max_chain_length_chaining, unused_slots_chaining = hash_table_chaining.stats() # Get stats for linear probing
    max_chain_length_linear, unused_slots_linear = hash_table_linear.stats() # Get stats for linear probing
    max_chain_length_quadratic_half, unused_slots_quadratic_half = hash_table_quadratic_half.stats() # Get stats for quadratic probing with c1 = c2 = 1/2
    max_chain_length_quadratic_zero_one, unused_slots_quadratic_zero_one = hash_table_quadratic_zero_one.stats() # Get stats for quadratic probing with c1 = 0, c2 = 1
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Calculate average nodes visited and number of words inserted for each probing method
    avg_nodes_visited_linear = hash_table_linear.average_nodes_visited_per_insertion()
    avg_nodes_visited_quadratic_half = hash_table_quadratic_half.average_nodes_visited_per_insertion()
    avg_nodes_visited_quadratic_zero_one = hash_table_quadratic_zero_one.average_nodes_visited_per_insertion()
    #------------------------------------------------------------------------------------------------------------------------------------------------
    words_inserted_chaining = hash_table_chaining.word_count
    words_inserted_linear = hash_table_linear.words_inserted
    words_inserted_quadratic_half = hash_table_quadratic_half.words_inserted
    words_inserted_quadratic_zero_one = hash_table_quadratic_zero_one.words_inserted
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Check insertion status
    status_chaining = check_insertion_status(hash_table_chaining, unique_words, words_inserted_chaining)
    status_linear = check_insertion_status(hash_table_linear, unique_words, words_inserted_linear)
    status_quadratic_half = check_insertion_status(hash_table_quadratic_half, unique_words, words_inserted_quadratic_half)
    status_quadratic_zero_one = check_insertion_status(hash_table_quadratic_zero_one, unique_words, words_inserted_quadratic_zero_one)

    # Formulate the statistics data in a tabular format
    table_data = [
        ["Probing Method", "Max Chain Length", "Unused Slots", "Avg Nodes Visited", "Words Inserted", "Insertion Status"],
        ["Chaining", max_chain_length_chaining, unused_slots_chaining, 'NA', words_inserted_chaining, status_chaining],
        ["Linear Probing", max_chain_length_linear, unused_slots_linear, avg_nodes_visited_linear, words_inserted_linear,status_linear],
        ["Quadratic Probing (c1=c2=1/2)", max_chain_length_quadratic_half, unused_slots_quadratic_half, avg_nodes_visited_quadratic_half, words_inserted_quadratic_half, status_quadratic_half],
        ["Quadratic Probing (c1=0, c2=1)", max_chain_length_quadratic_zero_one, unused_slots_quadratic_zero_one, avg_nodes_visited_quadratic_zero_one, words_inserted_quadratic_zero_one, status_quadratic_zero_one]   
    ]

    return table_data


# Unit Tests
class TestHashTableOperations(unittest.TestCase):
    def setUp(self):
        self.hash_table_chaining = ChainingHashSet(10)
        self.hash_table_linear = LinearProbingHashSet(10)
        self.hash_table_quadratic_half = QuadraticProbingHashSet(n, "half")
        self.hash_table_quadratic_zero = QuadraticProbingHashSet(n, "zero_one")
        self.words = ["apple", "banana", "orange", "grape", "watermelon"]

        for word in self.words:
            self.hash_table_chaining.add(word)
            self.hash_table_linear.add(word)
            self.hash_table_quadratic_half.add(word)
            self.hash_table_quadratic_zero.add(word)

    # Testcase to check existing key logic
    def test_contains_existing_key(self):
        for word in self.words:
            self.assertTrue(self.hash_table_chaining.contains(word))
            self.assertTrue(self.hash_table_linear.contains(word))
            self.assertTrue(self.hash_table_quadratic_half.contains(word))
            self.assertTrue(self.hash_table_quadratic_zero.contains(word))
    
    # Testcase to check contains logic
    def test_contains_non_existing_key(self):
        self.assertFalse(self.hash_table_chaining.contains("pineapple"))
        self.assertFalse(self.hash_table_linear.contains("pineapple"))
        self.assertFalse(self.hash_table_quadratic_half.contains("pineapple"))
        self.assertFalse(self.hash_table_quadratic_zero.contains("pineapple"))

    # Text to check chaining, linear probing and quadratic probing logic
    text = ['Sandeep', 'Applied Algorithms', 'Elements of Artificial Intelligence', 'Applied Machine learning', 'Good', 'Grades', 'happy', 'Virat', 'robo', 'sandeer']
    
    # Testcase to check chaining logic
    def test_chaining(self):
        result = processing(self.text, 14)

        # Extract metrics for chaining from the result dictionary
        max_chain_length_chaining = [row[1] for row in result if row[0] == "Chaining"][0]
        unused_slots_chaining = [row[2] for row in result if row[0] == "Chaining"][0]
        avg_nodes_chaining = [row[3] for row in result if row[0] == "Chaining"][0]
        words_inserted_chaining = [row[4] for row in result if row[0] == "Chaining"][0]

        expected_max_chain_length = 3 
        expected_unused_slots = 5  
        expected_avg_nodes = 'NA'
        expected_words_inserted = 15  

        # Check if the output metrics match the expected values for chaining
        self.assertEqual(max_chain_length_chaining, expected_max_chain_length)
        self.assertEqual(unused_slots_chaining, expected_unused_slots)
        self.assertEqual(avg_nodes_chaining, expected_avg_nodes)
        self.assertEqual(words_inserted_chaining, expected_words_inserted)
    
    # Testcase to check linear probing logic
    def test_linear_probing(self):
        result = processing(self.text, 14)

        # Extract metrics for chaining from the result dictionary
        max_chain_length_linear = [row[1] for row in result if row[0] == "Linear Probing"][0]
        unused_slots_linear = [row[2] for row in result if row[0] == "Linear Probing"][0]
        avg_nodes_linear = round([row[3] for row in result if row[0] == "Linear Probing"][0], 2)
        words_inserted_linear = [row[4] for row in result if row[0] == "Linear Probing"][0]

        expected_max_chain_length = None 
        expected_unused_slots = 0  
        expected_avg_nodes = 1.07
        expected_words_inserted = 14  

        # Check if the output metrics match the expected values for chaining
        self.assertEqual(max_chain_length_linear, expected_max_chain_length)
        self.assertEqual(unused_slots_linear, expected_unused_slots)
        self.assertEqual(avg_nodes_linear, expected_avg_nodes)
        self.assertEqual(words_inserted_linear, expected_words_inserted)
   
    # Testcase to check quadratic probing with c1=c2=1/2 logic
    def test_quadratic_probing_half(self):
        result = processing(self.text, 14)
        
        # Extract metrics for chaining from the result dictionary
        max_chain_length_quadratic_half = [row[1] for row in result if row[0] == "Quadratic Probing (c1=c2=1/2)"][0]
        unused_slots_quadratic_half = [row[2] for row in result if row[0] == "Quadratic Probing (c1=c2=1/2)"][0]
        avg_nodes_quadratic_half = round([row[3] for row in result if row[0] == "Quadratic Probing (c1=c2=1/2)"][0], 2)
        words_inserted_quadratic_half = [row[4] for row in result if row[0] == "Quadratic Probing (c1=c2=1/2)"][0]

        expected_max_chain_length = None 
        expected_unused_slots = 2  
        expected_avg_nodes = 0.58
        expected_words_inserted = 12  

        # Check if the output metrics match the expected values for chaining
        self.assertEqual(max_chain_length_quadratic_half, expected_max_chain_length)
        self.assertEqual(unused_slots_quadratic_half, expected_unused_slots)
        self.assertEqual(avg_nodes_quadratic_half, expected_avg_nodes)
        self.assertEqual(words_inserted_quadratic_half, expected_words_inserted)
    
    # Testcase to check quadratic probing with c1=0, c2=1 logic
    def test_quadratic_probing_zero(self):
        result = processing(self.text, 14)

        # Extract metrics for chaining from the result dictionary
        max_chain_length_quadratic_zero = [row[1] for row in result if row[0] == "Quadratic Probing (c1=0, c2=1)"][0]
        unused_slots_quadratic_zero = [row[2] for row in result if row[0] == "Quadratic Probing (c1=0, c2=1)"][0]
        avg_nodes_quadratic_zero = round([row[3] for row in result if row[0] == "Quadratic Probing (c1=0, c2=1)"][0], 2)
        words_inserted_quadratic_zero = [row[4] for row in result if row[0] == "Quadratic Probing (c1=0, c2=1)"][0]

        expected_max_chain_length = None 
        expected_unused_slots = 3  
        expected_avg_nodes = 0.73
        expected_words_inserted = 11  

        # Check if the output metrics match the expected values for chaining
        self.assertEqual(max_chain_length_quadratic_zero, expected_max_chain_length)
        self.assertEqual(unused_slots_quadratic_zero, expected_unused_slots)
        self.assertEqual(avg_nodes_quadratic_zero, expected_avg_nodes)
        self.assertEqual(words_inserted_quadratic_zero, expected_words_inserted)

if __name__ == '__main__':
    n = 1024  # Change to the desired number of words to insert for each method

    # a = 'Frog_Prince.txt'  # Replace 'Combined_Tales.txt' with your combined tales file name
    # with open(a, 'r') as file:
    #     text = file.read().split()
    # # Send the file content for preprocessing
    # result = processing(text, n)
    # # Display the statistics in a table
    # print('Frog Prince')
    # print(tabulate(result, headers="firstrow", tablefmt="grid"))

    # print('\n')

    # b = 'Combined_Tales.txt'  # Replace 'Combined_Tales.txt' with your combined tales file name
    # with open(b, 'r') as file:
    #     text = file.read().split()
    # # Send the file content for preprocessing
    # result = processing(text, n)
    # print('Combined Tales')
    # print(tabulate(result, headers="firstrow", tablefmt="grid"))

  # Creating a test suite
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHashTableOperations)
  # Running the tests
    unittest.TextTestRunner().run(test_suite)
