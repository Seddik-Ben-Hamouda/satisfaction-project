import os
import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

df = pd.read_csv("data/clean/glovo_reviews_clean.csv", keep_default_na=False)
df["at"] = pd.to_datetime(df["at"])
df["has_arabic"] = df["has_arabic"].astype(str).eq("True")

# Chart 1: distribution of stars
counts = df["score"].value_counts().sort_index()
colors = ["#c0392b"] * 3 + ["#2e86c1"] * 2
plt.figure(figsize=(7, 4))
plt.bar(counts.index, counts.values, color=colors)
plt.xlabel("Stars")
plt.ylabel("Number of reviews")
plt.title("Glovo Tunisia: stars (red = not high, blue = high)")
plt.savefig("figures/01_score_distribution.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 2: volume and average score per quarter
q = df.groupby(df["at"].dt.to_period("Q"))["score"].agg(["count", "mean"])
labels = q.index.astype(str)
fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(labels, q["count"], color="#d5d8dc")
ax1.set_ylabel("Number of reviews")
ax2 = ax1.twinx()
ax2.plot(labels, q["mean"], marker="o", color="#2e86c1")
ax2.set_ylabel("Mean stars")
ax2.set_ylim(1, 5)
plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
ax1.set_title("Reviews and mean score per quarter")
plt.savefig("figures/02_trend_by_quarter.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 3: review length by stars
data = [df.loc[df["score"] == s, "n_words"] for s in range(1, 6)]
plt.figure(figsize=(7, 4))
plt.boxplot(data, showfliers=False)
plt.xticks([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
plt.xlabel("Stars")
plt.ylabel("Words per review")
plt.title("Review length by stars")
plt.savefig("figures/03_length_by_score.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 4: share of high satisfaction by script
g = df.groupby("has_arabic")["high_satisfaction"].agg(["mean", "count"])
names = ["Latin only" if not k else "Contains Arabic" for k in g.index]
plt.figure(figsize=(6, 4))
plt.bar(names, g["mean"], color=["#7f8c8d", "#2e86c1"])
for i, (m, c) in enumerate(zip(g["mean"], g["count"])):
    plt.text(i, m + 0.01, f"n={c}", ha="center")
plt.ylim(0, 1)
plt.ylabel("Share of high satisfaction (4-5 stars)")
plt.title("High satisfaction by script")
plt.savefig("figures/04_script_vs_satisfaction.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 5: most frequent words in 1-star vs 5-star reviews
STOP = {
    "les", "des", "une", "pas", "que", "qui", "est", "pour", "dans", "avec",
    "sur", "mais", "vous", "nous", "mon", "ton", "ses", "aux", "par", "plus",
    "tout", "tous", "cette", "ces", "very", "the", "and", "for", "you", "not",
    "this", "with", "have", "that", "are", "was", "application", "glovo", "app",
    "fait", "bien", "bon",
}

def top_words(texts, n=12):
    c = Counter()
    for t in texts:
        c.update(w for w in re.findall(r"[a-zà-ÿ]+", t) if len(w) > 2 and w not in STOP)
    return c.most_common(n)

low = top_words(df.loc[df["score"] == 1, "text_norm"])
high = top_words(df.loc[df["score"] == 5, "text_norm"])
print("1-star:", low)
print("5-star:", high)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, words, title, col in [
    (axes[0], low, "Top words, 1-star", "#c0392b"),
    (axes[1], high, "Top words, 5-star", "#2e86c1"),
]:
    w, n = zip(*words)
    ax.barh(w[::-1], n[::-1], color=col)
    ax.set_title(title)
plt.savefig("figures/05_top_words.png", dpi=150, bbox_inches="tight")
plt.close()

print("charts saved in figures/")