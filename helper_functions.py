#import libraries
import numpy as np

#Lists
alphabet_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Functions

def file_to_word_list(input_file, min_letters = 0):

    word_list = []

    with open(input_file, "r") as file:
        for line in file:
            stripped_line = line.strip().upper()

            if len(stripped_line) >= min_letters:
                word_list.append(stripped_line)

        word_list = remove_duplicates(word_list)

    return word_list

def remove_duplicates(input_list):
    unique_arr = np.unique(np.array(input_list))
    return list(unique_arr)

def filter_list(main_list, remove_list):
    return list(np.setdiff1d(main_list, remove_list))

def clean_word_list(word_list):
    base_word_list = [word.upper() for word in word_list]

    #Exclusion Lists
    exclusion_list = []
    for exclusion_file in ["profanity_dictionary.txt", "scrabble_acceptable_place_names.txt", "scrabble_monetary_units.txt", "scrabble_proper_names.txt", "scrabble_words_that_surprised_you.txt", "scrabble_words_without_vowels.txt"]:
        exclusion_file = "dictionary_data/" + exclusion_file
        exclusion_file_word_list = file_to_word_list(exclusion_file)
        exclusion_list.extend(exclusion_file_word_list)
    exclusion_list = remove_duplicates(exclusion_list)

    acceptable_list = file_to_word_list("dictionary_data/acceptable_words.txt")
    exclusion_list  = filter_list(exclusion_list, acceptable_list)

    base_word_list = filter_list(base_word_list, exclusion_list)

    return base_word_list

#test = ["Leora", "anna", "reading", "story"]
#print(clean_word_list(test))
#test =["Leora", "Leora", "Yale", "Orange"]
#print(remove_duplicates(test))
