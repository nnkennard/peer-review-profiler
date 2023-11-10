import argparse
import collections
import glob
import json
import stanza
import subprocess

from convokit import Speaker, Utterance, Corpus, TextParser, PolitenessStrategies

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i',
                    '--input_dir',
                    type=str,
                    help='Directory containing input-formatted JSON files.')
parser.add_argument(
    '-o',
    '--output_dir',
    type=str,
    help='Directory to which features JSON format should be written.')

SENTENCIZE_PIPELINE = stanza.Pipeline("en", processors="tokenize")

convokit_TP = TextParser()
convokit_PS = PolitenessStrategies()
convokit_rev = Speaker(id="reviewer_id")

SPECIFICITY_DIR = "Domain-Agnostic-Sentence-Specificity-Prediction/"


def length_featurizer(input_obj):
    features = {}
    for key, text in input_obj.items():
        sentences = [[token.text for token in sentence_obj.tokens]
                     for sentence_obj in SENTENCIZE_PIPELINE(text).sentences]
        features[key] = {
            "char_len": len(text),
            "sentence_len": len(sentences),
            "token_len": len(sum(sentences, [])),
            "tokenized": sentences
        }
    return features


def politeness_featurizer(input_obj):
    features = {}
    for key, text in input_obj.items():
        corpus = Corpus(
            utterances=[Utterance(text=text, speaker=convokit_rev)])
        corpus = convokit_PS.transform(convokit_TP.transform(corpus))
        features[key] = corpus.get_utterances_dataframe(
        )['meta.politeness_strategies'][None]
    return features


def aspect_featurizer(input_obj):
    key_order = []
    sample_file_lines = []
    for key, text in input_obj.items():
        key_order.append(key)
        sample_file_lines.append(text.replace('\n', ' '))
    # Prepare sample.txt file -- remove newlines between reviews
    with open('ReviewAdvisor/tagger/sample.txt', 'w') as f:
        f.write("\n".join(sample_file_lines) + "\n")
    # run tagger shell script
    subprocess.run('bash aspect_helper.sh'.split())

    features = {}
    with open('ReviewAdvisor/tagger/result.jsonl', 'r') as f:
        for key, result_str in zip(key_order, f.readlines()):
            result = json.loads(result_str)
            features[key] = dict(
                collections.Counter(f'aspect_{label[2]}'
                                    for label in result['labels']))
    return features


def specificity_featurizer(current_output_obj):
    sentence_provenances = []
    sentences = []
    for key, current_features in current_output_obj.items():
        for i, sentence in enumerate(current_features['tokenized']):
            sentence_provenances.append((key, i))
            sentences.append(" ".join(sentence))
    with open(f'{SPECIFICITY_DIR}/twitters.txt', 'w') as s_file:
        with open(f'{SPECIFICITY_DIR}/twitteru.txt', 'w') as u_file:
            for handle in [s_file, u_file]:
                handle.write("sent_text\n")
                for sentence in sentences:
                    handle.write(sentence + "\n")
    #subprocess.run('bash specificity_helper.sh'.split())


FEATURIZER_MAP = {
    "length": length_featurizer,
    "politeness": politeness_featurizer,
    "aspect": aspect_featurizer,
#    "specificity": specificity_featurizer,
}


def featurize_file(path, output_dir):
    with open(path, 'r') as f:
        input_obj = json.load(f)

    output_obj = collections.defaultdict(dict)
    for feature_name, batch_featurizer in FEATURIZER_MAP.items():
        if feature_name == "specificity":
            assert all('tokenized' in v for v in output_obj.values())
            features = batch_featurizer(output_obj)
        else:
            features = batch_featurizer(input_obj)
        for key, feature_map in features.items():
            output_obj[key].update(feature_map)

    output_path = f'{output_dir}/' + path.split('/')[-1]
    with open(output_path, 'w') as f:
        f.write(json.dumps(output_obj, indent=2))


def main():

    args = parser.parse_args()

    for path in glob.glob(f'{args.input_dir}/*.json'):
        featurize_file(path, args.output_dir)


if __name__ == "__main__":
    main()
