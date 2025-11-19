# HOW TO MODEL WITH THESE PKL FILES

Hello modelers! I have saved all the top 10 features that correlate to each label in the industry openings labels and the industry layoffs labels.
There are 34 labels for both openings and layoffs, so modeling may prove to be quite a task.

Use the following commands to load the pkl files into dictionaries:

with open("top_features_dict_spearman.pkl", "rb") as f:
    top_features_openings = pickle.load(f)

with open("top_features_dict_PCA.pkl", "rb") as f:
    top_features_layoffs = pickle.load(f)

Each entry in the dictionary contains a list of column names that are in the csv's in the folder data/reduced
Each dictionary contains another dictionary with the lagged correlations in them. These will be very advantageous towards forecasting trends. See model_feature_selection.ipynb for more clarity on how these look.
With this in mind, you should also load the dataframes present in that folder to access the data for modeling.
The labels for the features are in data/labels, and are csv files, load those too so that you can train the model.

If the metrics for the data don't work out in your favor (currently measured in percents), you can pull them from the jolts_counts_seasonally_adjusted.csv file or the jolts_counts_not_seasonally_adjusted.csv file, whichever one you think is best (consult Chat GPT or something to figure that out)
You may have to look at the column names and define a regex to pull the matching columns, but it shouldn't be too hard of a task. If it is, reach out to me and I will help.

Thank you for your support with this modeling process!
- Sameer Sethuram