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
    "review_text": "This is the first review. This is the second sentence of the first review.",
    "tokenized_review_text": ["This is the first review.", "This is the second sentence of the first review."],
    "review_id": "review_id_1"
  },
  {
    "review_text": "This is the second review.",
    "tokenized_review_text": ["This is the second review.", "This is the second sentence of the second review."],
    "review_id": "review_id_2"
  },
]
```


## Analysis
This requires an input json file with the format:

```
[
  {
    "review_id": "review_id_1",
    "gold_annotations": {
      "overall": 5,
      "any_other_score_type": 5,
    }
  },
  {
    "review_id": "review_id_2",
    "gold_annotations": {
      "overall": 5,
      "any_other_score_type": 5,
    }
  },
]
```


## Feature pipeline

```
bash run_feature_pipeline.sh -i [input_json_file] -r [run_name]
```

Name the run something that will help identify which input json file was used. The generated features will be found in a `[run_name]/final_features.json`.

The generated correlation scores between features and review quality will be found in `[run_name]/correlations.json`.

Heatmaps to interpret feature importance will be found in `[run_name]/plots/`.
