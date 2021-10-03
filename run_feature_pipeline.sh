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

module load python3/3.9.0-2010
module load python3/3.7.3-1904

mkdir ${run_name}

source ve/bin/activate

echo "Checking input file"
python generate_features/00_check_and_prep_input_file.py -a $input_file -o ${run_name}

echo "Generating aspect labels"
bash generate_features/01_generate_aspect_labels.sh \
	${run_name}

echo "Generating argument labels"
python generate_features/02_generate_argument_labels.py \
	-m models/argument/SciBert.model \
	-o ${run_name}


echo "Generating length features"
python generate_features/03_generate_length_features.py \
  -o $run_name

deactivate
source specificity_ve/bin/activate

echo "Generating specificity labels"
bash generate_features/04_generate_specificity_labels.sh \
	$run_name

deactivate
source ve/bin/activate

echo "Generating politeness labels"
python generate_features/05_generate_politeness_labels.py \
  -o $run_name

echo "Generating combination scores"
python generate_features/06_generate_combined_feature.py \
   -d $run_name

echo "Consolidating and transforming features"
python generate_features/07_consolidate_features.py \
	-d $run_name

echo "Analyzing features"
python generate_features/08_correlation_with_quality.py \
   -i ${run_name}/input.json \
   -d $run_name

mkdir ${run_name}/plots

echo "Plotting heatmaps"
python generate_features/09_plot_heatmaps.py \
   -d $run_name

echo "Producing result table"
python generate_features/10_produce_table.py \
   -d $run_name

