"""Script to consolidate aspect features with review_id.
"""

import argparse
import collections
import json

parser = argparse.ArgumentParser(
    description='Consolidate features from ReviewAdvisor')
parser.add_argument('-i',
                    '--input_file',
                    type=str,
                    help='Original JSON file used to generate aspect features.')
parser.add_argument('-r',
                    '--result_file',
                    type=str,
                    help='result.jsonl file produced by ReviewAdvisor tagger')
parser.add_argument('-o',
                    '--output_dir',
                    type=str,
                    help='Output directory for this run')


def main():
  args = parser.parse_args()

  text_and_ids = []
  with open(args.input_file, 'r') as f:
    input_obj = json.load(f)
    for x in input_obj:
      text_and_ids.append((x["review_text"], x["review_id"]))

  aspect_features = {}

  with open(args.result_file, 'r') as f:
    lines = f.readlines()
    for result_text, (review_text, review_id) in zip(lines, text_and_ids):
      result = json.loads(result_text)
      label_list = []
      for start, end, label in result["labels"]:
        label_list.append((label, result["text"][start:end]))
      aspect_features[review_id] = {"aspect_spans": label_list}

  with open(args.output_dir + "/aspect_features.json", 'w') as f:
    json.dump(aspect_features, f)


if __name__ == "__main__":
  main()
