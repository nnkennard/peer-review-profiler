#!/bin/bash

set -e

cur_dir=`pwd`

cd ReviewAdvisor/
bash download_tagger.sh
bash download_dataset.sh

wget https://nlp.stanford.edu/data/glove.840B.300d.zip
unzip glove.840B.300d.zip
rm glove.840B.300d.zip
mkdir -p models/specificity
mv glove.840B.300d.txt models/specificity

