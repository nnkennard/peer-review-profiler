#!/bin/bash

#module load python3/3.9.0-2010

#python3 -m venv ve
#source ve/bin/activate
#python -m pip install --upgrade pip
#python -m pip install -r requirements.txt

#git submodule update --init --recursive
#git submodule update --init --recursive # I don't know if these needs to be run twice? But I've had to

cd ReviewAdvisor/
bash download_tagger.sh
bash download_dataset.sh
cd tagger
ln -s ../seqlab_final/
sed -i 's/is_world_master/is_world_process_zero/' run_tagger.py

#cd ../../

#wget https://nlp.stanford.edu/data/glove.840B.300d.zip
#unzip glove.840B.300d.zip
#rm glove.840B.300d.zip
#mv glove.840B.300d.txt Domain-Agnostic-Sentence-Specificity-Prediction

#mkdir -p models/argument
# ??? Where to get the SciBert model???

# This is for Convokit
#python -m spacy download en_core_web_sm