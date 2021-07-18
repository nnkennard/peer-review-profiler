"""Script to check if input json file is correctly formatted for features.

  The input file should be in json format:

  [
    {
      "review_text": "This is the first review. This is the second sentence of the first review.",
      "tokenized_review_text": [
          "This is the first review.",
          "This is the second sentence of the first review."],
      "review_id": "review_id_1"
    },
    {
      "review_text": "This is the second review. This is the second sentence of the second review.",
      "tokenized_review_text": [
          "This is the second review.",
          "This is the second sentence of the second review."],
      "review_id": "review_id_2"
    },
  ]

  Args:
    annotation_file: Input json file.

  Output:
    Prints approval message or location of first error.
"""


import argparse
import json

parser = argparse.ArgumentParser(description='Check json input for pipeline')
parser.add_argument('-a',
                    '--annotation_file',
                    type=str,
                    help='Input json file to check')


def check_item(index, item):
  """Check the format of an item representing the text of a single review.

    Args:
      index: Index of this item in the input file (for error message).
      item: json-formatted object representing single item.

    Returns:
      True if item is correctly formatted, False otherwise.
  """
  if 'review_id' not in item:
    print("Item {0} is missing the review_id field".format(index))
    return False
  elif not type(item['review_id']) == str:
    print(("The value of review_id field should be a string; "
           "check item {0}").format(index))
    return False
  elif 'review_text' not in item:
    print("Item {0} is missing the review_text field".format(index))
    return False
  elif not type(item['review_text']) == str:
    print(("The value of review_text field should be a string; "
           "check item {0}").format(index))
    return False
  elif 'tokenized_review_text' not in item:
    print("Item {0} is missing the tokenized_review_text field".format(index))
    return False
  elif not all(type(i) == str for i in item['tokenized_review_text']):
    print(("The value of tokenized_review_text field should be a list "
           "of strings; check item {0}").format(index))
    return False

  return True


def main():
  args = parser.parse_args()
  with open(args.annotation_file, 'r') as f:
    try:
      obj = json.load(f)
    except json.decoder.JSONDecodeError:
      print("Please use a valid JSON file")
      exit()

    if type(obj) == list:
      if all(check_item(i, item) for i, item in enumerate(obj)):
        print("You're good to go; {0} is formatted correctly".format(
            args.annotation_file))
    else:
      print("The top level type of the json file should be a list.")


if __name__ == "__main__":
  main()
