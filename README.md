# VibeCheck.ai 🔪

*5 questions. 1 song. no mercy.*

A Gen Z playlist recommender built with Python + Streamlit. Answer 5 unhinged questions about your mood, texting habits, and 3am behavior → get your one perfect song match via cosine similarity, plus a personalized AI roast explaining exactly why it fits.

Built on 3hrs of sleep & spite by khushi ☕

---

## what's actually happening (the DS part)

1. **Tag vectorization** — each quiz answer maps to a vibe tag (20 possible tags total: `villain`, `healing`, `down_bad`, `chaotic`, `gremlin`, etc). User answers become a binary vector across all 20 tags.
2. **Cosine similarity** — the user vector is compared against every song's tag vector in a 67-song database spanning 10 genres. Closest match wins.
3. **LLM layer** — Groq (Llama 3 70B) generates a personalized roast explaining why that song fits, referencing the user's specific tags, plus a 2-line "vibe horoscope" forecast based on your dominant tag across past quiz attempts.

This is a simplified version of how real recommendation systems work (Spotify, Netflix, etc.) — just without collaborative filtering or user history at scale.

## features

**Core experience**
- 🖱️ **Pink sparkle cursor trail** — Y2K-style canvas particle trail (stars + circles) that follows your cursor, theme-aware colors for dark/light mode
- 🎵 **Song title bounce** — animated bounce on your result reveal
- 🌸 **Soft Girl Mode** — full dark/light theme toggle with distinct color palettes for each, including a separately re-themed sidebar
- 🏆 **Rare Vibe Badges** — 10 special tag-combo badges (e.g. "Chaotic Visionary," "Secretly Unhinged") with rarity stats, awarded for specific tag combinations
- 🔮 **Vibe Horoscope** — AI-generated 2-line daily forecast based on your most frequent vibe tag across quiz history, with hardcoded fallbacks if the API call fails
- 🎧 **Genre-matched ambient audio** — hovering a genre card previews a short ambient track before you commit
- 😒 **Retry roasts** — escalating sarcastic commentary if you retake the quiz

**Sidebar (right column)**
- 📅 **Vibe of the Day** — a 28-slot grid (7 days × 4 time-of-day windows) surfacing a different curated song depending on when you visit, with a direct YouTube search link
- 📼 **Vibe history** — last 30 quiz results persisted locally, showing your 6 most recent with date, song, and vibe
- 🔥 **Weekly streak tracker** — visual chip row showing which days in the past week you've taken the quiz
- 🔍 **Personality breakdown** — your top 4 most frequent vibe tags across history, converted into named "types" (e.g. "The Main Character," "Chaotic Neutral") with percentage bars

**Left column**
- 🆕 **"What's New" panel** — postcard-style callouts introducing the sparkle trail, song bounce, soft girl mode, rare badges, and vibe horoscope to first-time visitors

**Infra**
- 👁️ **Live view counter** — persistent visit count, with a fixed offset added to account for views from before the current deploy
- 📊 **Optional Google Analytics 4** — wired in via `GA_MEASUREMENT_ID` env var; does nothing if unset

## setup

```bash
# 1. clone / download the folder

# 2. install dependencies
pip install -r requirements.txt

# 3. set your API key
export GROQ_API_KEY=your_key_here
# on Windows: set GROQ_API_KEY=your_key_here

# optional — enables Google Analytics 4 tracking if set
export GA_MEASUREMENT_ID=G-XXXXXXXXXX

# 4. run
streamlit run app.py
```

App opens at http://localhost:8501

## files

```
playlist_fixer/
├── app.py           # main Streamlit UI, theming, quiz flow, all features
├── recommender.py   # cosine similarity engine
├── songs_db.py      # song database — 67 songs, 10 genres, tagged
├── requirements.txt
└── README.md
```

## how to extend this

- **add more songs** to `songs_db.py` — the recommender scales automatically
- **replace tag vectors with real embeddings** — swap `vectorize_tags()` in `recommender.py` with `sentence-transformers` embeddings for richer matching
- **move history/view-count storage off local JSON** — `.vibe_history.json` and `.view_count.json` are local files and won't persist properly across redeploys or multiple instances; swap for a real DB (SQLite, Supabase, etc.) for production
- **add real collaborative filtering** — the personality breakdown and horoscope currently run on simple tag-frequency counts; a proper user-history model could replace this
- **RAG pipeline** — give the LLM the full song database as context instead of just the top match, for richer roast generation

## Built By

Soumya Thamke — [GitHub](https://github.com/soumyathamke) | [Kaggle](https://www.kaggle.com/soumyathamke)
