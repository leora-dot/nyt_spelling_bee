#Import Libraries
from marisa_trie import Trie
from queue import Queue

class Solver():

    def __init__(self, input_file, min_letters):

        self.candidates = Queue()
        self.solutions = []

        #Generate word list From file
        word_list = []

        with open(input_file, "r") as file:
            for line in file:
                stripped_line = line.strip().upper()

                if len(stripped_line) >= min_letters:
                    word_list.append(stripped_line)

        #Generate trie from word list
        self.trie = Trie(word_list)

    def generate_solutions(self, letter_list, center_letter):
        center_letter = center_letter.upper()
        letter_list = [letter.upper() for letter in letter_list]

        self.generate_candidates(letter_list)

        while not self.candidates.empty():
            candidate_current = self.candidates.get()

            if self.trie.keys(candidate_current): #if word or prefix
                if candidate_current in self.trie: #if word
                    if center_letter in candidate_current:
                        self.solutions.append(candidate_current)

                self.generate_candidates(letter_list, candidate_current)

            self.candidates.task_done()

    def return_solutions(self):
        self.solutions.sort()
        print(self.solutions)

    def generate_candidates(self, letter_list, root_string = ""):

        for letter in letter_list:
            self.candidates.put(root_string + letter)

