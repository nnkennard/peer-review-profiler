# 696-review-discourse

## Setup

```
bash setup.sh
```

This does the following steps:
1. Set up a virtualenv and install necessary packages
2. Download models and relocate appropriately
3. Set up submodules for specificity and aspect

## Generating features

This requires an input json file with the format:

```
[
  {
    "review_text": "This is the first review.",
    "review_id": "review_id_1"
  },
  {
    "review_text": "This is the second review.",
    "review_id": "review_id_2"
  },
]
```


```
bash run_feature_pipeline.sh -i [input_json_file] -r [run_name]
```

Name the run something that will indicate which input json file was used. The generated features will be found in a `[run_name]/final_features.json`.

## Feature pipeline

## Analysis
TODO: this part
