TEMP_FILE_NAME="args_input_temp.txt"

python 02a_aspect_input_prep.py $1 "ReviewAdvisor/tagger/"$TEMP_FILE_NAME
cd ReviewAdvisor/tagger/
sed -i 's/is_world_master/is_world_process_zero/' run_tagger.py
ln -s ../seqlab_final/
bash prepare.sh $TEMP_FILE_NAME
python run_tagger.py config.json
bash post_process.sh

cd ../../

python 02b_format_aspect_results.py -i $1 -r ReviewAdvisor/tagger/results.jsonl

