import argparse
import glob
import json
import stanza

from convokit import Speaker, Utterance, Corpus, TextParser, PolitenessStrategies

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i', '--input_dir', default='', type=str, help='')
parser.add_argument('-o', '--output_dir', default='', type=str, help='')


SENTENCIZE_PIPELINE = stanza.Pipeline("en", processors="tokenize")

convokit_TP = TextParser()
convokit_PS = PolitenessStrategies()
convokit_rev = Speaker(id="reviewer_id")


def length_featurizer(text):

    sentences = [[token.text for token in sentence_obj.tokens]
                 for sentence_obj in SENTENCIZE_PIPELINE(text).sentences]

    return {
        "char_len": len(text),
        "sentence_len": len(sentences),
        "token_len": len(sum(sentences, [])),
        "tokenized": sentences
    }


def politeness_featurizer(text):
    corpus = Corpus(utterances=[Utterance(text=text, speaker=convokit_rev)])
    corpus = convokit_PS.transform(convokit_TP.transform(corpus))
    return corpus.get_utterances_dataframe(
    )['meta.politeness_strategies'][None]


FEATURIZER_MAP = {
    "length": length_featurizer,
    "politeness": politeness_featurizer,
}


def featurize_text(text):
    features = {}
    for feature_name, featurizer in FEATURIZER_MAP.items():
        features.update(featurizer(text))
    return features


def featurize_file(path, output_dir):
    with open(path, 'r') as f:
        input_obj = json.load(f)
        output_obj = {}
        for key, text in input_obj.items():
            output_obj[key] = featurize_text(text)
    output_path = f'{output_dir}/' + path.split('/')[-1]
    with open(output_path, 'w') as f:
      f.write(json.dumps(output_obj, indent=2))


def main():

    args = parser.parse_args()

    for path in glob.glob(f'{args.input_dir}/*.json'):
        featurize_file(path, args.output_dir)


if __name__ == "__main__":
    main()
