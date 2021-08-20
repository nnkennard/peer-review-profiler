"""Prepare input for specificity model."""

import argparse
import json

import pipeline_lib

parser = argparse.ArgumentParser(
    description='Prepare input for specificity model')
parser.add_argument('-o',
                    '--output_dir',
                    type=str,
                    help='Output directory for temp files')


def main():

  args = parser.parse_args()

  with open(pipeline_lib.get_input_file_name(args.output_dir), 'r') as f:
    obj = json.load(f)

  sentence_provenances = []
  sentences = []

  for example in obj:
    review_id = example["review_id"]
    for i, sentence in enumerate(example["review_sentences"]):
      sentences.append(sentence)
      sentence_provenances.append([review_id, i])

  with open(args.output_dir + "/specificity_provenances.json", 'w') as f:
    json.dump(sentence_provenances, f)

  # We have these twitter files in order to be similar to the original names
  # in the specificity model
  with open(args.output_dir + "/twitters.txt", 'w') as s_file:
    with open(args.output_dir + "/twitter.txt", 'w') as u_file:
      for handle in [s_file, u_file]:
        handle.write("sent_text\n")
        for sentence in sentences:
          handle.write(sentence + "\n")


if __name__ == "__main__":
  main()
