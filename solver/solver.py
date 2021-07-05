#Import Libraries
import itertools
from queue import Queue

class EnglishDict():

    def __init__(self, input_file, min_letters = 0):
        self.min_letters = min_letters
        self.words = {}

        print("Generating Dictionary...")

        with open(input_file, "r") as file:
            for line in file:
                stripped_line = line.strip()

                if len(stripped_line) >= min_letters:
                    self.words[stripped_line] = True

        print("Dictionary Generated.")

    def is_word(self, input_word):
        is_word = self.words.get(input_word, False)
        return is_word

class Solver():

    def __init__(self, letter_center, letter1, letter2, letter3, letter4, letter5, letter6):
        self.letter_center = letter_center
        self.letter_list = [letter_center, letter1, letter2, letter3, letter4, letter5, letter6]
        self.letter_list.sort()

        self.is_profanity = False
        self.max_letters = 7

        self.english_dictionary = EnglishDict("wordswithfriends_dictionary.txt", 4)

        self.words_unchecked = Queue()
        self.words_solution = []

    def generate_combinations(self):

        self.combinations_list = []

        for i in range(4, self.max_letters + 1):
            self.combinations_list.append(itertools.product(self.letter_list, repeat = i))

    def generate_words_unchecked(self):

        for iterator in self.combinations_list:
            for combination in iterator:
                if self.letter_center in combination:
                    word = "".join(combination)
                    self.words_unchecked.put(word)

    def check_words(self):

        print("Checking Words...")

        while not self.words_unchecked.empty():
            word = self.words_unchecked.get()
            if self.english_dictionary.is_word(word):
                self.words_solution.append(word)
            self.words_unchecked.task_done()

        print(self.words_solution)
