import argparse
import csv
import json

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i', '--input_csv', default='', type=str, help='')
parser.add_argument('-o', '--output_json', default='', type=str, help='')



CONTENT_KEYS = [
"Q1 (Summary)",
"Q3 (Justification of the score)",
"Q4 (Detailed feedback)",
"Q6 (Questions for the author response.)",
"Q10 (Confidential comments to SPC, AC and Program Chair)"
]

PAPER_ID = "Paper ID"
REVIEWER_NUMBER = "Reviewer Number"

def main():
  args = parser.parse_args()

  review_texts = {}
  with open(args.input_csv, 'r') as f:
    dr = csv.DictReader(f)
    for row in dr:
      identifier = f'{row[PAPER_ID]}|||{row[REVIEWER_NUMBER]}'
      assert identifier not in review_texts
      review_texts[identifier] = "\n".join([row[key] for key in CONTENT_KEYS])

  with open(args.output_json, 'w') as f:
    f.write(json.dumps(review_texts, indent=2))



if __name__ == "__main__":
  main()

