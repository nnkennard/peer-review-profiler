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
    "review_sentences": ["This is the first review.", "This is the second sentence of the first review."],
    "review_id": "review_id_1",
    "score": 1.0,
  },
  {
    "review_text": "This is the second review.",
    "review_sentences": ["This is the second review.", "This is the second sentence of the second review."],
    "review_id": "review_id_2",
    "score": 3.5,
  },
]
```

The `tokenized_review_text` field is optional. If not supplied, the sentences in review_text are separated using NLTK.
The value of the `score` field should be a float value from the set {0.0, 0.5, 1.0, ... , 5.0}.

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