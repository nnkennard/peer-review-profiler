class ArgumentType(object):
  FACT = "fact"
  EVALUATION = "evaluation"
  REQUEST = "request"
  REFERENCE = "reference"
  NONARG = "non-arg"
  QUOTE = "quote"
  ALL = [FACT, EVALUATION, REQUEST, REFERENCE, NONARG, QUOTE]

class FeatureType(object):
  ARGUMENT = "argument"
  ASPECT = "aspect"
  POLITENESS = "politeness"
  SPECIFICITY = "specificity"
  LENGTH = "length"
  COMBINED = "combined"
  ALL = [ARGUMENT, ASPECT, POLITENESS, SPECIFICITY, LENGTH, COMBINED]

class CombinedFeatureType(object):
  ARGUMENT = "argument"
  SPECIFICITY = "specificity"
  ALL = [ARGUMENT, SPECIFICITY]

def get_input_file_name(run_dir):
  return run_dir + "/input.json"
