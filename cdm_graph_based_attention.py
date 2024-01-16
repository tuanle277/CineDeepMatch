from utils import *

hierarchy = {'genres': 5,
             'character': 4,
             'cast': 4,
             'rating': 4,
             'crew': 3,
             'popularity': 2,
             'male_rate': 1,
             'original_language': 2
} # the importance score for each attribute

features = list(hierarchy.keys())
interest_features = {1 if df.iloc[x]["runtime"] == 0 or df.iloc[x]["InteractionDuration"] == 0 else df.iloc[x]["InteractionDuration"] / df.iloc[x]["runtime"]: df.iloc[x][features] for x in range(len(df) // 100)}


def build_user_preference(user_interaction_df):
  features = list(user_interaction_df.keys())
  duration_features = {user_interaction_df.iloc[x]["InteractionDuration"]: user_interaction_df.iloc[x][features] for x in range(len(user_interaction_df)//100)}

  user_preference = {}
  for feature in features:
    if feature in ["cast", "character", "crew", "genres"]:
      top_k = 10
      user_preference[feature] = get_top_k(duration_features, feature, top_k)

    elif feature in ["popularity", "rating", "original_language", "male_rate"]:
      user_preference[feature] = get_top_fea(duration_features, feature)

  return user_preference

## Build Hierarchy/attention scores

def create_movie_lists(tmdb_credit_df, tmdb_movie_df):
  ms = []

  for index in range(len(tmdb_credit_df)):
    ms.append({"id": tmdb_credit_df.movie_id[index],
              "title": tmdb_credit_df.title[index],
              "character": [],
              "cast": [],
              "male_rate": 0,
              "crew": [],
              'genres': [x['name'] for x in json.loads(tmdb_movies_df.genres[index])],
              'original_language': tmdb_movies_df.original_language[index],
              'popularity': tmdb_movies_df.popularity[index],
              'runtime': tmdb_movies_df.runtime[index],
              'rating': tmdb_movies_df.vote_average[index],
              }
            )

  m, f = 0, 0

  for c in json.loads(tmdb_credit_df.cast[index]):
    ms[index]["cast"].append(c["name"])
    ms[index]["character"].append(c["character"])
    if c["gender"] == 2:
      m += 1
    else:
      f += 1
  if m > 0 and f > 0:
    ms[index]["male_rate"] = m/(m+f)
  for crew in json.loads(tmdb_credit_df.crew[index]):
    if crew["job"] in ["Director", "Writer", "Producer"]:
      ms[index]["crew"].append(crew["name"])

  return ms

"""Get recommendations from the attention scores"""

def get_Recommendations(movie_list, hierarchy, user_preference):

  similarity_table, score_sheets = [], []
  score_sheet = {}
  for i in range(len(movie_list)):
    score_sheets.append([])

    score = 0
    score_sheet["genres"] = compare_lists(user_preference["genres"], movie_list[i]["genres"])
    score_sheet["crew"] = compare_lists(user_preference["crew"], movie_list[i]["crew"])
    score_sheet["character"] = compare_lists(user_preference["character"], movie_list[i]["character"])
    score_sheet["cast"] = compare_lists(user_preference["cast"], movie_list[i]["cast"])
    score_sheet["original_language"] = int(movie_list[i]["original_language"] == user_preference["original_language"])
    score_sheet["popularity"] = get_similarity(user_preference["popularity"], movie_list[i]["popularity"])
    score_sheet["rating"] = get_similarity(user_preference["rating"], movie_list[i]["rating"])
    score_sheet["male_rate"] = get_similarity(user_preference["male_rate"], movie_list[i]["male_rate"])

    for key in score_sheet:
      score += score_sheet[key] * hierarchy[key]

    similarity_table.append(score/(sum(hierarchy.values())))
    score_sheets[i].append(score_sheet)

  # score_sheets = np.array(score_sheets)
  similarity_table = np.array(similarity_table)

  return similarity_table, score_sheets, movie_list


"""## Display recommendations
- similarity_table: The matrix with each row containing a vector with corresponding similarity scores
- score_sheets: each attribute's similarity score
- movie_list: list containing all the dictionary of attributes of the corresponding
"""

def user_display(similarity_table, score_sheets, movie_list):

  movie_match_num = 15
  movie_similarities = {x: similarity_table[x] for x in range(len(similarity_table))}
  # id_sheet = {x: score_sheets[liked_id][x] for x in range(len(score_sheets))}

  similar_movies = sorted(movie_similarities.items(), key=lambda x:x[1], reverse=True)[1: movie_match_num + 1]

  print("Based on user preference, we got the following recommendation list:")
  print("Recommendations:")
  print("________________________________")
  for i in range(len(similar_movies)):
    print(i + 1, " " * (len(str(len(similar_movies))) - len(str(i + 1))) + "|", movie_list[similar_movies[i][0]]["title"], "|", "similarity:", str(round(similar_movies[i][1]*100, 2)) + "%")


def main(df):
  start_time = time.time()
  user_preference = build_user_preference(df)

  print("For user, preference is formed by the following features")
  for feature, value in user_preference.items():
    print(f"* Feature: {feature}")
    if type(value) == list:
      for v in value:
        print(f"--- {v}")

    else:
      print(value)

  movie_list = create_movie_lists(tmdb_credit_df, tmdb_movies_df)
  similarity_table, score_sheets, ms = get_Recommendations(movie_list, hierarchy, user_preference)
  assert similarity_table.shape[0] == len(ms)

  user_display(similarity_table, score_sheets, ms)

  print("Run time in total: ", time.time() - start_time)
  print("______End of Code______")


main(df)