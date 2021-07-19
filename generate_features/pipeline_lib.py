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
  ALL = [ARGUMENT, ASPECT, POLITENESS, SPECIFICITY]


