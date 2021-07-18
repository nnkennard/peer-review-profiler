import argparse
import collections
import json
import numpy as np

parser = argparse.ArgumentParser(
    description='Consolidate annotations into single file')
parser.add_argument(
    '-d',
    '--run_directory',
    type=str,
    help='JSON file with review text to annotate with specificity')

class FeatureType(object):
  ARGUMENT = "argument"
  ASPECT = "aspect"
  POLITENESS = "politeness"
  SPECIFICITY = "specificity"
  ALL = [ARGUMENT, ASPECT, POLITENESS, SPECIFICITY]

def count_key(arg_name):
  return "count_{0}".format(arg_name)

def normalized_key(arg_name):
  return "norm_{0}".format(arg_name)

def featurize_list(feature_list):
  transformed = {}
  feat_counter = collections.Counter(feature_list)
  for arg_name, count in feat_counter.items():
    transformed[count_key(arg_name)] = count
    transformed[normalized_key(arg_name)] = count / len(feature_list)
  return transformed

def transform_argument(features):
  return featurize_list(features["argument_labels"])

def transform_aspect(features):
  return featurize_list([aspect for aspect, span in features["aspect_spans"]])

def central_tendencies(values, name):
  return {
    "mean_{0}".format(name): np.mean(values),
    "min_{0}".format(name): min(values),
    "max_{0}".format(name): max(values),
    "median_{0}".format(name): np.median(values)
  }

def transform_specificity(features):
  return central_tendencies(features["specificities"], "specificity")

TRANSFORM_MAP = {
  FeatureType.ARGUMENT: transform_argument,
  FeatureType.ASPECT: transform_aspect,
  FeatureType.POLITENESS: lambda x:x,
  FeatureType.SPECIFICITY: transform_specificity,
}

def get_feature_obj(dir_name, feature_type):
  with open(dir_name + "/" + feature_type + "_features.json", 'r') as f:
    return json.load(f)

def main():

  args = parser.parse_args()

  overall_features = collections.defaultdict(dict)

  for feature_name in FeatureType.ALL:
    for review_id, features in get_feature_obj(args.run_directory, feature_name).items():
      overall_features[review_id].update(TRANSFORM_MAP[feature_name](features))

  print(args.run_directory + "/final_features.json")

  with open(args.run_directory + "/final_features.json", 'w') as f:
    json.dump(overall_features, f)


if __name__ == "__main__":
  main()

