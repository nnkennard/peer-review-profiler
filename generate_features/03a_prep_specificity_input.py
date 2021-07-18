import argparse
import json

parser = argparse.ArgumentParser(
    description='Clean and anonymize annotation data')
parser.add_argument(
    '-i',
    '--input_file',
    type=str,
    help='JSON file with review text to annotate with specificity')
parser.add_argument('-o',
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
      sentences.append(sentence)
      sentence_provenances.append([review_id, i])

  with open(args.output_dir + "/specificity_provenances.json", 'w') as f:
    json.dump(sentence_provenances, f)

  with open(args.output_dir + "/twitters.txt", 'w') as s_file:
    with open(args.output_dir + "/twitter.txt", 'w') as u_file:
      for handle in [s_file, u_file]:
        handle.write("sent_text\n")
        for sentence in sentences:
          handle.write(sentence + "\n")


if __name__ == "__main__":
  main()
