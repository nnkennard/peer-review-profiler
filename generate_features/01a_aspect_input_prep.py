"""Script to prepare sentence for aspect labeling in ReviewAdvisor.

  TODO(NNK): Figure out why this newline replacement thing is required.

  Args:
    sys.argv[1]: input json file (correctly formatted)
    sys.argv[2]: output file location
"""

import json
import sys

import pipeline_lib

with open(pipeline_lib.get_input_file_name(sys.argv[1]), 'r') as f:
  with open(sys.argv[2], 'w') as g:
    g.write("\n".join(
        x["review_text"].replace("\n", " ") for x in json.load(f)))
