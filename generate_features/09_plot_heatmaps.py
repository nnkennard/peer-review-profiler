import seaborn as sns
import matplotlib.pyplot as plt
import json
import argparse
import numpy as np
import math

parser = argparse.ArgumentParser(
    description='Plot the heatmaps of correlations and p-values')

parser.add_argument(
    '-d',
    '--run_directory',
    type=str,
    help='path to run directory that contains correlations file')


def get_p_corr(correlations):
  features = []
  p_values = []
  corr = []
  for feature, corr_values in correlations.items():
    if math.isnan(list(corr_values.values())[0]):
      continue

    features.append(feature)
    for k, v in corr_values.items():
      if k == 'correlation':
        corr.append(v)
      else:
        p_values.append(v)

  return features, corr, p_values


def plot_heatmap(run_directory, plot_type, features, corr, p_values):
  n = len(features)
  fig, axes = plt.subplots(1, 2, figsize=(10, n), dpi=75, sharey=True)
  fig.add_subplot(axes[0])
  sns.heatmap(
      np.array(p_values).reshape(n, 1),
      robust=True,
      center=0.00128,
      vmax=0.005,
      annot=True,
      yticklabels=features,
      xticklabels=['overall'],
      linewidths=1,
      cbar=False,
  )
  plt.gca().set_title("p-values")

  fig.add_subplot(axes[1])
  sns.heatmap(
      np.array(corr).reshape(n, 1),
      robust=True,
      annot=True,
      center=0,
      vmax=1,
      vmin=-1,
      yticklabels=features,
      xticklabels=['overall'],
      linewidths=1,
  )
  plt.gca().set_title("Correlation")

  filename = "".join([run_directory, "/plots/", plot_type, ".pdf"])

  plt.savefig(filename, bbox_inches='tight')


def get_significant_features(method, features, corr, p_values):
  sig_features = []
  sig_corr = []
  sig_p_values = []
  for i in range(len(p_values)):
    if method == 'normal' and p_values[i] < 0.05:
      sig_features.append(features[i])
      sig_corr.append(corr[i])
      sig_p_values.append(p_values[i])
    elif method == 'correction' and p_values[i] < (0.05 / len(features)):
      sig_features.append(features[i])
      sig_corr.append(corr[i])
      sig_p_values.append(p_values[i])

  return sig_features, sig_corr, sig_p_values


def main():
  args = parser.parse_args()
  correlation_file = args.run_directory + "/correlations.json"

  with open(correlation_file, 'r') as f:
    correlations = json.load(f)

  features, corr, p_values = get_p_corr(correlations)

  # Plot the heatmap for significant features (p < 0.05)
  sig_features, sig_corr, sig_p_values = get_significant_features(
      'normal', features, corr, p_values)
  plot_heatmap(args.run_directory, 'significant_feature', sig_features,
               sig_corr, sig_p_values)

  # Plot the heatmap for significant features (with Bonferroni Correction)
  sig_features_correction, sig_corr_correction, sig_p_values_correction = get_significant_features(
      'correction', features, corr, p_values)
  plot_heatmap(args.run_directory, 'significant_feature_after_correction',
               sig_features_correction, sig_corr_correction,
               sig_p_values_correction)


if __name__ == "__main__":
  main()
