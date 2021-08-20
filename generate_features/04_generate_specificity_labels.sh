#!/bin/bash

python generate_features/04a_prep_specificity_input.py -o $1

cp $1/twitter*  Domain-Agnostic-Sentence-Specificity-Prediction/dataset/data

python test.py --gpu_id 0 --test_data twitter 
mv  predictions.txt ../$1/specificity_predictions.txt
cd ../

python generate_features/04b_consolidate_specificity_output.py -d $1
