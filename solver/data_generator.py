#import libraries
import itertools
import pandas as pd
from queue import Queue
from csv import DictWriter

#import modules
from validator import Validator
from solver import Solver

class DataGenerator():

    def __init__(self, output_file, profanity_input_file, solver):

        self.solver = solver
        self.output_file = output_file
        self.profanity_input_file = profanity_input_file
        self.data_unlogged = Queue()
        self.max_combinations = 3
        self.combinations_counter = 0

        self.letter_combinations = itertools.combinations("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 7)
        self.is_combination_current = False

        self.combination = None
        self.combination_string = None

    def get_completed_dict(self):
        completed_combinations = pd.read_csv(self.output_file, usecols=["SEVEN_LETTERS"])
        completed_combinations = completed_combinations["SEVEN_LETTERS"].unique()
        self.logged_dict = {combination:True for combination in completed_combinations}

    def is_combination_in_log(self):

        if self.logged_dict.get(self.combination_string, False):
            return True
        else:
            self.is_combination_current = True
            return False

    def generate_combination_data(self):

        for center_letter in self.combination:
            output_dict = {}
            validator = Validator(self.solver, self.combination, center_letter, self.profanity_input_file)

            output_dict["SEVEN_LETTERS"] = self.combination_string
            output_dict["CENTER_LETTER"] = center_letter
            output_dict["NUM_SOLUTIONS"] = validator.num_solutions()
            output_dict["IS_PROFANE"] = validator.is_profane()
            output_dict["IS_PANGRAM"] = validator.is_pangram()

            self.data_unlogged.put(output_dict)

        self.combinations_counter +=1

    def log_data(self):

        with open(self.output_file, 'a', newline='') as file:
            dictwriter_object = DictWriter(file, fieldnames= ["SEVEN_LETTERS", "CENTER_LETTER", "NUM_SOLUTIONS", "IS_PROFANE", "IS_PANGRAM"])

            while not self.data_unlogged.empty():
                data = self.data_unlogged.get()
                dictwriter_object.writerow(data)

            file.close()

    def run(self):

        self.get_completed_dict()

        for combination in self.letter_combinations:
            self.combination = combination
            self.combination_string = "".join(letter for letter in self.combination)

            if self.is_combination_current:
                self.generate_combination_data()
            elif not self.is_combination_in_log():
                self.generate_combination_data()

            if self.combinations_counter >= self.max_combinations:
                self.log_data()
