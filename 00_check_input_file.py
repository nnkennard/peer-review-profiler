import argparse
import json

parser = argparse.ArgumentParser(
    description='Check json input for pipeline')
parser.add_argument('-a',
                    '--annotation_file',
                    type=str,
                    help='Input json file to check')

def check_item(index, item):
  if 'review_id' not in item:
    print("Item {0} is missing the review_id field".format(index))
    return False
  elif not type(item['review_id']) == str:
    print(
        ("The value of review_id field should be a string; "
         "check item {0}").format(index))
    return False
  elif 'review_text' not in item:
    print("Item {0} is missing the review_text field".format(index))
    return False
  elif not type(item['review_text']) == str:
    print(
        ("The value of review_text field should be a string; "
         "check item {0}").format(index))
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
        print("You're good to go!")
    else:
      print("The top level type of the json file should be a list.")



if __name__ == "__main__":
  main()

