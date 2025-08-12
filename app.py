import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
import json
import re
from collections import Counter
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# page config
st.set_page_config(
    page_title="the secret of us deep dive",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# custom CSS for better styling with album colors
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #87CEEB, #F0E68C, #DDA0DD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-transform: lowercase;
    }
    .metric-card {
        background: linear-gradient(135deg, #87CEEB 0%, #F0E68C 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        text-transform: lowercase;
    }
    .insight-box {
        background: linear-gradient(135deg, #F0E68C 0%, #DDA0DD 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-transform: lowercase;
    }
    .album-title {
        color: #87CEEB;
        text-transform: lowercase;
    }
    .section-header {
        color: #F0E68C;
        text-transform: lowercase;
    }
    .sub-header {
        color: #DDA0DD;
        text-transform: lowercase;
    }
</style>
""",
    unsafe_allow_html=True,
)

# load album data
with open("Lyrics_TheSecretofUs.json", "r") as file:
    album_data = json.load(file)

# extract lyrics and song titles
lyrics_data = []
for track in album_data["tracks"]:
    song = track["song"]
    lyrics_data.append({"title": song["title"], "lyrics": song["lyrics"]})

# create DataFrame
df = pd.DataFrame(lyrics_data)


def analyze_lyrics(lyrics):
    blob = TextBlob(lyrics)

    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    words = re.findall(r"\b\w+\b", lyrics.lower())
    word_count = len(words)

    unique_words = len(set(words))
    vocabulary_richness = unique_words / word_count if word_count > 0 else 0

    sentences = blob.sentences
    sentiment_variance = (
        np.var([s.sentiment.polarity for s in sentences]) if len(sentences) > 1 else 0
    )

    word_freq = Counter(words)
    most_common_word = word_freq.most_common(1)[0][0] if word_freq else ""
    repetition_score = word_freq.most_common(1)[0][1] / word_count if word_freq else 0

    return {
        "sentiment": sentiment,
        "subjectivity": subjectivity,
        "word_count": word_count,
        "unique_words": unique_words,
        "vocabulary_richness": vocabulary_richness,
        "sentiment_variance": sentiment_variance,
        "repetition_score": repetition_score,
        "most_common_word": most_common_word,
    }


analysis_results = df["lyrics"].apply(analyze_lyrics)
for key in analysis_results.iloc[0].keys():
    df[key] = analysis_results.apply(lambda x: x[key])

# sidebar: song selector
st.sidebar.header("🎵 Song Explorer")
song_titles = df["title"].tolist()
selected_song = st.sidebar.selectbox("Choose a song to explore", song_titles)

# main header
st.markdown(
    '<h1 class="main-header">🎵 the secret of us: deep dive analysis</h1>',
    unsafe_allow_html=True,
)

# album info with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(album_data["cover_art_url"], width=300)
    st.markdown(
        f"<h3 class='album-title' style='text-align: center;'>{album_data['full_title'].lower()}</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center; text-transform: lowercase;'><strong>release date:</strong> {album_data['release_date_for_display'].lower()}</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center; text-transform: lowercase;'><strong>artist:</strong> {album_data['artist']['name'].lower()}</p>",
        unsafe_allow_html=True,
    )

# creative insights section
st.markdown("---")
st.markdown(
    '<h2 class="section-header">🔍 **creative insights & patterns**</h2>',
    unsafe_allow_html=True,
)

# emotional journey visualization
st.markdown(
    '<h3 class="sub-header">**emotional journey through the album**</h3>',
    unsafe_allow_html=True,
)
fig_journey = go.Figure()

# create emotional journey line
fig_journey.add_trace(
    go.Scatter(
        x=df.index,
        y=df["sentiment"],
        mode="lines+markers",
        name="Emotional Arc",
        line=dict(color="#FF6B6B", width=3),
        marker=dict(size=10, color=df["sentiment"], colorscale="RdBu", showscale=True),
    )
)

fig_journey.update_layout(
    title="the emotional rollercoaster of 'the secret of us'",
    xaxis_title="track order",
    yaxis_title="sentiment score",
    height=400,
    showlegend=False,
)

# Add annotations for peaks and valleys
for i, (title, sentiment) in enumerate(zip(df["title"], df["sentiment"])):
    if sentiment == df["sentiment"].max() or sentiment == df["sentiment"].min():
        fig_journey.add_annotation(
            x=i,
            y=sentiment,
            text=title[:15] + "..." if len(title) > 15 else title,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636EFA",
        )

st.plotly_chart(fig_journey, use_container_width=True)

# Word cloud for the entire album
st.markdown(
    '<h3 class="sub-header">☁️ **album word cloud**</h3>', unsafe_allow_html=True
)
all_lyrics = " ".join(df["lyrics"].tolist())
words = re.findall(r"\b\w+\b", all_lyrics.lower())
word_freq = Counter(words)

# Filter out common words
common_words = {
    "the",
    "and",
    "i",
    "you",
    "to",
    "a",
    "of",
    "in",
    "that",
    "it",
    "is",
    "was",
    "for",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "they",
    "we",
    "say",
    "her",
    "she",
    "or",
    "an",
    "will",
    "my",
    "one",
    "all",
    "would",
    "there",
    "their",
    "what",
    "so",
    "up",
    "out",
    "if",
    "about",
    "who",
    "get",
    "which",
    "go",
    "me",
    "when",
    "make",
    "can",
    "like",
    "time",
    "no",
    "just",
    "him",
    "know",
    "take",
    "people",
    "into",
    "year",
    "your",
    "good",
    "some",
    "could",
    "them",
    "see",
    "other",
    "than",
    "then",
    "now",
    "look",
    "only",
    "come",
    "its",
    "over",
    "think",
    "also",
    "back",
    "after",
    "use",
    "two",
    "how",
    "our",
    "work",
    "first",
    "well",
    "way",
    "even",
    "new",
    "want",
    "because",
    "any",
    "these",
    "give",
    "day",
    "most",
    "us",
}
filtered_words = {
    word: count
    for word, count in word_freq.items()
    if word not in common_words and len(word) > 2
}

if filtered_words:
    fig, ax = plt.subplots(figsize=(12, 8))
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="viridis",
        max_words=100,
    ).generate_from_frequencies(filtered_words)

    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# Lyrical complexity analysis
st.markdown(
    '<h3 class="sub-header">🧠 **lyrical complexity analysis**</h3>',
    unsafe_allow_html=True,
)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("vocabulary richness", f"{df['vocabulary_richness'].mean():.2f}")
with col2:
    st.metric("repetition score", f"{df['repetition_score'].mean():.2f}")
with col3:
    st.metric("emotional variance", f"{df['sentiment_variance'].mean():.3f}")
with col4:
    st.metric("avg words per song", f"{df['word_count'].mean():.0f}")

# Song comparison radar chart
st.markdown(
    '<h3 class="sub-header">**song comparison radar**</h3>', unsafe_allow_html=True
)
selected_songs = st.multiselect(
    "select songs to compare", df["title"].tolist(), default=df["title"].tolist()[:3]
)

if selected_songs:
    fig_radar = go.Figure()

    for song in selected_songs:
        song_data = df[df["title"] == song].iloc[0]
        fig_radar.add_trace(
            go.Scatterpolar(
                r=[
                    song_data["sentiment"],
                    song_data["subjectivity"],
                    song_data["vocabulary_richness"],
                    song_data["repetition_score"],
                    song_data["sentiment_variance"],
                ],
                theta=[
                    "Sentiment",
                    "Subjectivity",
                    "Vocabulary",
                    "Repetition",
                    "Emotional Variance",
                ],
                fill="toself",
                name=song,
            )
        )

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="multi-dimensional song comparison",
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Selected song deep dive
st.markdown("---")
st.markdown(
    f'<h2 class="section-header">🎵 **deep dive: {selected_song.lower()}**</h2>',
    unsafe_allow_html=True,
)

song_row = df[df["title"] == selected_song].iloc[0]

# Song metrics in styled cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
    <div class="metric-card">
        <h3>word count</h3>
        <h2>{song_row["word_count"]}</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )
with col2:
    sentiment_color = "#87CEEB" if song_row["sentiment"] < 0 else "#F0E68C"
    st.markdown(
        f"""
    <div class="metric-card">
        <h3>sentiment</h3>
        <h2 style="color: {sentiment_color}">{song_row["sentiment"]:.2f}</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""
    <div class="metric-card">
        <h3>subjectivity</h3>
        <h2>{song_row["subjectivity"]:.2f}</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"""
    <div class="metric-card">
        <h3>vocabulary</h3>
        <h2>{song_row["vocabulary_richness"]:.2f}</h2>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Creative insights for selected song
st.markdown('<h3 class="sub-header">**song insights**</h3>', unsafe_allow_html=True)
insights = []
if song_row["sentiment"] > 0.3:
    insights.append("this song has a notably positive emotional tone")
elif song_row["sentiment"] < -0.3:
    insights.append("this song carries heavy emotional weight")
else:
    insights.append("this song maintains emotional balance")

if song_row["subjectivity"] > 0.7:
    insights.append("highly personal and subjective lyrics")
elif song_row["subjectivity"] < 0.3:
    insights.append("more objective and narrative-driven")

if song_row["repetition_score"] > 0.1:
    insights.append("uses repetition as a lyrical device")
if song_row["vocabulary_richness"] > 0.6:
    insights.append("rich and diverse vocabulary")
if song_row["sentiment_variance"] > 0.1:
    insights.append("emotional intensity varies throughout")

for insight in insights:
    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

# Lyrics display
st.markdown('<h3 class="sub-header">**full lyrics**</h3>', unsafe_allow_html=True)
st.text_area("Lyrics", song_row["lyrics"], height=300, key="lyrics_display")

# Album-wide patterns
st.markdown("---")
st.markdown(
    '<h2 class="section-header">**album-wide patterns**</h2>', unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    # Sentiment distribution
    fig_sent_dist = px.histogram(
        df,
        x="sentiment",
        nbins=10,
        title="sentiment distribution across album",
        color_discrete_sequence=["#87CEEB"],
    )
    st.plotly_chart(fig_sent_dist, use_container_width=True)

with col2:
    # Subjectivity vs Sentiment scatter
    fig_scatter = px.scatter(
        df,
        x="sentiment",
        y="subjectivity",
        text="title",
        size="word_count",
        title="sentiment vs subjectivity",
        color="sentiment_variance",
        color_continuous_scale="Viridis",
    )
    fig_scatter.update_traces(textposition="top center")
    st.plotly_chart(fig_scatter, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666;'>
    <p>made with ❤️</p>
    <p>deep dive analysis of Gracie Abrams' The Secret of Us album</p>
</div>
""",
    unsafe_allow_html=True,
)
