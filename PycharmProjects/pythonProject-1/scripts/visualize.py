from pathlib import Path
import json
from collections import Counter
import matplotlib.pyplot as plt

TOK_FILE = Path("data/albums_tokens_filtered/albums_tokens_filtered.json")

with TOK_FILE.open("r", encoding="utf-8") as f:
    records = json.load(f)

def get_period(year: str) -> str:
    y = int(year)
    if 2016 <= y <= 2018:
        return "2016–2018"
    elif 2019 <= y <= 2021:
        return "2019–2021"
    elif 2022 <= y <= 2025:
        return "2022–2025"
    return "Unknown"


all_tokens = [tok for r in records for tok in r.get("tokens", [])]
cnt_all = Counter(all_tokens)

words100, freqs100 = zip(*cnt_all.most_common(100))

plt.figure(figsize=(16, 7))
plt.bar(words100, freqs100, color="darkslateblue")
plt.xticks(rotation=75, ha="right")
plt.ylabel("Частота")
plt.title("Топ-100 самых частотных слов")
plt.tight_layout()
plt.show()


period_tokens = {"2016–2018": [], "2019–2021": [], "2022–2025": []}
for r in records:
    period = get_period(r.get("year", "0"))
    if period in period_tokens:
        period_tokens[period].extend(r.get("tokens", []))


for period, tokens in period_tokens.items():
    counter = Counter(tokens)
    top30 = counter.most_common(30)
    words30, freqs30 = zip(*top30)

    plt.figure(figsize=(14, 6))
    plt.bar(words30, freqs30, color="teal")
    plt.xticks(rotation=75, ha="right")
    plt.ylabel("Частота")
    plt.title(f" Топ-30 слов за период {period}")
    plt.tight_layout()
    plt.show()