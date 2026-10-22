import pandas as pd

df = pd.read_csv("data/raw/glovo_reviews_raw.csv", keep_default_na=False)
text = df["content"].str.strip()

print("empty:", (text == "").sum())
print(df.loc[text == "", ["score", "content"]])

df["n_chars"] = text.str.len()
print("under 4 chars:", (df["n_chars"] < 4).sum())
print(text[df["n_chars"] < 4].value_counts().head(15))

has_arabic = text.str.contains(r"[\u0600-\u06FF]", regex=True)
print("arabic script share:", has_arabic.mean())

print("duplicate texts:", text.duplicated().sum())
print(text.str.lower().value_counts().head(10))

df["at"] = pd.to_datetime(df["at"])
print(df.groupby(df["at"].dt.year)["score"].agg(["count", "mean"]))