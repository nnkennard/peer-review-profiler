#!/bin/bash

python generate_features/03a_prep_specificity_input.py -i  $1 -o $2

cp $2/twitter*  Domain-Agnostic-Sentence-Specificity-Prediction/dataset/data

cd  Domain-Agnostic-Sentence-Specificity-Prediction/
python train.py --gpu_id 0 --test_data twitter
python test.py --gpu_id 0 --test_data twitter 
mv  predictions.txt ../$2/specificity_predictions.txt
cd ../

python generate_features/03b_consolidate_specificity_output.py -d $2
