import pandas as pd

df = pd.read_csv("data/raw/glovo_reviews_raw.csv")

print(df.shape)
print(df.dtypes)
print(df.isna().sum())
print(df["score"].value_counts(normalize=True).sort_index())
print(df["content"].str.len().describe())
print(df["at"].min(), df["at"].max())
print(df["content"].sample(15, random_state=1).to_string())