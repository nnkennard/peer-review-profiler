"""Generate argument labels using AMPERE dataset.
  Args:
    input_file: properly formatted input JSON file
    model: SciBERT model TODO(CL): Fill in the details of where this came from.
    output_dir: output directory for this run.

  Outputs:
    Argument lists at the sentence level are written to argument_features.json
      in the run directory.
"""

import argparse
import collections
import glob
import json
import numpy as np
import re
import torch
import torch.nn.functional as F
from tqdm import tqdm
import transformers
from torch.utils.data import DataLoader, SequentialSampler, TensorDataset

import pipeline_lib

parser = argparse.ArgumentParser(
    description='Generate argument labels using AMPERE dataset.')
parser.add_argument(
    '-f',
    '--input_file',
    type=str,
    help='JSON file with review text to annotate with arguments')
parser.add_argument('-m',
                    '--model',
                    type=str,
                    help='Pretrained SciBERT checkpoint')
parser.add_argument('-o', '--output_dir', type=str, help='Output JSON file')

SCIBERT_BASE = "allenai/scibert_scivocab_uncased"

def get_model_and_tokenizer(scibert_ckpt, device):
  """Load model from checkpoint and initialize tokenizer.

    Args:
      scibert_ckpt: path to SciBERT model checkpoint
      device: device for torch

    Returns:
      Classification model and tokenizer.
  """

  model = transformers.BertForSequenceClassification.from_pretrained(
      SCIBERT_BASE,
      num_labels=len(pipeline_lib.ArgumentType.ALL),
      output_attentions=False,
      output_hidden_states=False)

  model.to(device)
  model.load_state_dict(
      torch.load(scibert_ckpt, map_location=torch.device('cpu')))

  tokenizer = transformers.BertTokenizer.from_pretrained(SCIBERT_BASE,
                                                         do_lower_case=True)

  return model, tokenizer


def get_argument_features(examples, scibert_ckpt):
  """
    Runs the trained argument models in evaluation mode
    
    Args:
      examples: List of examples in json format
      scibert_ckpt: path to SciBERT model checkpoint

    Returns:
      A map from review ids to a list of argument features for each
  """
  keys, review_texts = zip(*examples)

  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  model, tokenizer = get_model_and_tokenizer(scibert_ckpt, device)
  encoded_data_test = tokenizer.batch_encode_plus(review_texts,
                                                  add_special_tokens=True,
                                                  return_attention_mask=True,
                                                  pad_to_max_length=True,
                                                  max_length=256,
                                                  truncation=True,
                                                  return_tensors='pt')

  batch_size = 16

  input_ids_test = encoded_data_test['input_ids']
  attention_masks_test = encoded_data_test['attention_mask']
  dataset_test = TensorDataset(input_ids_test, attention_masks_test)
  dataloader_test = DataLoader(dataset_test,
                               sampler=SequentialSampler(dataset_test),
                               batch_size=batch_size)

  model.eval()
  predictions = []
  for batch in tqdm(dataloader_test):
    batch = tuple(b.to(device) for b in batch)
    inputs = {
        'input_ids': batch[0],
        'attention_mask': batch[1],
    }
    with torch.no_grad():
      output = model(**inputs)
    logits = output[0]
    predictions.append(logits)

  predictions = torch.cat(predictions, dim=0)
  probs = F.softmax(predictions, dim=1).cpu().numpy()

  labels = []
  for p in probs:
    labels.append(pipeline_lib.ArgumentType.ALL[np.argmax(p)])

  label_sequence_builder = collections.defaultdict(
      lambda: collections.defaultdict())

  for key, label in zip(keys, labels):
    review_id, index = retrieve_from_sentence_key(key)
    label_sequence_builder[review_id][index] = label

  features = {}
  for review_id, labels in label_sequence_builder.items():
    assert list(sorted(labels.keys())) == list(range(len(labels)))
    features[review_id] = {
        "argument_labels": [labels[i] for i in sorted(labels.keys())]
    }

  return features


def create_sentence_key(review_id, index):
  return "{0}|||{1}".format(review_id, index)


def retrieve_from_sentence_key(sentence_key):
  review_id, index = sentence_key.split("|||")
  return review_id, int(index)


def get_example_tuples(file_example_list):
  """Get tuples for argument input from example list.

    Args:
      file_example_list: JSON list of examples

    Returns:
      A list of (sentence_key, sentence) tuples
        where sentence key is of the format review_id|||sentence_index
  """

  example_tuples = []
  for example in file_example_list:
    for i, sentence in enumerate(example["tokenized_review_text"]):
      example_tuples.append((create_sentence_key(example["review_id"],
                                                 i), sentence))
  return example_tuples


def main():

  args = parser.parse_args()

  example_list = []
  with open(args.input_file, 'r') as f:
    example_list += get_example_tuples(json.load(f))

  argument_features = get_argument_features(example_list, args.model)

  with open(args.output_dir + "/argument_features.json", 'w') as f:
    json.dump(argument_features, f)


if __name__ == "__main__":
  main()
