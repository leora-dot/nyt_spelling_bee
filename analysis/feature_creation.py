#Import libraries
import numpy as np
import pandas as pd
import sys

#Import modules
sys.path.append("..")
from helper_functions import alphabet_string
from helper_functions import vowel_string

#
#Define Constants
#

is_letter_vowel_columns = ["IS_LETTER_{}".format(letter) for letter in vowel_string]
is_letter_center_vowel_columns = ["IS_LETTER_CENTER_{}".format(letter) for letter in vowel_string]

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

#
#Create Vowel Features
#

df_features["NUM_VOWELS"] = df_features[is_letter_vowel_columns].sum(axis = 1)
df_features["IS_LETTER_CENTER_VOWEL"] = (df_features[is_letter_center_vowel_columns].sum(axis = 1) > 0).astype(int)


#
#Create Prefix & Suffix Features
#

#Two Letters

df_features["IS_AL"] = df_features[["IS_LETTER_A", "IS_LETTER_L"]].all(axis = 1).astype(int)
df_features["IS_ED"] = df_features[["IS_LETTER_E", "IS_LETTER_D"]].all(axis = 1).astype(int)
df_features["IS_ES"] = df_features[["IS_LETTER_E", "IS_LETTER_S"]].all(axis = 1).astype(int)
df_features["IS_IN"] = df_features[["IS_LETTER_I", "IS_LETTER_N"]].all(axis = 1).astype(int)
df_features["IS_UN"] = df_features[["IS_LETTER_U", "IS_LETTER_N"]].all(axis = 1).astype(int)
df_features["IS_RE"] = df_features[["IS_LETTER_R", "IS_LETTER_E"]].all(axis = 1).astype(int)
df_features["IS_LY"] = df_features[["IS_LETTER_L", "IS_LETTER_Y"]].all(axis = 1).astype(int)
df_features["IS_OR"] = df_features[["IS_LETTER_O", "IS_LETTER_R"]].all(axis = 1).astype(int)
df_features["IS_IM"] = df_features[["IS_LETTER_I", "IS_LETTER_M"]].all(axis = 1).astype(int)

#Three Letters
df_features["IS_PRE"] = df_features[["IS_LETTER_P", "IS_LETTER_R", "IS_LETTER_E"]].all(axis = 1).astype(int)
df_features["IS_ING"] = df_features[["IS_LETTER_I", "IS_LETTER_N", "IS_LETTER_G"]].all(axis = 1).astype(int)
df_features["IS_IAL"] = df_features[["IS_LETTER_I", "IS_LETTER_A", "IS_LETTER_L"]].all(axis = 1).astype(int)
df_features["IS_DIS"] = df_features[["IS_LETTER_D", "IS_LETTER_I", "IS_LETTER_S"]].all(axis = 1).astype(int)
df_features["IS_DIF"] = df_features[["IS_LETTER_D", "IS_LETTER_I", "IS_LETTER_F"]].all(axis = 1).astype(int)
df_features["IS_IST"] = df_features[["IS_LETTER_I", "IS_LETTER_S", "IS_LETTER_T"]].all(axis = 1).astype(int)
df_features["IS_EST"] = df_features[["IS_LETTER_E", "IS_LETTER_S", "IS_LETTER_T"]].all(axis = 1).astype(int)

#Four Letters
df_features["IS_ABLE"] = df_features[["IS_LETTER_A", "IS_LETTER_B", "IS_LETTER_L", "IS_LETTER_E"]].all(axis = 1).astype(int)
df_features["IS_IBLE"] = df_features[["IS_LETTER_I", "IS_LETTER_B", "IS_LETTER_L", "IS_LETTER_E"]].all(axis = 1).astype(int)
df_features["IS_TION"] = df_features[["IS_LETTER_T", "IS_LETTER_I", "IS_LETTER_O", "IS_LETTER_N"]].all(axis = 1).astype(int)
df_features["IS_SION"] = df_features[["IS_LETTER_S", "IS_LETTER_I", "IS_LETTER_O", "IS_LETTER_N"]].all(axis = 1).astype(int)
