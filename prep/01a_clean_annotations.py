import argparse
import collections
import json
import nltk
import re

import annotation_lib

parser = argparse.ArgumentParser(
    description='Clean and anonymize annotation data')
parser.add_argument('-a',
                    '--annotation_file',
                    type=str,
                    help='path to Django annotation dump')
parser.add_argument('-o',
                    '--output_file',
                    type=str,
                    help='path to cleaned output file')

VALID_ANNOTATORS = "AS CL DP SB".split()
ANNOTATOR_MAP = {
    initials: "anno{0}".format(i)
    for i, initials in enumerate(sorted(VALID_ANNOTATORS))
}

REVIEW_FILE_MAP = {
    'iclr18': 'annotation_data/iclr18_ann.json',
    'neurips18': 'annotation_data/neurips18_ann_sm.json'
}

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

def sentence_separate(text):
  for regex, replacement in PRE_TOKENIZATION_REGEXES:
    text = re.sub(regex, replacement, text)
  return nltk.sent_tokenize(text)


def build_text_map(review_file_map):
  overall_text_map = {}
  for conference, filename in review_file_map.items():
    with open(filename, 'r') as f:
      text_data = json.load(f)
      assert conference == text_data["conference"]
      for review_rebuttal_pair in text_data["review_rebuttal_pairs"]:
        review_sid = review_rebuttal_pair["review_sid"]
        assert review_sid not in overall_text_map
        text = review_rebuttal_pair["review_text"]["text"]
        overall_text_map[review_sid] = (text, sentence_separate(text))

  return overall_text_map


def get_assigned_annotators(text_map):
  sorted_iclr_ids = sorted(k for k in text_map.keys() if "NIPS" not in k)
  sorted_neurips_ids = sorted(k for k in text_map.keys() if "NIPS" in k)

  valid_annotators = collections.defaultdict(set)
  for common_id in sorted_iclr_ids[149:200] + sorted_neurips_ids[0:28]:
    valid_annotators[common_id].update(VALID_ANNOTATORS)

  single_annotator_map = {
      "AS": sorted_iclr_ids[:149],
      "CL": sorted_neurips_ids[90:],
      "DP": sorted_iclr_ids[201:],
      "SB": sorted_neurips_ids[29:90]
  }

  for ann, ids in single_annotator_map.items():
    for ann_id in ids:
      valid_annotators[ann_id].add(ann)

  return valid_annotators

def metareview_cleanup(key, value):
  if key == value:
    return key
  elif key.lower() == annotation_lib.METAREVIEW:
    return value
  else:
    assert value.lower() == annotation_lib.METAREVIEW
    return key


def clean_ratings(ratings_json, pk):
  new_ratings = {}
  for k, v in json.loads(ratings_json).items():
    try:
      int_value = int(v)
      if k in annotation_lib.BINARY_FIELDS:
        if pk < 28:
          int_value = int(int_value > 2)
        else:
          assert int_value in range(2)
      new_ratings[k.lower()] = int_value
    except ValueError:  # Probably metareview field
      new_ratings[annotation_lib.METAREVIEW] = metareview_cleanup(k, v)
  return new_ratings


def get_conference_and_text(review_id, text_map):
  conference = "neurips18" if 'NIPS' in review_id else "iclr18"
  text = text_map[review_id]
  return conference, text


class CleanedAnnotation(object):

  def __init__(self, annotations, text_map, annotator_map, review_id):
    final_annotations = self._get_final_annotations(annotations)
    self.all_annotations = [
        self._clean_annotation(ann, annotator_map) for ann in final_annotations
    ]
    self.conference, (self.text, self.tokenized_text) = get_conference_and_text(
        review_id, text_map)
    self.review_id = review_id

  def _get_final_annotations(self, annotations):
    sorted_annotations = sorted(annotations,
                                key=lambda x: x["pk"],
                                reverse=True)
    selected_annotations = {}
    for ann in sorted_annotations:
      annotator = ann["fields"]["annotator_initials"]
      if annotator not in selected_annotations:
        selected_annotations[annotator] = ann
    return list(selected_annotations.values())

  def _clean_annotation(self, annotation, annotator_map):
    cleaned_ratings = clean_ratings(annotation["fields"]["ratings"],
                                    annotation["pk"])
    values_for_annotation = [
        cleaned_ratings.get(key, None) for key in annotation_lib.ALL_FIELDS
    ]
    return annotation_lib.Annotation(annotation["fields"]["review_id"],
                      annotator_map[annotation["fields"]["annotator_initials"]],
                      *values_for_annotation)

  def asdict(self):
    return {
        "review_text": self.text,
        "tokenized_review_text": self.tokenized_text,
        "all_annotations": [ann._asdict() for ann in self.all_annotations],
        "conference": self.conference,
        "review_id": self.review_id,
    }



def main():

  args = parser.parse_args()

  assert args.annotation_file.endswith(".json")
  if args.output_file is None:
    output_file = args.annotation_file.replace(".json", "_clean.json")
  else:
    output_file = args.output_file

  text_map = build_text_map(REVIEW_FILE_MAP)
  assigned_annotators = get_assigned_annotators(text_map)

  annotation_map = collections.defaultdict(list)

  with open(args.annotation_file, 'r') as f:
    overall_obj = json.load(f)
    for annotation in overall_obj:
      review_id = annotation["fields"]["review_id"]
      if annotation["fields"]["annotator_initials"] in assigned_annotators[
          review_id]:
        annotation_map[review_id].append(annotation)

  clean_annotation_list = []
  for review_id, annotations in annotation_map.items():
    clean_annotation_list.append(CleanedAnnotation(
        annotations, text_map, ANNOTATOR_MAP, review_id).asdict())

  with open(output_file, 'w') as f:
    json.dump(clean_annotation_list, f)


if __name__ == "__main__":
  main()
