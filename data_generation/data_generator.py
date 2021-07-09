#import libraries
import itertools
import pandas as pd
import numpy as np
import queue
from csv import DictWriter
import time
from datetime import datetime
import threading
import sys

#import modules
sys.path.append("..")
from validator import Validator
from solver import Solver
from helper_functions import alphabet_string

class DataGenerator():

    def __init__(self, output_file):

        self.output_file = output_file

        self.to_generate = queue.Queue() #Task IDs
        self.to_process = queue.Queue() #Unprocessed Data
        self.to_log = queue.Queue() #Unlogged data

        self.is_generation_active = True
        self.is_processing_active = True
        self.is_logging_active = True
        self.is_active = True

        self.progress_interval = 1 #time between progress loops in minutes
        self.block_time = 5 #time for blocking in seconds

    def check_log(self):

        print("Checking existing data log...")

        logged_keys = pd.read_csv(self.output_file, usecols=[self.output_column_index_name], squeeze = True)
        logged_max = logged_keys.max()

        if np.isnan(logged_max):
            logged_max = 0
        self.index_last_logged = logged_max

    def generate_tasks(self):

        for task_index in range(self.index_last_logged, self.index_last):
            self.to_generate.put(task_index)

    def generate_data_loop(self):

        while not self.to_generate.empty():
            task_index = self.to_generate.get()
            self.generate_data(task_index)
            self.to_generate.task_done()

        self.is_generation_active = False

    def process_data_loop(self):

        while self.is_processing_active:
            try:
                data = self.to_process.get(block = False)
                self.process_data(data)
                self.to_process.task_done()
            except queue.Empty:
                if self.is_generation_active:
                    time.sleep(self.block_time)
                else:
                    self.is_processing_active = False

    def generate_file_objects(self):

        self.file = open(self.output_file, 'a', newline='')
        self.dictwriter_object = DictWriter(self.file, fieldnames= self.output_column_names)

    def log_data_loop(self):

        write_counter = 0
        counter_max = 500

        self.generate_file_objects()

        while self.is_logging_active:

            try:
                output_dict = self.to_log.get(block = False)
                self.dictwriter_object.writerow(output_dict)
                self.index_last_logged = output_dict.get(self.output_column_index_name)
                self.to_log.task_done()
                write_counter +=1

                if write_counter == counter_max:
                    self.file.close()
                    self.generate_file_objects()
                    write_counter = 0

            except queue.Empty:

                if self.is_generation_active:
                    time.sleep(self.block_time)

                else:
                    self.file.close()
                    self.is_logging_active = False
                    self.print_progress()

    def print_progress(self):

        now = datetime.now()
        now_string = now.strftime("%m/%d/%Y %H:%M:%S")
        print("{:,} / {:,} combinations logged ({:.2%} complete) at {}".format(self.index_last_logged, self.index_last, self.index_last_logged/self.index_last, now_string))

    def print_progress_loop(self):

        sleep_time = self.progress_interval * 60

        while self.is_active:
            self.print_progress()
            time.sleep(sleep_time)

    def run(self):

        self.check_log()
        self.print_progress()
        self.generate_tasks()

        print("Generating new data...")

        for method in [self.generate_data_loop, self.process_data_loop, self.log_data_loop, self.print_progress_loop]:
            thread = threading.Thread(target = method, daemon = True)
            thread.start()

        #BLOCKING
        while self.is_active:
            if not self.is_logging_active:
                self.is_active = False
            time.sleep(self.block_time)

        print("Data generation complete.")

class GameDataGenerator(DataGenerator):

    def __init__(self, output_file, profanity_input_file, solver):
        super().__init__(output_file)

        self.solver = solver
        self.index_last = 657800 #26 choose 7
        self.profanity_input_file = profanity_input_file
        self.output_column_names = ["COMBINATION_INDEX", "SEVEN_LETTERS", "CENTER_LETTER", "NUM_SOLUTIONS", "IS_PROFANE", "IS_PANGRAM"]
        self.output_column_index_name = "COMBINATION_INDEX"

        self.task_name = "combinations"

    def generate_data(self, task_index): #INDEX > VALIDATOR TUPS
        combinations = itertools.combinations(alphabet_string, 7)
        combination = next(itertools.islice(combinations, task_index, task_index + 1))
        combination_string = "".join(letter for letter in combination)

        for center_letter in combination:
            validator = Validator(self.solver, combination, center_letter, self.profanity_input_file)
            raw_data_tup = (task_index, combination_string, center_letter, validator)
            self.to_process.put(raw_data_tup)

    def process_data(self, raw_data_tup): #VALIDATOR TUP > OUTPUTDICT

        task_index = raw_data_tup[0]
        combination_string, center_letter = raw_data_tup[1], raw_data_tup[2]
        validator = raw_data_tup[3]
        output_dict = {}

        output_dict["COMBINATION_INDEX"] = task_index
        output_dict["SEVEN_LETTERS"] = combination_string
        output_dict["CENTER_LETTER"] = center_letter
        output_dict["NUM_SOLUTIONS"] = validator.num_solutions()
        output_dict["IS_PROFANE"] = validator.is_profane()
        output_dict["IS_PANGRAM"] = validator.is_pangram()

        self.to_log.put(output_dict)

if __name__ == "__main__":
    solver = Solver("dictionary_data/wordswithfriends_dictionary.txt", 4)
    game_generator = GameDataGenerator("solution_data.csv", "dictionary_data/profanity_dictionary.txt", solver)
    game_generator.run()
