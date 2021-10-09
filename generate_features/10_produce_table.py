import argparse
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

parser = argparse.ArgumentParser(
    description='Produce a table of significant correlations')

parser.add_argument(
    '-d',
    '--run_directory',
    type=str,
    help='path to run directory that contains correlations file')


def main():
  args = parser.parse_args()
  correlation_file = args.run_directory + "/correlations.json"

  with open(correlation_file, 'r') as f:
    correlations = json.load(f)
  pd.set_option('display.max_columns', None)
  
  df_dicts = []
  num_features = len(correlations)
  for feature_name, corr_values in correlations.items():
    p_value = corr_values['p-value']
    if math.isnan(p_value) or p_value > 0.05:
      continue
    df_dicts.append({
        "feature": feature_name,
        "correlation": corr_values['correlation'],
        "p_value": p_value,
        "significant_with_correction": p_value < 0.05 / num_features,
    })

  df = pd.DataFrame.from_dict(df_dicts).sort_values(by="correlation",
                                                    ascending=False,
                                                    key=abs)
  with open(args.run_directory + "/result.txt", 'w') as f:
    f.write("Summary of results for run: " + os.path.basename(
      os.path.normpath(args.run_directory)) + "\n\n" + str(df) + "\n")


if __name__ == "__main__":
  main()
