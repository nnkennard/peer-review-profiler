"""Generate politeness labels using Convokit."""

import argparse
import json
from nltk.tokenize import word_tokenize


parser = argparse.ArgumentParser(
    description='Generate politeness labels using Convokit.')
parser.add_argument(
    '-i',
    '--input_file',
    type=str,
    help='JSON file with review text to annotate with arguments')
parser.add_argument('-o', '--output_dir', type=str, help='Output JSON file')


def main():
  args = parser.parse_args()

  utterance_list = []

  overall_features = {}
  with open(args.input_file, 'r') as f:
    obj = json.load(f)
    for example in obj:
      overall_features["review_id"] = {
        "num_sentences": len(example["tokenized_review_text"]),
        "num_tokens": sum(len(word_tokenize(sent)) for sent in example["tokenized_review_text"])
      }
  
  with open(args.output_dir + "/length_features.json", 'w') as f:
    json.dump(overall_features, f)


if __name__ == "__main__":
  main()
