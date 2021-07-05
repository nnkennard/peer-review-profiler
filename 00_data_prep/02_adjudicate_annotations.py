import argparse
import collections
import itertools
import json

from statistics import mean

import annotation_lib

from nltk import agreement
from nltk.metrics import interval_distance, binary_distance

parser = argparse.ArgumentParser(
    description='Adjudicate common annotations to produce gold annotations')
parser.add_argument('-c',
                    '--clean_annotation_file',
                    type=str,
                    help='path to cleaned, anonymized annotation file')
parser.add_argument('-o',
                    '--output_file',
                    type=str,
                    help='path to adjudicated output file')

ALL_ANNOTATORS = ["anno{0}".format(i) for i in range(4)]

def get_agreement(trio):
  data = []
  for annotation in trio:
    for field in annotation_lib.BINARY_FIELDS:
      val = annotation[field]
      if val is None:
        return -1
      else:
        data.append((annotation["annotator"], field, val))

  task = agreement.AnnotationTask(data=data, distance=interval_distance)
  return task.alpha()


def select_best_trio(all_annotations):
  agreements = []
  best_agreement = float("-inf")
  best_trio = None
  for trio in itertools.combinations(all_annotations, 3):
    this_agreement = get_agreement(trio)
    if this_agreement > best_agreement:
      best_trio = trio
      best_agreement = this_agreement
  return trio

def get_adjudicated_annotation(best_trio):
  adjudicated_values = {}
  for field in annotation_lib.CATEGORICAL_FIELDS:
    values = collections.Counter([ann[field] for ann in best_trio])
    if len(values) == 3:
      adjudicated_values[field] = None
    adjudicated_values[field] = values.most_common(1)[0][0]
  for field in annotation_lib.LIKERT_FIELDS:
    values = collections.Counter([ann[field] for ann in best_trio])
    if len(values) == 3:
      adjudicated_values[field] = round(mean(values))
    else:
      adjudicated_values[field] = values.most_common(1)[0][0]
  adjudicated_values["annotator"] = "|".join(ann["annotator"] for ann in
  best_trio)
  adjudicated_values["review_id"] = best_trio[0]["review_id"]


def adjudicate(all_annotations):
  best_trio = select_best_trio(all_annotations)
  return get_adjudicated_annotation(best_trio)


def main():

  args = parser.parse_args()

  assert args.clean_annotation_file.endswith(".json")
  if args.output_file is None:
    output_file = args.clean_annotation_file.replace(".json", "_adjudicated.json")
  else:
    output_file = args.output_file

  final_examples = []
  with open(args.clean_annotation_file, 'r') as f:
    for example in json.load(f):
      all_annotations = example["all_annotations"]
      if len(all_annotations) == 1:
        gold_annotation, = all_annotations
      else:
        assert len(all_annotations) == 4
        gold_annotation = adjudicate(all_annotations)
      example["gold_annotation"] = gold_annotation
      final_examples.append(example)

  with open(output_file, 'w') as f:
    json.dump(final_examples, f)

if __name__ == "__main__":
  main()

