#Import Libraries
from marisa_trie import Trie
from queue import Queue
import sys

#import modules
sys.path.append("..")
from helper_functions import file_to_word_list
from helper_functions import clean_word_list

class Solver():

    def __init__(self, dictionary_input_file, min_letters):

        self.candidates = Queue()
        word_list = file_to_word_list(dictionary_input_file, min_letters)
        word_list = clean_word_list(word_list)

        #Generate trie from word list
        self.trie = Trie(word_list)

    def generate_solutions(self, letter_list, center_letter):
        center_letter = center_letter.upper()
        letter_list = [letter.upper() for letter in letter_list]

        self.solutions = []
        self.generate_candidates(letter_list)

        while not self.candidates.empty():
            candidate = self.candidates.get()

            if self.trie.keys(candidate): #if word or prefix
                if candidate in self.trie: #if word
                    if center_letter in candidate:
                        self.solutions.append(candidate)

                self.generate_candidates(letter_list, candidate)

            self.candidates.task_done()

        self.solutions.sort()
        return self.solutions

    def generate_candidates(self, letter_list, root_string = ""):

        for letter in letter_list:
            self.candidates.put(root_string + letter)
