from google_play_scraper import reviews, Sort
import pandas as pd

APP_ID = "com.glovo"
LANGS = ["fr", "ar", "en"]

rows = []
for lang in LANGS:
    token = None
    while True:
        batch, token = reviews(
            APP_ID, lang=lang, country="tn",
            sort=Sort.NEWEST, count=200,
            continuation_token=token,
        )
        rows.extend(batch)
        if not batch or token is None or len(rows) > 6000:
            break

df = pd.DataFrame(rows)
df = df[["reviewId", "userName", "content", "score", "at", "thumbsUpCount", "appVersion"]]
df = df.drop_duplicates(subset="reviewId")
df.to_csv("data/raw/glovo_reviews_raw.csv", index=False, encoding="utf-8-sig")
print(len(df), "reviews saved")