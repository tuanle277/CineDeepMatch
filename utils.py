from setup import *

# for list elements in dataset
def aggregate_list(interest_features, feature_name):
  assert feature_name in ["cast", "genres", "crew", "character"]

  feature_duration = {}
  for duration, features in interest_features.items():
    feature = json.loads(features[feature_name])
    for f in feature:
      if f not in feature_duration:
        feature_duration[f] = 0
      else:
        feature_duration[f] += duration

  feature_duration = {k: v for k, v in sorted(feature_duration.items(), key=lambda item: item[1], reverse=True)}

  return feature_duration

def get_top_k(interest_features, feature_name, k):
  feature_duration = aggregate_list(interest_features, feature_name)
  if feature_name == "cast":
    topk = [id_cast.iloc[x]["Cast"] for x in feature_duration.keys() if id_cast.iloc[x]["Cast"] != None][:k]
  elif feature_name == "character":
    topk = [id_chac.iloc[x]["Character"] for x in feature_duration.keys() if id_chac.iloc[x]["Character"] != None][:k]
  elif feature_name == "crew":
    topk = [id_crew.iloc[x]["Crew"] for x in feature_duration.keys() if id_crew.iloc[x]["Crew"] != None][:k]
  else:
    topk = [id_genres.iloc[x]["Genre"] for x in feature_duration.keys() if id_genres.iloc[x]["Genre"] != None][:k]

  assert type(topk) == list
  return topk

def get_top_fea(interest_features, feature_name):
  dumax, feamax = 0, None

  for duration, features in interest_features.items():
    feature = features[feature_name]
    if duration > dumax:
      dumax = duration
      feamax = feature

  return feamax

def compare_lists(l1, l2): # how much percent of l1 is in l2 -> use this to make the similarity table
  if len(l1) == 0 or len(l2) == 0:
    return 0
  l1, l2 = res = [*set(l1)], set(l2)

  matching = 0
  for e in l1:
    if e in l2:
      matching += 1

  return matching/len(l1)

def get_similarity(a, b):
  if a == b:
    return 1

  return (max(a, b) - abs(a - b)) / max(a, b)
