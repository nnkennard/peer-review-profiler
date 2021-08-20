"""Script to check if input json file is correctly formatted for features.

  The input file should be in json format:

  [
    {
      "review_text": "This is the first review. This is the second sentence of the first review.",
      "review_sentences": [
          "This is the first review.",
          "This is the second sentence of the first review."],
      "review_id": "review_id_1"
    },
    {
      "review_text": "This is the second review. This is the second sentence of the second review.",
      "review_sentences": [
          "This is the second review.",
          "This is the second sentence of the second review."],
      "review_id": "review_id_2"
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
from nltk.tokenize import sent_tokenize

import pipeline_lib

parser = argparse.ArgumentParser(description='Check json input for pipeline')
parser.add_argument('-a',
                    '--annotation_file',
                    type=str,
                    help='Input json file to check')
parser.add_argument('-o', '--output_dir', type=str, help='Output JSON file')



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
    tokenized_sentences = sent_tokenize(item["review_text"])
    assert type(tokenized_sentences) == list and all(type(x) == str for x in tokenized_sentences)
    item.update({"review_sentences" : tokenized_sentences})
    return item
  elif not all(type(i) == str for i in item['review_sentences']):
    print(("The value of review_sentences field should be a list "
           "of strings; check item {0}").format(index))
    return None

  return item


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
      print("You're good to go; {0} is formatted correctly".format(
            args.annotation_file))
    else:
      print("The top level type of the json file should be a list.")

  with open(pipeline_lib.get_input_file_name(args.output_dir), 'w') as f:
    json.dump(final_items, f)


if __name__ == "__main__":
  main()
