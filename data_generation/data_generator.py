#import libraries
import itertools
import pandas as pd
import numpy as np
import queue
from csv import DictWriter
import time
from datetime import datetime
import threading

#import modules
from validator import Validator
from solver import Solver

class DataGenerator():

    def __init__(self, output_file, profanity_input_file, solver):

        self.solver = solver
        self.output_file = output_file
        self.profanity_input_file = profanity_input_file
        self.data_unlogged = queue.Queue()

        self.is_data_generation_active = True
        self.is_data_logging_active = True
        self.is_active = True

        self.combination_index = None
        self.combination = None
        self.combination_string = None

        self.num_combinations_total = 657800 #26 choose 7
        self.progress_interval = 1 #time between progress loops in minutes
        self.block_time = 5 #time for blocking in seconds

    def check_log(self):

        print("Checking existing data log...")

        logged_keys = pd.read_csv(self.output_file, usecols=["COMBO_INDEX"])
        logged_max = logged_keys.max()["COMBO_INDEX"]
        if np.isnan(logged_max):
            logged_max = 0
        self.last_logged_index = logged_max

        self.print_progress()

    def generate_iterators(self):

        combinations = itertools.combinations("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 7)
        combination_keys = itertools.count()
        combinations_and_keys = zip(combination_keys, combinations)

        start_index = self.last_logged_index
        self.combinations_outstanding = itertools.islice(combinations_and_keys, start_index, self.num_combinations_total + 1)

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

    def generate_file_objects(self):

        self.file = open(self.output_file, 'a', newline='')
        self.dictwriter_object = DictWriter(self.file, fieldnames= ["COMBO_INDEX", "SEVEN_LETTERS", "CENTER_LETTER", "NUM_SOLUTIONS", "IS_PROFANE", "IS_PANGRAM"])

    def log_data_loop(self):

        write_counter = 0
        counter_max = 500

        self.generate_file_objects()

        while self.is_data_logging_active:

            try:
                data = self.data_unlogged.get(block = False)
                self.dictwriter_object.writerow(data)
                self.last_logged_index = data.get("COMBO_INDEX")
                self.data_unlogged.task_done()
                write_counter +=1

                if write_counter == counter_max:
                    self.file.close()
                    self.generate_file_objects()
                    write_counter = 0

            except queue.Empty:

                if self.is_data_generation_active:
                    time.sleep(self.block_time)

                else:
                    self.file.close()
                    self.is_data_logging_active = False
                    self.print_progress()

    def print_progress(self):

        now = datetime.now()
        now_string = now.strftime("%m/%d/%Y %H:%M:%S")
        print("{:,} / {:,} combinations logged ({:.2%} complete) at {}".format(self.last_logged_index, self.num_combinations_total, self.last_logged_index/self.num_combinations_total, now_string))

    def print_progress_loop(self):

        sleep_time = self.progress_interval * 60

        while self.is_active:
            self.print_progress()
            time.sleep(sleep_time)

    def generate_data_loop(self):

        while self.is_data_generation_active:
            tup = next(self.combinations_outstanding, None)

            if tup is None:
                self.is_data_generation_active = False

            else:
                self.combination_index, self.combination = tup[0], tup[1]
                self.combination_string = "".join(letter for letter in self.combination)
                self.generate_combination_data()

    def run(self):

        self.check_log()
        self.generate_iterators()

        print("Generating new data...")

        for method in [self.generate_data_loop, self.print_progress_loop, self.log_data_loop]:
            thread = threading.Thread(target = method, daemon = True)
            thread.start()

        #BLOCKING
        while self.is_active:
            if (not self.is_data_generation_active) and (not self.is_data_logging_active):
                self.is_active = False
            time.sleep(self.block_time)

        print("Data generation complete.")
