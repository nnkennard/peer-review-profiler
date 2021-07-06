import collections

BINARY_FIELDS = ('importance originality method presentation interpretation '
                 'reproducibility').split()
LIKERT_FIELDS = "overall evidence constructiveness".split()
METAREVIEW = "metareview"
CATEGORICAL_FIELDS = BINARY_FIELDS + [METAREVIEW]
ALL_FIELDS = CATEGORICAL_FIELDS + LIKERT_FIELDS

METAREVIEW_VALUES = "nota maybe no yes-agree yes-disagree".split()
METAREVIEW_MAP = {value: i for i, value in enumerate(METAREVIEW_VALUES)}

Annotation = collections.namedtuple("Annotation",
                                    "review_id annotator".split() + ALL_FIELDS)

