import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import emoji
import random

# Set page config with a cute emoji
st.set_page_config(page_title="Text Sentiment Analysis", page_icon="🌸", layout="wide")

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #FFB6C1;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF69B4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Sentiment Analyzer 🌸")

with st.sidebar:
    st.header("About")
    st.write("This app helps you analyze the sentiment of your text!")

# Main content
st.write("### Enter your text below to analyze its sentiment!")

user_input = st.text_area(
    "Type your message here...", placeholder="💭 What's on your mind?"
)

if user_input:
    # Analyze sentiment
    analysis = TextBlob(user_input)
    sentiment_score = analysis.sentiment.polarity

    # Create cute emoji based on sentiment
    if sentiment_score > 0.3:
        emoji_face = "😊"
    elif sentiment_score < -0.3:
        emoji_face = "😢"
    else:
        emoji_face = "😐"

    # Display results in cute containers
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Sentiment Score", f"{sentiment_score:.2f}", emoji_face)

    with col2:
        st.metric("Subjectivity", f"{analysis.sentiment.subjectivity:.2f}", "🎯")

    with col3:
        st.metric("Word Count", len(user_input.split()), "📝")

    # Create cute visualization
    sentiment_data = pd.DataFrame(
        {
            "Metric": ["Positive", "Neutral", "Negative"],
            "Value": [
                max(0, sentiment_score),
                1 - abs(sentiment_score),
                max(0, -sentiment_score),
            ],
        }
    )

    fig = px.bar(
        sentiment_data,
        x="Metric",
        y="Value",
        color="Metric",
        color_discrete_sequence=["#FFB6C1", "#FFC0CB", "#FF69B4"],
    )

    fig.update_layout(
        title="✨ Sentiment Breakdown ✨",
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.markdown("Made with 💖")
