"""Generate combined feature using argument and specificity JSON files.
  Args:
    run_directory: input and output directory for this run.

  Outputs:
    Combination score lists at the sentence level are written to combined_features.json
      in the run directory.
"""

import argparse
import collections
import json

import pipeline_lib

parser = argparse.ArgumentParser(
    description=
    'Generate combined feature using argument and specificity JSON files.')
parser.add_argument('-d',
                    '--run_directory',
                    type=str,
                    help='Input and output directory for this run')


def get_feature_obj(dir_name, feature_type):
  with open(dir_name + "/" + feature_type + "_features.json", 'r') as f:
    return json.load(f)


def get_score(combined_features):
  significant_argument = ["evaluation", "request"]
  combination_socre = collections.defaultdict(dict)
  for review_id, features in combined_features.items():
    argument_labels = features["argument_labels"]
    specificities = features["specificities"]
    scores = []
    n = len(argument_labels)
    for i, label in enumerate(argument_labels):
      score = 0
      if label in significant_argument:
        score = round(specificities[i] / n, 5)
      scores.append(score)
    combination_socre[review_id] = {"combination_score": scores}

  return combination_socre


def main():

  args = parser.parse_args()

  combined_features = collections.defaultdict(dict)
  for feature_name in pipeline_lib.CombinedFeatureType.ALL:
    for review_id, features in get_feature_obj(args.run_directory,
                                               feature_name).items():
      combined_features[review_id].update(features)

  combination_score = get_score(combined_features)

  with open(args.run_directory + "/combined_features.json", 'w') as f:
    json.dump(combination_score, f)


if __name__ == "__main__":
  main()
