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
