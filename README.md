This was tested on Unity.

# Setup
Create a conda environment with requirements:
```
conda create --name profiler_env python=3.9
conda activate profiler_env
python -m pip install -r requirements.txt
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
