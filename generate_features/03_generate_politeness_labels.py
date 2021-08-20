"""Generate politeness labels using Convokit."""

import argparse
import json

from convokit import Speaker, Utterance, Corpus, TextParser, PolitenessStrategies

import pipeline_lib

parser = argparse.ArgumentParser(
    description='Generate politeness labels using Convokit.')
parser.add_argument('-o', '--output_dir', type=str, help='Output JSON file')


def main():
  args = parser.parse_args()

  reviewer_speakers = [
      Speaker(id="reviewer_id0", name="Reviewer0"),
      Speaker(id="reviewer_id1", name="Reviewer1")
  ]
  utterance_list = []
  text_parser = TextParser()
  ps = PolitenessStrategies()

  overall_features = {}
  with open(pipeline_lib.get_input_file_name(args.output_dir), 'r') as f:
    obj = json.load(f)
    for example in obj:
      review_id = example["review_id"]
      features = []
      corpus = Corpus(
          utterances=[Utterance(text=example["review_text"],
          speaker=reviewer_speakers[0])])
      corpus = text_parser.transform(corpus)
      corpus = ps.transform(corpus, markers=True)
      overall_features[review_id] = corpus.get_utterances_dataframe()[
          "meta.politeness_strategies"][0]

  with open(args.output_dir + "/politeness_features.json", 'w') as f:
    json.dump(overall_features, f)


if __name__ == "__main__":
  main()
