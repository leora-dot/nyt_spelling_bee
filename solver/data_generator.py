#import libraries
import itertools
import pandas as pd
import numpy as np
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

        self.combination_index = None
        self.combination = None
        self.combination_string = None

    def get_progress(self):
        logged_keys = pd.read_csv(self.output_file, usecols=["COMBO_INDEX"])
        logged_max = logged_keys.max()["COMBO_INDEX"]
        if np.isnan(logged_max):
            logged_max = 0
        self.logged_max = logged_max

    def generate_iterators(self):

        combinations = itertools.combinations("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 7)
        combination_keys = itertools.count()
        combinations_and_keys = zip(combination_keys, combinations)

        start_index = self.logged_max
        self.combinations_outstanding = itertools.islice(combinations_and_keys, start_index, None)

    def generate_combination_data(self):

        for center_letter in self.combination:
            output_dict = {}
            validator = Validator(self.solver, self.combination, center_letter, self.profanity_input_file)

            output_dict["COMBO_INDEX"] = self.combination_index
            output_dict["SEVEN_LETTERS"] = self.combination_string
            output_dict["CENTER_LETTER"] = center_letter
            output_dict["NUM_SOLUTIONS"] = validator.num_solutions()
            output_dict["IS_PROFANE"] = validator.is_profane()
            output_dict["IS_PANGRAM"] = validator.is_pangram()

            self.data_unlogged.put(output_dict)

        self.combinations_counter +=1

    def log_data(self):

        with open(self.output_file, 'a', newline='') as file:
            dictwriter_object = DictWriter(file, fieldnames= ["COMBO_INDEX", "SEVEN_LETTERS", "CENTER_LETTER", "NUM_SOLUTIONS", "IS_PROFANE", "IS_PANGRAM"])

            while not self.data_unlogged.empty():
                data = self.data_unlogged.get()
                dictwriter_object.writerow(data)

            file.close()

    def run(self):

        self.get_progress()
        self.generate_iterators()

        for tup in self.combinations_outstanding:
            self.combination_index, self.combination = tup[0], tup[1]
            self.combination_string = "".join(letter for letter in self.combination)

            self.generate_combination_data()

            if self.combinations_counter >= self.max_unlogged_combinations:
                self.log_data()
