import re
import pandas as pd

df = pd.read_csv("data/clean/glovo_reviews_clean.csv", keep_default_na=False)

pattern = re.compile(r"\b(?=\w*[a-z])(?=\w*[2356789])\w+\b")
false_pos = re.compile(r"^\d+(h|min|mn|g|eme|ème|e|er|ère|dt|d|k|m|kg|ml|cl)$")

def arabizi_hits(t):
    return [w for w in pattern.findall(t) if not false_pos.match(w)]

df["hits"] = df["text_norm"].apply(arabizi_hits)
df["maybe_arabizi"] = df["hits"].apply(len) > 0

print("share with a letter+digit word:", df["maybe_arabizi"].mean())
print(df.groupby("maybe_arabizi")["high_satisfaction"].agg(["mean", "count"]))

sample = df[df["maybe_arabizi"]].sample(20, random_state=1)
for _, row in sample.iterrows():
    print(row["hits"], "|", row["content"][:70].replace("\n", " "))