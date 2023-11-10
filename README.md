This was tested on Unity.

# Setup
Create a conda environment with requirements:
```
conda create --name profiler_env python=3.9
conda activate profiler_env
python -m pip install -r requirements.txt
```

## Aspect
We require a separate environment for aspect features
You won't have to activate this environment, it's activated in a subprocess from the featurizer script.
```
conda create --name profiler_aspect_env python=3.8
conda deactivate
conda activate profiler_aspect_env
python -m pip install -r ReviewAdvisor/tagger/requirements.txt
```

ReviewAdvisor also requires that you download their data and model files. You should be able to use `ReviewAdvisor/download_dataset.sh` and `ReviewAdvisor/download_tagger.sh`, but I ran into some problems with Google Drive and had to download them through a browser and scp to Unity. 

## Specificity
Another one for specificity (let me know if there is a better way to do this!)
```
conda create --name profiler_specificity_env python=3.7.3
conda deactivate
conda activate profiler_specificity_env
python -m pip install -r Domain-Agnostic-Sentence-Specificity-Prediction/requirements.txt
wget https://nlp.stanford.edu/data/glove.840B.300d.zip
unzip glove.840B.300d.zip
rm glove.840B.300d.zip
mv glove.840B.300d.txt Domain-Agnostic-Sentence-Specificity-Prediction/
```

# Featurizer
The featurize script reads all json files from a specified input directory and writes the features to corresponding json files in a specified output directory.

Input file format:
```
{
  "text_identifier_1": "text_1",
  "text_identifier_2": "text_2",
  ...
  "text_identifier_n": "text_n"
}
```

Then run 
```
python featurize.py -i [input directory] -o [output directory]
```


Output file format:
```
{
  "text_identifier_1": {
    "feature_1": value_1_1,
    "feature_2": value_2_1,
    ...
    "feature_n": value_n_1,
    },

  "text_identifier_2": {
    ...
    },

  ...

  "text_identifier_n": {
    ...
    }
}
```
# Converting IJCAI data

To convert an IJCAI csv file into a json input file, use the following script:

```
python format_ijcai_reviews.py -i [IJCAI csv e.g. example_reviews.csv] -o [output json file name]
```

You might want your output file to be in the directory that will be used as input to the featurizer.
