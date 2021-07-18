TEMP_FILE_NAME="args_input_temp.txt"

python generate_features/01a_aspect_input_prep.py $1 "ReviewAdvisor/tagger/"$TEMP_FILE_NAME

# These steps are part of the ReviewAdvisor pipeline
cd ReviewAdvisor/tagger/
bash prepare.sh $TEMP_FILE_NAME
python run_tagger.py config.json
bash post_process.sh

cd ../../

python generate_features/01b_format_aspect_results.py -i $1 -r ReviewAdvisor/tagger/result.jsonl -o $2

