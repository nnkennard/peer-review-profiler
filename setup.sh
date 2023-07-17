#!/bin/bash

# Create two virtual envs

create_virtualenv() {
  python_version=$1
  venv_name=$2
  requirements_file=$3


  conda create --name $venv_name python=$python_version
  conda activate $venv_name
  python -m pip install --upgrade pip
  python -m pip install -r $requirements_file
  conda deactivate
}

#create_virtualenv 3.9.0 prp_env requirements.txt
#create_virtualenv 3.7.3 prp_specificity_env requirements_specificity.txt

#git submodule update --init --recursive
#git submodule update --init --recursive # I don't know if these needs to be run twice? But I've had to

cd ReviewAdvisor/
# The following two downloads don't work. I manually download them through a browser and scp to the server.
#bash download_tagger.sh
#bash download_dataset.sh
cd tagger
ln -s ../seqlab_final/
sed -i 's/is_world_master/is_world_process_zero/' run_tagger.py

cd ../../

wget https://nlp.stanford.edu/data/glove.840B.300d.zip
unzip glove.840B.300d.zip
rm glove.840B.300d.zip
mv glove.840B.300d.txt Domain-Agnostic-Sentence-Specificity-Prediction


# This is for Convokit and Scibert
module load python3/3.9.0-2010
source ve/bin/activate

mkdir -p models/argument
cd models/argument
gdown https://drive.google.com/uc?id=1pd6wJ8A9xzWbS1--6iZ6E-b_1ZpxD37m
cd ../../

python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt')"
deactivate

# Specificity preparation

module load python3/3.7.3-1904
source specificity_ve/bin/activate
rm Domain-Agnostic-Sentence-Specificity-Prediction/dataset/data/twitter*
cp unlabeled_specificity/twitter* Domain-Agnostic-Sentence-Specificity-Prediction/dataset/data
touch  Domain-Agnostic-Sentence-Specificity-Prediction/dataset/data/twitterl.txt
touch  Domain-Agnostic-Sentence-Specificity-Prediction/dataset/data/twitterv.txt
cd  Domain-Agnostic-Sentence-Specificity-Prediction/
python train.py --gpu_id 0 --test_data twitter
deactivate
