import json
import sys

with open(sys.argv[1], 'r') as f:
  with open(sys.argv[2], 'w') as g:
    g.write("\n".join(
        x["review_text"].replace("\n", " ") for x in json.load(f)))
