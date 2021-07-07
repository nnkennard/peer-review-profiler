#!/bin/bash

python generate_features/03a_prep_specificity_input.py -i  $1 -o $2

mv $2/twitter*  Domain-Agnostic-Sentence-Specificity-Prediction/

cd  Domain-Agnostic-Sentence-Specificity-Prediction/
python train.py --gpu_id 0 --test_data twitter
python test.py --gpu_id 0 --test_data twitter 
mv  predictions.txt ../$2
cd ../$2

head predictions.txt
head specificity_provenances.csv
