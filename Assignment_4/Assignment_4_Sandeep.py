import unittest
import math
from collections import defaultdict

def huffman(text):
    # If the input text is empty, return an empty dictionary
    if not text:
        return {}

    # Handles the case of a single character
    if len(text) == 1:
        return {text[0]: "0"}

    # Calculates the character frequencies
    frequencies = defaultdict(int)
    for char in text:
        frequencies[char] += 1

    # Creates Huffman Tree
    def huffman_tree(frequency_map):
        nodes = [[freq, [char, ""]] for char, freq in frequency_map.items()]

        while len(nodes) > 1:
            # Find the two nodes with the smallest freq.
            min1 = min(nodes, key=lambda x: x[0])
            nodes.remove(min1)
            min2 = min(nodes, key=lambda x: x[0])
            nodes.remove(min2)

            for pair in min1[1:]:
                pair[1] = '0' + pair[1]
            for pair in min2[1:]:
                pair[1] = '1' + pair[1]
            new_node = [min1[0] + min2[0]] + min1[1:] + min2[1:]

            nodes.append(new_node)

        huffman_tree = nodes[0][1:]
        return huffman_tree
    huffman_tree = huffman_tree(frequencies)

    # Create a dictionary of Huffman-encoded characters
    huffman_dict = {char: code for char, code in huffman_tree}

    return huffman_dict

CharNum = 32 # ASCII character set
if CharNum == 32:
    list = "abcdefghijklmnopqrstuvwxyz. ,!?'"
    n = 5
elif CharNum == 64:
    list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ. ,!?'"
    n = 6
elif CharNum == 128:
    # Create a list of valid characters based on CharNum
    list = "".join([chr(i) for i in range(32, 128)])
    n = 7

# ------------------------- Bits Difference function --------------------------------------
# Calculates bits saved
def bits_diff(text):
    huffman_dict = huffman(text)
    huffman_bits = 0
    for char in text:
        if char in huffman_dict:
            huffman_bits += len(huffman_dict[char])

    fixed_length_bits = math.log(CharNum, 2) * len(text)

    bits_saved = fixed_length_bits - huffman_bits

    return bits_saved

# --------------------------- Unit Testing -------------------------------------------------------------
class TestHuffmanEncoding(unittest.TestCase):
    def test_huffman_encoding(self):
        # Test encoding a simple text with known results
        text = "BCCABBDDAECCBBAEDDCC"
        expected_result = {'A': '101', 'B': '01', 'C': '11', 'D': '00', 'E': '100'}
        encoded_dict = huffman(text)
        self.assertEqual(encoded_dict, expected_result)

    def test_huffman_encoding_empty_text(self):
        # Test encoding an empty string
        text = ""
        expected_result = {}
        encoded_dict = huffman(text)
        self.assertEqual(encoded_dict, expected_result)

    def test_huffman_single_letter(self):
        # Test encoding a string with symbols
        text = "x"
        # Expected Huffman dictionary based on character frequencies:
        expected_result = {'x': '0'}
        encoded_dict = huffman(text)
        self.assertEqual(encoded_dict, expected_result)

    def test_huffman_encoding_symbols(self):
        # Test encoding a string with symbols
        text = "!@#$%^&*"
        # Expected Huffman dictionary based on character frequencies:
        expected_result = {'!': '000', '@': '001', '#': '010', '$': '011', '%': '100', '^': '101', '&': '110', '*': '111'}
        encoded_dict = huffman(text)
        self.assertEqual(encoded_dict, expected_result)
    
    def test_bits_diff(self):
        # Test bits_diff function with known values
        huffman_dict = {'a': '11', 'b': '0', 'c': '10'}
        n = math.log(CharNum, 2)
        text = "aaabbbcc"
        if n == 5:
            expected_result = 27 # Fixed-length bits: 5*8=40, Huffman bits: 13
        elif n == 6:
            expected_result = 35 # Fixed-length bits: 6*8=48, Huffman bits: 13
        elif n == 7:
            expected_result = 43 # Fixed-length bits: 7*8=56, Huffman bits: 13
        bits_saved = bits_diff(text)
        self.assertEqual(bits_saved, expected_result)

    def test_bits_diff_empty_text(self):
        # Test bits_diff function with an empty string
        huffman_dict = {}
        n = math.log(CharNum, 2)
        text = ""
        expected_result = 0  # No savings as there's no content to encode
        bits_saved = bits_diff(text)
        self.assertEqual(bits_saved, expected_result)

    def test_bits_diff_large_text(self):
        # Test bits_diff function with a large text
        huffman_dict = {'A': '101', 'B': '01', 'C': '11', 'D': '00', 'E': '100'}
        n = math.log(CharNum, 2)
        text = "BCCABBDDAECCBBAEDDCC"
        if n == 5:
            expected_result = 55 # Fixed-length bits: 5*20=100, Huffman bits: 45
        elif n == 6:
            expected_result = 75 # Fixed-length bits: 6*20=120, Huffman bits: 45
        elif n == 7:
            expected_result = 95  # Fixed-length bits: 7*20=140, Huffman bits: 45
        bits_saved = bits_diff(text)
        self.assertEqual(bits_saved, expected_result)


if __name__ == "__main__":
    # Creating a test suite
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHuffmanEncoding)
    # Running the tests
    unittest.TextTestRunner().run(test_suite)

    # ------------------------------- Example ------------------------------------------------
    file_path = 'gutenberg.txt'  # Path to your text file
    with open(file_path, 'r', encoding='utf-8') as file:  # Read text from the file
            plain_text = file.read()

    text = "".join(char for char in plain_text if char in list)

    encoded_dict = huffman(text)
    # for char, code in encoded_dict.items():
    #     print(f"{char}: {code}")

    huffman_dict = encoded_dict  # Replace with your Huffman dictionary
    saved_bits = bits_diff(text)
    # print(f"Bits saved using Huffman encoding: {saved_bits} bits")