# 696-review-discourse

## Setup

```
bash setup.sh
```

This does the following steps:
1. Set up a virtualenv and install necessary packages
2. Download models and relocate appropriately
3. Set up submodules for specificity and aspect

## Running analysis

This requires an input json file with the format:

```
[
  {
    "review_text": "This is the first review. This is the second sentence of the first review.",
    "review_id": "review_id_1",
    "score": 1.0,
  },
  {
    "review_text": "This is the second review.",
    "review_id": "review_id_2",
    "score": 3.5,
  },
]
```
The value of the `score` field should be a float value from the set {1.0, 1.5, 2.0, ... , 5.0}.

Then, run:

```
bash run_feature_pipeline.sh -i [input_json_file] -r [run_name]
```

Name the run something that will help identify which input json file was used.

The following outputs are generated:

| Output             | Path |
|--------------------|------|
| Features           | `[run_name]/final_features.json`    |
| Correlation scores | `[run_name]/correlations.json`    |
| Plots              | `[run_name]/plots/*`    |


# Notes
* To run on `gypsum.cs.umass.edu`, please request a 1080ti node; other nodes have compatibility issues.
* To generate plots with the data collected for the 696DS project for comparison, use `data/final_annotated_scored.json` as the input file.
