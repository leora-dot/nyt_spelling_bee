#Import libraries
import numpy as np
import pandas as pd
import sys

#Import modules
sys.path.append("..")
from helper_functions import alphabet_string

#
#Load & Clean Data
#

df = pd.read_csv("../data_generation/solution_data.csv", usecols=["SEVEN_LETTERS", "CENTER_LETTER", "NUM_SOLUTIONS", "IS_PROFANE", "IS_PANGRAM"])
df.drop_duplicates(inplace = True)

bool_cols = ["IS_PROFANE", "IS_PANGRAM"]
for col in bool_cols:
    df[col] = df[col].astype(int)

#
#Select Valid Data
#

df_valid = df.copy()
df_valid = df_valid[df_valid["IS_PROFANE"] == 0]
df_valid = df_valid[df_valid["IS_PANGRAM"] == 1]

df_valid.drop(columns = bool_cols, inplace = True)
df_valid.reset_index(inplace = True, drop = True)

df_features = df_valid.copy()

#
#Create Letter Features
#

for letter in alphabet_string:
    df_features["IS_LETTER_" + letter] = df_features["SEVEN_LETTERS"].apply(lambda x: letter in x).astype(int)
    df_features["IS_LETTER_CENTER_" + letter] = df_features["CENTER_LETTER"].apply(lambda x: letter in x).astype(int)
