import pandas as pd

df = pd.read_csv("data/raw/glovo_reviews_raw.csv", keep_default_na=False)

df = df.drop(columns=["userName", "appVersion"])
df["content"] = df["content"].str.strip()
df["at"] = pd.to_datetime(df["at"])

df["high_satisfaction"] = (df["score"] >= 4).astype(int)
df["n_chars"] = df["content"].str.len()
df["n_words"] = df["content"].str.split().str.len()
df["has_arabic"] = df["content"].str.contains(r"[\u0600-\u06FF]", regex=True)
df["text_norm"] = df["content"].str.lower()
df["is_repeated_text"] = df["text_norm"].duplicated(keep=False)

df = df.sort_values("at").reset_index(drop=True)
df.to_csv("data/clean/glovo_reviews_clean.csv", index=False, encoding="utf-8-sig")

print(df.shape)
print(df["high_satisfaction"].value_counts(normalize=True))
print("null-like texts kept:", df["text_norm"].isin(["null", "nul", "none"]).sum())