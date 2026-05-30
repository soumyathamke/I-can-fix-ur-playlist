# I-can-fix-ur-playlist
GenZ AI music recommendation web app — built a custom cosine similarity recommendation engine backed by an LLM API for personalised song matching.

# 🔪 VibeCheck.ai — i can fix ur playlist

https://vibecheckzip--khush786.replit.app/

A GenZ-flavoured AI music recommendation web app that analyses your personality through 5 unhinged quiz questions and recommends the perfect song — powered by a custom cosine similarity recommendation engine and the Groq LLM API.

---

## What It Does

1. User picks a genre (optional) and answers 5 personality-based quiz questions
2. Answers are converted into personality **tags** (e.g. `villain_era`, `down_bad`, `dreamer`)
3. A **cosine similarity algorithm** (NumPy) matches the user's tag vector against a curated song database
4. The **Groq LLM API** generates a personalised, sassy explanation of why that song matches them
5. Result flashes on screen with background audio matching the user's mood

---

## Tech Stack

- **Python** — core backend logic
- **Streamlit** — interactive web frontend
- **NumPy** — vector-based cosine similarity for recommendation engine
- **Groq API** — LLM integration for personalised song explanations (LLM inference)
- **REST API** (requests) — external API calls for audio and LLM responses
- **Custom song database** — 50+ songs tagged by mood, energy, valence, and genre

---

## How the Recommendation Engine Works

Each song in the database has a set of **mood tags** (e.g. `main_character`, `healing`, `villain`).

When the user answers the quiz, their answers map to personality tags. These are **vectorised** using one-hot encoding:

```python
def vectorize_tags(tags: list[str]) -> np.ndarray:
    vec = np.zeros(len(ALL_TAGS))
    for tag in tags:
        if tag in TAG_INDEX:
            vec[TAG_INDEX[tag]] = 1.0
    return vec
```

**Cosine similarity** is then computed between the user vector and each song vector:

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

The top-scoring song is returned. If a genre filter is applied, it filters first then falls back to all songs if no match is found.

---

## Project Structure

```
playlist_fixer/
├── app.py              # Streamlit frontend + UI logic (661 lines)
├── recommender.py      # Cosine similarity recommendation engine
├── songs_db.py         # Curated song database with mood tags
└── requirements.txt    # Dependencies
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Groq API key
export GROQ_API_KEY=your_key_here

# 3. Run the app
streamlit run app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## Features

- 5 personality quiz questions with GenZ-style answer options
- Genre filter (Pop, Hip-Hop, R&B, Indie, Electronic, Rock, Latin, K-Pop, Afrobeats, Sad Girl)
- Background audio per genre and mood
- LLM-generated personalised roast/explanation of song match
- Dark → light UI transition as quiz progresses
- Judgy rotating restart messages

---

## Built By

Soumya Thamke — [GitHub](https://github.com/soumyathamke) | [Kaggle](https://www.kaggle.com/soumyathamke)
