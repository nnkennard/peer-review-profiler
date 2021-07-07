import argparse
import json

parser = argparse.ArgumentParser(
    description='Clean and anonymize annotation data')
parser.add_argument(
    '-f',
    '--input_file',
    type=str,
    help='JSON file with review text to annotate with arguments')
parser.add_argument(
    '-o',
    '--output_dir',
    type=str,
    help='Output JSON file')


def main():
  args = parser.parse_args()

  with open(args.input_file, 'r') as f:
    obj = json.loads(f)
  pass


if __name__ == "__main__":
  main()

