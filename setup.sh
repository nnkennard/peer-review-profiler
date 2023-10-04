conda create --name prp_env python=3.9
conda activate prp_env
python -m pip install stanza
python -m spacy download en_core_web_sm # for convokit
