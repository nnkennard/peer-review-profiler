import argparse
import csv
import sys
import json

parser = argparse.ArgumentParser(
    description='Clean and anonymize annotation data')
parser.add_argument(
    '-i',
    '--input_file',
    type=str,
    help='JSON file with review text to annotate with specificity')
parser.add_argument(
    '-o',
    '--output_dir',
    type=str,
    help='Output directory for temp files')



def main():

  args = parser.parse_args()

  with open(args.input_file, 'r') as f:
    obj = json.load(f)

  sentence_provenances = []
  sentences = []

  for example in obj:
    review_id = example["review_id"]
    for i, sentence in enumerate(example["tokenized_review_text"]):
      sentences.append({"sent_text":sentence})
      sentence_provenances.append({
        "review_id": review_id,
        "sentence_index":i
      })

  with open(args.output_dir + "/specificity_provenances.csv", 'w') as f:
    w = csv.DictWriter(f, fieldnames=["review_id", "sentence_index"])
    w.writeheader()
    for row in sentence_provenances:
      w.writerow(row)

  with open(args.output_dir + "/twitters.csv", 'w') as s_file:
    with open(args.output_dir + "/twitteru.csv", 'w') as u_file:
      s_writer = csv.DictWriter(s_file, fieldnames=["sent_text"])
      u_writer = csv.DictWriter(u_file, fieldnames=["sent_text"])
      for writer in [s_writer, u_writer]:
        writer.writeheader()
        for sentence in sentences:
          writer.writerow(sentence)

if __name__ == "__main__":
  main()

