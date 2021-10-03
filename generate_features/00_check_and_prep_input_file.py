"""Script to check if input json file is correctly formatted for features.

  The input file should be in json format:

  [
    {
      "review_text": "This is the first review. This is the second sentence of the first review.",
      "review_sentences": [
          "This is the first review.",
          "This is the second sentence of the first review."],
      "review_id": "review_id_1",
      "score": 5,
    },
    {
      "review_text": "This is the second review. This is the second sentence of the second review.",
      "review_sentences": [
          "This is the second review.",
          "This is the second sentence of the second review."],
      "review_id": "review_id_2"
      "score": 3,
    },
  ]

  The review_sentences field is optional. If it is not present, the sentences
  in review_text are separated using NLTK

  Args:
    annotation_file: Input json file.

  Output:
    Prints approval message or location of first error.
"""

import argparse
import json
import nltk
import re

import pipeline_lib

parser = argparse.ArgumentParser(description='Check json input for pipeline')
parser.add_argument('-a',
                    '--annotation_file',
                    type=str,
                    help='Input json file to check')
parser.add_argument('-o', '--output_dir', type=str, help='Output JSON file')

PRE_TOKENIZATION_REGEXES = [
    (r'\n', ' '),
    (r'(\d)(?:\.) ', '\g<1>, '),
    (r'((\b\w)+)(?:\.)', '\g<1> '),
    (r'(?i)etc.', 'etc'),
    (r'(?i)eqn.', 'eqn'),
    (r'(?i)eq.', 'eq'),
    (r'(?i)fig.', 'fig'),
    (r'(?i)sec.', 'sec'),
    (r'al.', 'al'),
    (r' +', ' '),
]

VALID_SCORES = [i / 2 for i in range(2, 11)]


def sentence_separate(text):
  for regex, replacement in PRE_TOKENIZATION_REGEXES:
    text = re.sub(regex, replacement, text)
  return nltk.sent_tokenize(text)


def check_for_score(item, index):
  if 'score' not in item:
    return item, False
  else:
    if item['score'] not in VALID_SCORES:
      print(type(item["score"]), item["score"])
      print("Score should be in the range 1-5; please check item {0}".format(
          index))
      return None
    else:
      return item, True


def check_item(index, item):
  """Check the format of an item representing the text of a single review.

    Args:
      index: Index of this item in the input file (for error message).
      item: json-formatted object representing single item.

    Returns:
      Finalized item if correctly formatted, None otherwise.
  """
  if 'review_id' not in item:
    print("Item {0} is missing the review_id field".format(index))
    return None
  elif not type(item['review_id']) == str:
    print(("The value of review_id field should be a string; "
           "check item {0}").format(index))
    return None
  elif 'review_text' not in item:
    print("Item {0} is missing the review_text field".format(index))
    return None
  elif not type(item['review_text']) == str:
    print(("The value of review_text field should be a string; "
           "check item {0}").format(index))
    return None
  elif 'review_sentences' not in item:
    tokenized_sentences = sentence_separate(item["review_text"])
    assert type(tokenized_sentences) == list and all(
        type(x) == str for x in tokenized_sentences)
    item.update({"review_sentences": tokenized_sentences})
    return check_for_score(item, index)
  elif not all(type(i) == str for i in item['review_sentences']):
    print(("The value of review_sentences field should be a list "
           "of strings; check item {0}").format(index))
  else:
    return check_for_score(item, index)


def main():
  args = parser.parse_args()
  with open(args.annotation_file, 'r') as f:
    try:
      obj = json.load(f)
    except json.decoder.JSONDecodeError:
      print("Please use a valid JSON file")
      exit()

    if type(obj) == list:
      final_items = [check_item(i, item) for i, item in enumerate(obj)]
      assert None not in final_items
      items, has_score_values = zip(*final_items)
      if all(has_score_values):
        print("All items have a score; analysis will be carried out.")
      else:
        print(
            "Some items do not have a score; no analysis will be carried out.")
        print("Items at these indices do not have scores:", [
            i for i in range(len(has_score_values)) if not has_score_values[i]
        ])
      print("You're good to go; {0} is formatted correctly".format(
          args.annotation_file))
    else:
      print("The top level type of the json file should be a list.")

  with open(pipeline_lib.get_input_file_name(args.output_dir), 'w') as f:
    json.dump(items, f)


if __name__ == "__main__":
  main()
