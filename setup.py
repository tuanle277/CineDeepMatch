import json
import pandas as pd
import numpy as np
import random
import time
from constants import *

df = pd.read_csv(DATA_PATH + USER_MOVIE_PATH)
df.dropna(inplace=True)  # Drop rows with NaN
tmdb_credit_df = pd.read_csv(DATA_PATH + TMDB_PATH+TMDB_CREDIT_PATH)
tmdb_movies_df = pd.read_csv(DATA_PATH + TMDB_PATH + TMDB_MOVIE_PATH)

id_genres = pd.read_csv(DATA_PATH + ENCODING_PATH + ID_GENRE_PATH).dropna(inplace=False)
id_chac = pd.read_csv(DATA_PATH + ENCODING_PATH + ID_CHAR_PATH).dropna(inplace=False)
id_crew = pd.read_csv(DATA_PATH + ENCODING_PATH + ID_CREW_PATH).dropna(inplace=False)
id_cast = pd.read_csv(DATA_PATH + ENCODING_PATH + ID_CAST_PATH).dropna(inplace=False)

"""# Content-based recommendation system

A combination of the two, meaning have a hierarchy approach in calculating similarities between movies:

1. Hierachy matching, meaning match genre first, then rating.

2. grade how similar each pair of movie is using simple percentage of similarity

dataset used: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

## User preference forming
"""

