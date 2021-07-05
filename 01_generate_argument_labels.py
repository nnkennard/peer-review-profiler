import argparse
import glob
import json
import nltk
import numpy as np
import re
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, SequentialSampler, TensorDataset
import transformers
from tqdm import tqdm
#from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
#from transformers import BertForSequenceClassification
#from transformers import BertTokenizer

parser = argparse.ArgumentParser(
    description='Clean and anonymize annotation data')
parser.add_argument(
    '-f',
    '--input_file',
    type=str,
    help='JSON file with review text to annotate with arguments')
parser.add_argument(
    '-d',
    '--input_dir',
    type=str,
    help='Directory containing JSON files to be annotated with arguments')
parser.add_argument('-m',
                    '--model',
                    type=str,
                    help='Pretrained SciBERT checkpoint')

ARGUMENT_LABEL_LIST = "fact evaluation request reference non-arg quote".split()


def get_sentences(review):
  text = re.sub(r'\n', ' ', review)
  text = re.sub(r' +', ' ', text)
  text = re.sub(r'\d.', '<NUM>', text)
  text = re.sub(r'al.', 'al', text)
  review_sentences = nltk.sent_tokenize(text)
  return review_sentences


def get_unlabeled_data(filepath=None):
  """
    Converts json file(s) containing entire reviews
    into a single dataframe contaning review sentences

    This is the input data for the model
    """
  data_dict = {}
  count = 0
  if filepath is not None:
    # process a single file
    process_review_file(filepath, data_dict, count, venue=None)
  else:
    # Process all reviews from a list of all conferences
    # stored at the top of this file
    for venue, path in tqdm(filepaths.items()):
      count += process_review_file(path, data_dict, count, venue)
  data_df = pd.DataFrame.from_dict(data_dict, orient='index')

  # if processing all conferences, save unlabeled input data
  if filepath is not None:
    data_df.to_csv(output_dir + 'unlabeled.csv')

  # Either ways, return the dataframe
  return data_df


def process_review_file(filepath, data_dict, count, venue):
  """
    Iteratively split a review into sentences, 
    add the sentences to a shared dictionary,
    and return the updated count 
    
    filepath: path to the JSON file of reviews
    data_dict: dictionary that stores all the sentences
    count: total number of sentences in the dictionary
    venue: conference venue (where the reviews are from)
    """
  with open(filepath, 'r') as f:
    data = json.load(f)
    reviews = data['review_rebuttal_pairs']
    for number, review in tqdm(enumerate(reviews)):
      review_sentences = get_sentences(review['review_text']['text'])
      assert len(review_sentences) > 0
      for sent in review_sentences:
        data_dict[count] = {
            'id': review['review_sid'],
            'number': review['index'],
            'review_sent': sent,
            'venue': venue,
            'decision': review['decision']
        }
        count += 1
  return count


SCIBERT_BASE = "allenai/scibert_scivocab_uncased"


def get_model_and_tokenizer(scibert_ckpt, device):

  model = transformers.BertForSequenceClassification.from_pretrained(
      SCIBERT_BASE,
      num_labels=6,
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
  """
  review_ids, review_texts = zip(*examples)

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

  print(predictions)
  predictions = torch.cat(predictions, dim=0)
  probs = F.softmax(predictions, dim=1).cpu().numpy()

  labels = []
  for p in probs:
    labels.append(ARGUMENT_LABEL_LIST[np.argmax(p)])



def main():

  args = parser.parse_args()

  if args.input_file is None and args.input_dir is None:
    print("Please enter an input file or input directory.")
    exit

  if args.input_file is not None:
    assert args.input_dir is None
    input_files = [args.input_file]
  else:
    assert args.input_dir is not None
    input_files = glob.glob(args.input_dir + "/*.json")

  example_list = []
  for input_file in input_files:
    with open(input_file, 'r') as f:
      example_list += [(x["review_id"], x["review_text"]) for x in json.load(f)]

  argument_features = get_argument_features(example_list, args.model)

  if args.output_file is not None:
    output_filename = args.output_file
  else:
    output_filename = "arguments_output.json"

  with open(output_filename, 'w') as f:
    json.dump(argument_features, f)


if __name__ == "__main__":
  main()
