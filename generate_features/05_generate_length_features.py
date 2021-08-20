"""Generate politeness labels using Convokit."""

import argparse
import json
from nltk.tokenize import word_tokenize

import pipeline_lib

parser = argparse.ArgumentParser(
    description='Generate politeness labels using Convokit.')
parser.add_argument('-o', '--output_dir', type=str, help='Output JSON file')


def main():
  args = parser.parse_args()

  utterance_list = []

  overall_features = {}
  with open(pipeline_lib.get_input_file_name(args.output_dir), 'r') as f:
    obj = json.load(f)
    for example in obj:
      overall_features["review_id"] = {
        "num_sentences": len(example["review_sentences"]),
        "num_tokens": sum(len(word_tokenize(sent)) for sent in example["review_sentences"])
      }

  with open(args.output_dir + "/length_features.json", 'w') as f:
    json.dump(overall_features, f)


if __name__ == "__main__":
  main()
