#!/bin/bash

# Create two virtual envs

create_virtualenv() {
  module_name=$1
  venv_name=$2
  requirements_file=$3

  module load $module_name
    python3 -m venv $venv_name
    source $venv_name/bin/activate
      python -m pip install --upgrade pip
      python -m pip install -r $requirements_file
    deactivate
  module unload $module_name

}

create_virtualenv python3/3.9.0-2010 ve requirements.txt
create_virtualenv python3/3.7.3-1904 specificity_ve requirements_specificity.txt

#git submodule update --init --recursive
#git submodule update --init --recursive # I don't know if these needs to be run twice? But I've had to

#cd ReviewAdvisor/
#bash download_tagger.sh
#bash download_dataset.sh
#cd tagger
#ln -s ../seqlab_final/
#sed -i 's/is_world_master/is_world_process_zero/' run_tagger.py

#cd ../../

#wget https://nlp.stanford.edu/data/glove.840B.300d.zip
#unzip glove.840B.300d.zip
#rm glove.840B.300d.zip
#mv glove.840B.300d.txt Domain-Agnostic-Sentence-Specificity-Prediction

#mkdir -p models/argument
#cd models/argument
#wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-6QMv3NahTukRniYyc_RGBkWzxrkyDTw' -O 'SciBert.model'
#cd ../../

# This is for Convokit
python -m spacy download en_core_web_sm

deactivate

# Specificity preparation

python3 -m venv ve_specificity
source ve_specificity/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_specificity.txt

#cp unlabeled_specificity/twitter* Domain-Agnostic-Sentence-Specificity-Prediction/
#cd  Domain-Agnostic-Sentence-Specificity-Prediction/
#python train.py --gpu_id 0 --test_data twitter

deactivate
