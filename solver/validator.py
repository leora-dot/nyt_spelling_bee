#import modules
from solver import Solver
from helper_functions import file_to_word_list

class Validator():

    def __init__(self, solver, letter_list, center_letter, profanity_input_file):

        self.letter_list = [letter.upper() for letter in letter_list]
        center_letter = center_letter.upper()
        self.profanity_input_file = profanity_input_file

        self.solver = solver
        self.solutions = self.solver.generate_solutions(self.letter_list, center_letter)

    def num_solutions(self):

        return len(self.solutions)

    def is_profane(self):

        profanity_list = file_to_word_list(self.profanity_input_file)

        for word in profanity_list:
            profanity_letters = list(set(word))
            if all(letter in self.letter_list for letter in profanity_letters):
                return True

        return False

    def is_pangram(self):

        for solution in self.solutions:
            if len(set(solution)) == 7:
                return True

        return False

