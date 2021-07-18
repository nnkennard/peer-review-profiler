#!/bin/bash

python -m venv ve
source ve/bin/activate
python -m pip install -r requirements.txt

cd ReviewAdvisor/
bash download_tagger.sh
bash download_dataset.sh
cd tagger
ln -s ../seqlab_final/
sed -i 's/is_world_master/is_world_process_zero/' run_tagger.py

cd ../../

wget https://nlp.stanford.edu/data/glove.840B.300d.zip
unzip glove.840B.300d.zip
rm glove.840B.300d.zip
mkdir -p models/specificity
mv glove.840B.300d.txt models/specificity

mkdir -p models/argument
# ??? Where to get the SciBert model???

# This is for Convokit
python -m spacy download en_core_web_sm
