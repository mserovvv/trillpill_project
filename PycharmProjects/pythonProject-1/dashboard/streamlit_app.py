import json
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# --- вспомогательные функции ---
def load_data(path: Path) -> pd.DataFrame:
    records = json.loads(path.read_text("utf-8"))
    df = pd.json_normalize(records)
    return df

def get_period(year: int) -> str:
    if 2016 <= year <= 2018:
        return "2016–2018"
    elif 2019 <= year <= 2021:
        return "2019–2021"
    elif 2022 <= year <= 2025:
        return "2022–2025"
    return "Unknown"

def plot_bar(words, freqs, title, figsize=(10, 5), color="teal"):
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(words, freqs, color=color)
    ax.set_title(title)
    ax.set_ylabel("Частота")
    ax.set_xticklabels(words, rotation=75, ha="right")
    st.pyplot(fig)

def plot_wordcloud(tokens, title):
    wc = WordCloud(
        width=800, height=400,
        background_color="white",
        collocations=False
    ).generate(" ".join(tokens))
    st.subheader(title)
    st.image(wc.to_array(), use_column_width=True)

# --- main ---
st.title("Thrill Pill Lyrics Dashboard")

DATA_PATH = Path("data/albums_tokens_filtered/albums_tokens_filtered.json")
df = load_data(DATA_PATH)

# привязываем периоды
df["year"] = df["year"].astype(int)
df["period"] = df["year"].apply(get_period)

# Sidebar
st.sidebar.header("Настройки")
periods = ["Все", "2016–2018", "2019–2021", "2022–2025"]
sel_period = st.sidebar.selectbox("Период", periods)

# фильтрация
if sel_period != "Все":
    df = df[df["period"] == sel_period]

# объединяем все токены
all_tokens = df.explode("tokens")["tokens"].dropna().tolist()
counter = Counter(all_tokens)

# Топ-100
st.subheader("Топ-100 слов"+(f" за период {sel_period}" if sel_period!="Все" else ""))
words100, freqs100 = zip(*counter.most_common(100))
plot_bar(words100, freqs100, f"Топ-100 самых частотных слов ({sel_period})", figsize=(16,6), color="darkslateblue")

# Топ-30
st.subheader("Топ-30 слов"+(f" за период {sel_period}" if sel_period!="Все" else ""))
words30, freqs30 = zip(*counter.most_common(30))
plot_bar(words30, freqs30, f"Топ-30 слов ({sel_period})", figsize=(14,5))

# WordCloud
plot_wordcloud(all_tokens, "Словарное облако")

# Сводка
st.markdown("---")
st.markdown(f"**Всего треков:** {df['title'].nunique()}  ")
st.markdown(f"**Всех токенов:** {len(all_tokens)}  ")
