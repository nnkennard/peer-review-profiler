#!/bin/bash

input_file="final_annotated.json"
run_name="run0"
 
while getopts ":i:r:" opt; do
  case $opt in
    i) input_file="$OPTARG"
    ;;
    r) run_name="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2; exit
    ;;
  esac
done
 
if [ -d "${run_name}" ]; then
  echo "Run named ${run_name} exists; please choose another name"
  exit
fi

mkdir ${run_name}

echo "Checking input file"
python generate_features/00_check_input_file.py -a $input_file

echo "Generating aspect labels"
bash generate_features/01_generate_aspect_labels.sh \
	$input_file ${run_name}

echo "Generating argument labels"
python generate_features/02_generate_argument_labels.py \
	-f $input_file -m models/argument/SciBert.model \
	-o ${run_name}

echo "Generating specificity labels"
bash generate_features/03_generate_specificity_labels.sh \
	$input_file ${run_name}

