"""Consolidate output of specificity model."""
import argparse
import collections
import csv
import json
from torch import tensor

parser = argparse.ArgumentParser(
    description='Consolidate output of specificity model.')
parser.add_argument('-d', '--dir_name', type=str, help='Directory for this run')


def main():

  args = parser.parse_args()

  provenances = []
  with open(args.dir_name + "/specificity_provenances.json", 'r') as f:
    provenances = json.load(f)

  with open(args.dir_name + "/specificity_predictions.txt", 'r') as f:
    values = [eval(line).item() for line in f]

  obj_builder = collections.defaultdict(dict)
  for (review_id, sentence_idx), value in zip(provenances, values):
    obj_builder[review_id][sentence_idx] = value

  final_builder = {}
  for review_id, specificities in obj_builder.items():
    assert list(sorted(specificities.keys())) == list(range(len(specificities)))
    final_builder[review_id] = {
        "specificities": [specificities[i] for i in range(len(specificities))]
    }

  with open(args.dir_name + "/specificity_features.json", 'w') as f:
    json.dump(final_builder, f)


if __name__ == "__main__":
  main()
