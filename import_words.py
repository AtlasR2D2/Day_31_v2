import pandas as pd

try:
    words_df = pd.read_csv(r".\data\words_to_learn.csv")
except FileNotFoundError:
    words_df = pd.read_csv(r".\data\french_words.csv")
finally:
    languages_list = list(words_df.columns)
    words_list = words_df.to_dict(orient="records")
