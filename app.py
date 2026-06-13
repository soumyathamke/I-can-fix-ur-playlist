import streamlit as st
import streamlit.components.v1 as components
import os, json, datetime, random, html as html_lib
from groq import Groq
from recommender import recommend, get_top_match

st.set_page_config(page_title="VibeCheck.ai", page_icon="🔪", layout="wide")

ACCENT      = "#ff2d78"
ACCENT_GLOW = "rgba(255,45,120,0.25)"
ACCENT_DIM  = "rgba(255,45,120,0.12)"
ACCENT_MID  = "rgba(255,45,120,0.45)"

# ── Rare vibe badge combos ──────────────────────────────────────
RARE_COMBOS = {
    frozenset(["villain", "dreamer"]): ("Chaotic Visionary", "only 2% of people get this", "🌌"),
    frozenset(["healthy", "villain"]): ("Psychologically Unstable Icon", "only 1% get this combo", "⚡"),
    frozenset(["healing", "gremlin"]): ("Soft Gremlin Era", "only 3% of people get this", "🌸"),
    frozenset(["aloof", "oversharer"]): ("Contradictory Queen", "only 1.5% match this energy", "🫥"),
    frozenset(["obsessive", "unbothered"]): ("Secretly Unhinged", "top 2% rarest vibe", "👁️"),
    frozenset(["unhinged_creative", "healthy"]): ("Functional Disaster", "only 4% get this", "🎤"),
    frozenset(["main_character", "rotting"]): ("Glamorous Disaster", "only 3% of users get this", "💅"),
    frozenset(["chaotic", "curated"]): ("Controlled Chaos Era", "only 2% vibe like this", "🌪️"),
    frozenset(["down_bad", "dreamer"]): ("Romantic Wreck", "only 3% of people get this", "💀"),
    frozenset(["emotional", "hype_energy"]): ("Crying While Raging", "top 2% most complex energy", "🔥"),
}

def get_rare_badge(tags):
    tag_set = frozenset(tags)
    for combo, badge in RARE_COMBOS.items():
        if combo.issubset(tag_set):
            return badge
    return None

# ── Vibe Horoscope via Groq ─────────────────────────────────────
def generate_vibe_horoscope(dominant_tag):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = days[datetime.datetime.now().weekday()]
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        prompt = f"""Write a 2-line "vibe forecast" for someone whose dominant vibe tag is "{dominant_tag}" on a {day_name}.
Style: Gen Z, lowercase, no punctuation except maybe an ellipsis, very short, slightly cryptic but relatable.
Example format:
line 1: [observation about their energy today]
line 2: [what they should do or watch out for]
Return ONLY the 2 lines, no labels, no extra text."""
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80
        )
        return response.choices[0].message.content.strip()
    except Exception:
        fallbacks = {
            "villain": "ur villain arc is peaking rn... embrace it\neveryone will understand eventually (they won't)",
            "healing": "ur in ur soft era and that's valid\njust don't reply to that text today",
            "dreamer": "something good is brewing in ur brain\ndon't let anyone rush u out of ur head",
            "main_character": "the universe is watching ur every move today\nno pressure but also all the pressure",
        }
        return fallbacks.get(dominant_tag, "ur energy today is... a lot\njust vibe and let it happen bestie")

# ── Vibe of the Day data ────────────────────────────────────────
VOTD_MAP = {
    (0, 0): {"song": "Levitating", "artist": "Dua Lipa", "vibe": "Monday morning hypeman", "emoji": "☀️", "note": "u need this more than coffee rn"},
    (0, 1): {"song": "Money Trees", "artist": "Kendrick Lamar", "vibe": "productive daydream", "emoji": "💭", "note": "big dreams, small lunch break"},
    (0, 2): {"song": "as it was", "artist": "Harry Styles", "vibe": "monday evening decompression", "emoji": "🌆", "note": "survived another monday. barely."},
    (0, 3): {"song": "Good Days", "artist": "SZA", "vibe": "midnight healing", "emoji": "🌙", "note": "tomorrow is a new day (cope)"},
    (1, 0): {"song": "Shake It Off", "artist": "Taylor Swift", "vibe": "tuesday grind", "emoji": "💪", "note": "not the worst day of the week actually"},
    (1, 1): {"song": "Espresso", "artist": "Sabrina Carpenter", "vibe": "midday slay", "emoji": "☕", "note": "carrying yourself like a main character"},
    (1, 2): {"song": "Saturn", "artist": "SZA", "vibe": "evening feels", "emoji": "🪐", "note": "reflective but make it aesthetic"},
    (1, 3): {"song": "Moon Song", "artist": "Phoebe Bridgers", "vibe": "late night spiral", "emoji": "🌕", "note": "don't text anyone"},
    (2, 0): {"song": "Magnetic", "artist": "ILLIT", "vibe": "hump day push", "emoji": "🔋", "note": "halfway there. keep going bestie."},
    (2, 1): {"song": "Rich Flex", "artist": "Drake & 21 Savage", "vibe": "wednesday flex", "emoji": "💅", "note": "it's giving 'made it to wednesday'"},
    (2, 2): {"song": "Everywhere, Everything", "artist": "Noah Kahan", "vibe": "soft hour", "emoji": "🍂", "note": "feeling everything at once, normal"},
    (2, 3): {"song": "Bags", "artist": "Clairo", "vibe": "3am thoughts", "emoji": "💤", "note": "ok but go to sleep for real"},
    (3, 0): {"song": "Not Like Us", "artist": "Kendrick Lamar", "vibe": "thursday villain era", "emoji": "😈", "note": "one day till freedom. act accordingly."},
    (3, 1): {"song": "Flowers", "artist": "Miley Cyrus", "vibe": "self-care thursday", "emoji": "🌸", "note": "u deserve nice things"},
    (3, 2): {"song": "Kill Bill", "artist": "SZA", "vibe": "pre-weekend chaos", "emoji": "🔪", "note": "starting to spiral already? valid"},
    (3, 3): {"song": "Escapism.", "artist": "RAYE ft. 070 Shake", "vibe": "thursday night fever", "emoji": "🌙", "note": "almost there. this song will carry u"},
    (4, 0): {"song": "Cruel Summer", "artist": "Taylor Swift", "vibe": "FRIDAY MORNING", "emoji": "🎉", "note": "the law says you must be excited rn"},
    (4, 1): {"song": "Nonsense", "artist": "Sabrina Carpenter", "vibe": "friday afternoon chaos", "emoji": "🫠", "note": "productivity is canceled. it's giving friday."},
    (4, 2): {"song": "APT.", "artist": "ROSÉ & Bruno Mars", "vibe": "friday night unlocked", "emoji": "🔓", "note": "go have fun. stop reading this."},
    (4, 3): {"song": "Redlight", "artist": "Sub Focus & Dimension", "vibe": "friday midnight mode", "emoji": "🌃", "note": "main character of the night"},
    (5, 0): {"song": "How Sweet", "artist": "NewJeans", "vibe": "slow saturday morning", "emoji": "🛏️", "note": "no alarms. just vibes. u earned this."},
    (5, 1): {"song": "Water", "artist": "Tyla", "vibe": "saturday glow up", "emoji": "✨", "note": "looking good, doing nothing"},
    (5, 2): {"song": "Whiplash", "artist": "aespa", "vibe": "saturday night main character", "emoji": "💫", "note": "all eyes on u and u know it"},
    (5, 3): {"song": "Stick Season", "artist": "Noah Kahan", "vibe": "late night feelings", "emoji": "🌌", "note": "why are u still awake"},
    (6, 0): {"song": "Liability", "artist": "Lorde", "vibe": "sunday scaries", "emoji": "😰", "note": "it's giving impending doom. classic."},
    (6, 1): {"song": "Supernatural", "artist": "Gracie Abrams", "vibe": "sunday soft era", "emoji": "☁️", "note": "healing before monday hits"},
    (6, 2): {"song": "Anti-Hero", "artist": "Taylor Swift", "vibe": "sunday dread", "emoji": "🫠", "note": "it's me, hi, i'm the problem, it's me"},
    (6, 3): {"song": "Featherweight", "artist": "boygenius", "vibe": "sunday night peace", "emoji": "🕯️", "note": "breathe. you'll get through this week."},
}

def get_time_slot():
    h = datetime.datetime.now().hour
    if 5 <= h < 12:  return 0
    if 12 <= h < 17: return 1
    if 17 <= h < 22: return 2
    return 3

def get_votd():
    wd = datetime.datetime.now().weekday()
    slot = get_time_slot()
    return VOTD_MAP.get((wd, slot), VOTD_MAP[(0, 0)])

GENRE_AUDIO = {
    "no preference": "", "Pop": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "Hip-Hop": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "R&B": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "Indie": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    "Electronic": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
    "Rock": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
    "Latin": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
    "K-Pop": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
    "Afrobeats": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
    "Sad Girl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
}

QUESTIONS = [
    {"emoji": "🌡️", "text": "current mood, no cap:",
     "options": [{"label": "main character energy 💅", "tag": "main_character"},
                 {"label": "rotting in bed 🛌 send help", "tag": "rotting"},
                 {"label": "villain era, no apologies 😈", "tag": "villain"},
                 {"label": "healing era but also unwell 🌸", "tag": "healing"}]},
    {"emoji": "📱", "text": "ur situationship texts 'hey' at 2am. u:",
     "options": [{"label": "reply instantly 💀 we're cooked", "tag": "down_bad"},
                 {"label": "leave on read 3hrs then reply 😏", "tag": "unbothered"},
                 {"label": "screenshot + send to group chat first", "tag": "chaotic"},
                 {"label": "i don't have one (liar)", "tag": "in_denial"}]},
    {"emoji": "🚗", "text": "alone in the car, aux is yours. u play:",
     "options": [{"label": "one song on repeat 30x 😤", "tag": "obsessive"},
                 {"label": "full curated playlist no skips 🎧", "tag": "curated"},
                 {"label": "shuffle whatever hits 📻", "tag": "chaotic_shuffle"},
                 {"label": "voice notes to myself lol 🎤", "tag": "unhinged_creative"}]},
    {"emoji": "🌙", "text": "last thing before sleeping:",
     "options": [{"label": "doomscroll tiktok till 3am 📲", "tag": "gremlin"},
                 {"label": "journal / reflect / cry a little ✍️", "tag": "emotional"},
                 {"label": "music + stare at ceiling 🌌", "tag": "dreamer"},
                 {"label": "sleep immediately like a dog 🐶", "tag": "healthy"}]},
    {"emoji": "💬", "text": "how do u text?",
     "options": [{"label": "lowercase, no punctuation ever", "tag": "gen_z_text"},
                 {"label": "FULL CAPS when excited 🔥", "tag": "hype_energy"},
                 {"label": "walls of text, oversharer", "tag": "oversharer"},
                 {"label": "one word replies, mysterious", "tag": "aloof"}]},
]

GENRES = ["no preference", "Pop", "Hip-Hop", "R&B", "Indie", "Electronic", "Rock", "Latin", "K-Pop", "Afrobeats", "Sad Girl"]
ROASTS = [
    "oh u wanna try again? 💀 what, the first answer hurt ur feelings?",
    "trying again? ur music taste is still broken btw 🔪",
    "not u trying to escape ur own vibe 💀",
    "sir/ma'am this isn't a retry game. but ok 🙄",
    "again?? the audacity 😭 ok fine i'll fix u again",
]

VIBE_EMOJIS = {
    "main_character": "💅", "rotting": "🛌", "villain": "😈", "healing": "🌸",
    "down_bad": "💀", "unbothered": "😏", "chaotic": "🌪️", "in_denial": "🙈",
    "obsessive": "👁️", "curated": "🎧", "chaotic_shuffle": "📻", "unhinged_creative": "🎤",
    "gremlin": "📲", "emotional": "✍️", "dreamer": "🌌", "healthy": "🐶",
    "gen_z_text": "💬", "hype_energy": "🔥", "oversharer": "📖", "aloof": "🫥",
}

# ── session state ───────────────────────────────────────────────
for k, v in [
    ("step", "start"), ("answers", []), ("genre", "no preference"),
    ("result", None), ("retries", 0), ("current_q", 0), ("selected_tag", None),
    ("view_count", None), ("dark_mode", True), ("horoscope", None),
]:
    if k not in st.session_state:
        st.session_state[k] = v

_COUNTER_FILE = ".view_count.json"
def _increment_views():
    try:
        data = {"v": 0}
        if os.path.exists(_COUNTER_FILE):
            with open(_COUNTER_FILE) as f: data = json.load(f)
        data["v"] = data.get("v", 0) + 1
        with open(_COUNTER_FILE, "w") as f: json.dump(data, f)
        return data["v"]
    except Exception: return "—"

if st.session_state.view_count is None:
    st.session_state.view_count = _increment_views()

# ── Theme vars ──────────────────────────────────────────────────
if st.session_state.dark_mode:
    BG          = "#060606"
    BG2         = "rgba(255,255,255,0.03)"
    BG3         = "rgba(255,255,255,0.015)"
    BORDER      = "rgba(255,255,255,0.08)"
    BORDER2     = "rgba(255,45,120,0.18)"
    TEXT        = "#fff"
    TEXT_DIM    = "rgba(255,255,255,0.4)"
    TEXT_DIMMER = "rgba(255,255,255,0.2)"
    CARD_BG     = "rgba(255,45,120,0.04)"
    TOGGLE_LABEL = "switch to soft girl mode 🌸"
    HERO_MID    = "#fff0f5"
else:
    BG          = "#fdf0f5"
    BG2         = "rgba(255,150,190,0.08)"
    BG3         = "rgba(255,150,190,0.04)"
    BORDER      = "rgba(255,100,160,0.2)"
    BORDER2     = "rgba(255,45,120,0.25)"
    TEXT        = "#2d0a1a"
    TEXT_DIM    = "rgba(45,10,26,0.5)"
    TEXT_DIMMER = "rgba(45,10,26,0.3)"
    CARD_BG     = "rgba(255,45,120,0.06)"
    TOGGLE_LABEL = "back to dark mode 🌑"
    HERO_MID    = "#fce4ec"

# ── GLOBAL CSS ──────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background: {BG} !important;
    color: {TEXT};
    transition: background 0.4s ease, color 0.4s ease;
}}
.stApp {{ background: {BG} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── Cursor sparkle canvas ── */
#sparkle-canvas {{
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 99999;
}}

/* ── Top bar pills ── */
.mode-toggle {{
    position: fixed; top: 14px; left: 18px; z-index: 9999;
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 20px; padding: 5px 14px;
    font-size: 11px; color: {TEXT_DIM};
    display: flex; align-items: center; gap: 5px;
    backdrop-filter: blur(8px); letter-spacing: 0.02em;
    font-family: 'DM Sans', sans-serif; cursor: pointer;
    transition: all 0.3s;
}}
.eye-counter {{
    position: fixed; top: 14px; right: 18px; z-index: 9999;
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 20px; padding: 5px 11px 5px 9px;
    font-size: 12px; color: {TEXT_DIM};
    display: flex; align-items: center; gap: 5px;
    backdrop-filter: blur(8px); letter-spacing: 0.02em;
    pointer-events: none; font-family: 'DM Sans', sans-serif;
}}

/* ── HERO ── */
.hero-wrap {{
    position: relative;
    text-align: center;
    padding: 3rem 0 0.5rem;
    overflow: visible;
}}
.hero-glow-ring {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 520px; height: 420px;
    border-radius: 50%;
    background: radial-gradient(ellipse at center,
        rgba(255,45,120,0.09) 0%,
        rgba(255,45,120,0.04) 45%,
        transparent 72%);
    pointer-events: none;
    z-index: 0;
}}
.hero-glow-ring-2 {{
    position: absolute;
    top: 60%; left: 50%;
    transform: translate(-50%, -50%);
    width: 800px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(ellipse at center,
        rgba(255,45,120,0.04) 0%,
        transparent 65%);
    pointer-events: none;
    z-index: 0;
}}
.hero-noise-line {{
    position: absolute;
    top: 0; left: -10%; right: -10%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,45,120,0.5) 40%, rgba(255,45,120,0.5) 60%, transparent 100%);
    z-index: 2;
}}
.hero-title-row {{
    position: relative; z-index: 1;
    display: flex; align-items: center;
    justify-content: center; gap: 10px;
    margin-bottom: 8px;
    line-height: 1;
}}
.vibe-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(42px, 5.8vw, 82px);
    font-weight: 400;
    letter-spacing: 6px;
    line-height: 0.95;
    background: linear-gradient(
        135deg,
        #ff2d78 0%,
        #ff6ba8 25%,
        {HERO_MID} 52%,
        #ff85b3 76%,
        #ff2d78 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 60px rgba(255,45,120,0.4));
}}
.vibe-knife {{
    font-size: 46px;
    -webkit-text-fill-color: initial;
    background: none;
    filter: drop-shadow(0 0 14px rgba(255,45,120,0.35));
}}
.vibe-sub {{
    position: relative; z-index: 1;
    text-align: center;
    font-size: 10px;
    color: {TEXT_DIM};
    letter-spacing: 0.38em;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-weight: 500;
}}
.made-by {{
    position: relative; z-index: 1;
    text-align: center;
    font-size: 10px;
    color: {TEXT_DIMMER};
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-style: italic;
    margin-bottom: 2rem;
}}

/* ── Rare badge ── */
.rare-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(255,200,0,0.15), rgba(255,150,0,0.08));
    border: 1px solid rgba(255,200,0,0.4);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #ffc85c;
    margin-bottom: 10px;
    animation: rarePulse 2s ease-in-out infinite;
}}
@keyframes rarePulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(255,200,0,0.2); }}
    50%       {{ box-shadow: 0 0 16px 4px rgba(255,200,0,0.15); }}
}}

/* ── Song title bounce ── */
.res-song-name {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 34px;
    letter-spacing: 2px;
    color: {ACCENT};
    line-height: 1.05;
    margin-bottom: 4px;
    filter: drop-shadow(0 0 12px {ACCENT_GLOW});
    animation: songBounce 1.6s ease-in-out infinite;
    display: inline-block;
}}
@keyframes songBounce {{
    0%, 100% {{ transform: translateY(0px); }}
    30%       {{ transform: translateY(-4px); }}
    60%       {{ transform: translateY(-2px); }}
}}

/* ── Horoscope card ── */
.horoscope-card {{
    background: linear-gradient(135deg, rgba(130,80,255,0.12), rgba(255,45,120,0.06));
    border: 1px solid rgba(130,80,255,0.25);
    border-radius: 18px;
    padding: 18px 16px;
    margin-bottom: 14px;
}}
.horoscope-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 12px;
    letter-spacing: 0.18em;
    color: rgba(130,80,255,0.7);
    margin-bottom: 10px;
    text-transform: uppercase;
}}
.horoscope-text {{
    font-size: 13px;
    color: {TEXT};
    line-height: 1.7;
    font-style: italic;
}}

/* ── Feature postcards ── */
.postcards-section {{ display: flex; flex-direction: column; gap: 12px; margin-top: 4px; }}
.postcard {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 14px 15px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}}
.postcard::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 16px 16px 0 0;
}}
.postcard-pink::before   {{ background: linear-gradient(90deg, #ff2d78, #ff85b3); }}
.postcard-purple::before {{ background: linear-gradient(90deg, #8250ff, #c77dff); }}
.postcard-gold::before   {{ background: linear-gradient(90deg, #ffc85c, #ff9f1c); }}
.postcard-teal::before   {{ background: linear-gradient(90deg, #00c9b1, #00e5ff); }}
.postcard-lime::before   {{ background: linear-gradient(90deg, #a8ff3e, #78edcd); }}
.postcard-icon    {{ font-size: 20px; margin-bottom: 5px; display: block; }}
.postcard-heading {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 14px; letter-spacing: 1.5px;
    color: {TEXT}; margin-bottom: 4px; line-height: 1.1;
}}
.postcard-desc {{ font-size: 10px; color: {TEXT_DIM}; line-height: 1.5; }}

/* ── Quiz ── */
.q-label {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px; letter-spacing: 2px;
    color: {TEXT}; margin-bottom: 1.2rem;
}}
div[data-testid="stRadio"] > div {{
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 10px !important;
}}
div[data-testid="stRadio"] label {{
    background: {BG2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
    padding: 16px 14px !important;
    color: {TEXT_DIM} !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    line-height: 1.45 !important;
    min-height: 68px !important;
    display: flex !important;
    align-items: center !important;
}}
div[data-testid="stRadio"] label:hover {{
    border-color: {ACCENT} !important;
    color: {TEXT} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px {ACCENT_GLOW} !important;
    background: {ACCENT_DIM} !important;
}}
div[data-testid="stRadio"] label:has(input:checked) {{
    border-color: {ACCENT} !important;
    background: {ACCENT_DIM} !important;
    color: {ACCENT} !important;
    box-shadow: 0 0 0 1px {ACCENT} !important;
}}
div[data-testid="stRadio"] input[type="radio"]  {{ display: none !important; }}
div[data-testid="stRadio"] label > div:first-child {{ display: none !important; }}
div[data-testid="stRadio"] > label {{ display: none !important; }}

/* ── Progress dots ── */
.dots-row {{ display:flex; gap:6px; justify-content:center; margin-bottom:2rem; }}
.pdot {{ width:6px; height:6px; border-radius:50%; background:rgba(255,255,255,0.12); transition:all 0.3s; }}
.pdot.active {{ background:{ACCENT}; width:22px; border-radius:3px; }}
.pdot.done   {{ background:{ACCENT_MID}; }}

/* ── Buttons ── */
div.stButton > button {{
    background: {ACCENT} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    letter-spacing: 0.05em !important;
    width: auto !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px {ACCENT_GLOW} !important;
}}
div.stButton > button:hover {{
    background: #ff5599 !important;
    transform: scale(1.04) !important;
    box-shadow: 0 6px 28px {ACCENT_GLOW} !important;
}}

/* ── Result card ── */
.result-wrap {{
    border-radius: 20px;
    border: 1px solid rgba(255,45,120,0.2);
    background: {CARD_BG};
    padding: 2rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}}
.result-wrap::before {{
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, {ACCENT_GLOW}, transparent 70%);
    pointer-events: none;
}}
.res-artist-name {{ font-size: 14px; color: {TEXT_DIM}; margin-bottom: 14px; }}
.vibe-tag {{
    display: inline-block;
    background: {ACCENT_DIM};
    border: 1px solid rgba(255,45,120,0.35);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: {ACCENT}; margin-bottom: 14px;
}}
.res-reason    {{ font-size: 14px; line-height: 1.8; color: {TEXT_DIM}; border-top: 1px solid {BORDER}; padding-top: 1rem; }}
.match-info    {{ font-size: 11px; color: {TEXT_DIMMER}; margin-top: 1rem; letter-spacing: 0.05em; }}
.yt-btn {{
    display: inline-block; margin-top: 1rem; color: {ACCENT};
    font-size: 13px; font-weight: 600; text-decoration: none;
    border: 1px solid rgba(255,45,120,0.3); border-radius: 999px;
    padding: 6px 18px; transition: all 0.2s;
}}
.yt-btn:hover {{ background: {ACCENT_DIM}; color: {ACCENT}; box-shadow: 0 0 16px {ACCENT_GLOW}; }}
.roast-txt {{ color: #ff8fab; font-size: 13px; text-align: center; margin: 1.5rem 0 0.5rem; font-weight: 500; font-style: italic; }}

/* ── Genre grid ── */
.section-lbl {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 13px; letter-spacing: 0.2em;
    color: {TEXT_DIMMER}; margin-bottom: 10px;
}}
.genre-card {{
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 14px; color: {TEXT_DIM};
    font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.18s;
    line-height: 1.4; user-select: none;
}}
.genre-card:hover {{ border-color: {ACCENT}; background: {ACCENT_DIM}; color: {TEXT}; transform: translateY(-1px); }}
.genre-sel {{ border-color: {ACCENT} !important; background: {ACCENT_DIM} !important; color: {ACCENT} !important; }}

/* ── Sidebar boxes ── */
.side-box {{
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 18px; padding: 18px 16px; margin-bottom: 14px;
}}
.side-box-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 12px; letter-spacing: 0.18em;
    color: {TEXT_DIMMER}; margin-bottom: 12px; text-transform: uppercase;
}}
.votd-card {{
    background: linear-gradient(135deg, rgba(255,45,120,0.14) 0%, rgba(255,45,120,0.04) 100%);
    border: 1px solid rgba(255,45,120,0.28);
    border-radius: 18px; padding: 18px 16px; margin-bottom: 14px;
}}
.hist-item {{
    display: flex; align-items: center; gap: 8px;
    padding: 7px 0; border-bottom: 1px solid {BORDER};
    font-size: 11px;
}}
.hist-item:last-child {{ border-bottom: none; padding-bottom: 0; }}
.hist-date  {{ color: {TEXT_DIMMER}; min-width: 36px; font-size: 9px; }}
.hist-song  {{ color: {TEXT}; font-weight: 600; flex: 1; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 110px; }}
.hist-vibe  {{
    font-size: 9px; background: {ACCENT_DIM};
    border: 1px solid rgba(255,45,120,0.18); border-radius: 999px;
    padding: 2px 7px; color: {ACCENT}; white-space: nowrap;
}}
.hist-empty {{ font-size: 11px; color: {TEXT_DIMMER}; font-style: italic; text-align: center; padding: 10px 0; }}
.streak-row  {{ display: flex; gap: 5px; flex-wrap: wrap; margin-top: 6px; }}
.streak-chip {{
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 999px; padding: 3px 9px; font-size: 9px; color: {TEXT_DIMMER};
}}
.streak-chip.active {{ background: {ACCENT_DIM}; border-color: rgba(255,45,120,0.3); color: {ACCENT}; }}
.compat-row {{ display: flex; gap: 8px; align-items: flex-start; padding: 7px 0; border-bottom: 1px solid {BORDER}; font-size: 11px; }}
.compat-row:last-child {{ border-bottom: none; }}
.compat-vibe {{ font-size: 16px; width: 22px; text-align: center; padding-top: 1px; }}
.compat-name {{ flex: 1; color: {TEXT_DIM}; font-weight: 500; font-size: 11px; }}
.compat-pct  {{ color: {ACCENT}; font-weight: 700; font-size: 12px; min-width: 32px; text-align: right; }}
.compat-bar-wrap {{ width: 100%; height: 2px; background: {BORDER}; border-radius: 2px; margin-top: 4px; }}
.compat-bar      {{ height: 2px; border-radius: 2px; background: {ACCENT}; }}

/* ── Kill the radio widget + its label ── */
div[data-testid="stRadio"] {{ display: none !important; }}

/* ── Responsive ── */
@media (max-width: 900px) {{
    section[data-testid="stMain"] > div > div > div[data-testid="stHorizontalBlock"] {{
        flex-direction: column !important;
    }}
    .postcards-section {{ grid-template-columns: 1fr !important; }}
    .genre-grid {{ grid-template-columns: 1fr 1fr !important; }}
}}
@media (max-width: 600px) {{
    .vibe-title  {{ font-size: 48px !important; }}
    .vibe-sub    {{ font-size: 12px !important; }}
    .genre-grid  {{ grid-template-columns: 1fr 1fr !important; }}
    .hero-wrap   {{ padding: 24px 16px 18px !important; }}
    .result-wrap {{ padding: 20px 16px !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Cursor Sparkle Trail ────────────────────────────────────────
components.html(f"""
<script>
(function() {{
    var doc = window.parent.document;
    var win = window.parent;
    var old = doc.getElementById('sparkle-canvas');
    if (old) old.remove();
    var canvas = doc.createElement('canvas');
    canvas.id = 'sparkle-canvas';
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:2147483647;';
    doc.body.appendChild(canvas);
    var ctx = canvas.getContext('2d');
    function resize() {{ canvas.width = win.innerWidth; canvas.height = win.innerHeight; }}
    resize();
    win.addEventListener('resize', resize);
    var particles = [];
    var isDark = {'true' if st.session_state.dark_mode else 'false'};
    var colors = isDark
        ? ['#ff2d78','#ff85b3','#ffffff','#ffb3d1','#ff5599','#ffe0ec']
        : ['#ff2d78','#ffb3d1','#ff85b3','#ffd6e8','#e91e63','#ff4081'];
    doc.addEventListener('mousemove', function(e) {{
        for (var i = 0; i < 4; i++) {{
            particles.push({{
                x: e.clientX + (Math.random()-0.5)*10,
                y: e.clientY + (Math.random()-0.5)*10,
                vx: (Math.random()-0.5)*2.5,
                vy: (Math.random()-1.5)*2.5,
                life: 1.0,
                size: Math.random()*5+2,
                color: colors[Math.floor(Math.random()*colors.length)],
                shape: Math.random() > 0.5 ? 'star' : 'circle'
            }});
        }}
    }});
    function drawStar(cx, x, y, r, col, alpha) {{
        cx.save(); cx.globalAlpha = alpha; cx.fillStyle = col; cx.beginPath();
        for (var i = 0; i < 5; i++) {{
            var a = (i * 4 * Math.PI / 5) - Math.PI/2;
            var ia = a + 2*Math.PI/5;
            if (i===0) cx.moveTo(x+r*Math.cos(a), y+r*Math.sin(a));
            else cx.lineTo(x+r*Math.cos(a), y+r*Math.sin(a));
            cx.lineTo(x+r*0.4*Math.cos(ia), y+r*0.4*Math.sin(ia));
        }}
        cx.closePath(); cx.fill(); cx.restore();
    }}
    function animate() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (var i = particles.length-1; i >= 0; i--) {{
            var p = particles[i];
            p.x += p.vx; p.y += p.vy; p.vy += 0.06; p.life -= 0.022;
            if (p.life <= 0) {{ particles.splice(i, 1); continue; }}
            if (p.shape === 'star') {{ drawStar(ctx, p.x, p.y, p.size, p.color, p.life); }}
            else {{
                ctx.save(); ctx.globalAlpha = p.life; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.size*0.6, 0, Math.PI*2);
                ctx.fill(); ctx.restore();
            }}
        }}
        requestAnimationFrame(animate);
    }}
    animate();
}})();
</script>
""", height=0)

# ── Helpers ─────────────────────────────────────────────────────
def generate_roast(song, user_tags, genre):
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        prompt = f"""You are a sassy Gen Z music expert who just recommended "{song['song']}" by {song['artist']}.
Their vibe tags: {', '.join(user_tags)}. Genre preference: {genre}.
Write 2-3 punchy sentences roasting them. Reference their tags. End with a sassy one-liner.
Mean but loving. Very Gen Z. No hashtags."""
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception:
        return f"ur tags literally screamed '{song['vibe']}' and i had no choice. this song found u. ur welcome."

def render_genre_cards(genres, selected_genre):
    html = '<div class="genre-grid" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:1rem">'
    for i, g in enumerate(genres):
        extra = " genre-sel" if g == selected_genre else ""
        html += f'<div class="genre-card{extra}" data-gidx="{i}">{g}</div>'
    html += "</div>"
    return html

def attach_genre_audio(genres):
    srcs_json = json.dumps([GENRE_AUDIO.get(g, "") for g in genres])
    components.html(f"""
    <script>
    (function() {{
        var srcs = {srcs_json};
        var _audio = null;
        function play(src) {{
            if (!src) return;
            if (_audio) {{ _audio.pause(); _audio.currentTime = 0; }}
            _audio = new Audio(src); _audio.volume = 0.2;
            _audio.play().catch(function(){{}});
        }}
        function stop() {{ if (_audio) {{ _audio.pause(); _audio.currentTime = 0; }} }}
        function attach() {{
            try {{
                var pdoc = window.parent.document;
                var cards = pdoc.querySelectorAll('.genre-card');
                if (!cards.length) return false;
                cards.forEach(function(card, i) {{
                    if (card.dataset.ah) return;
                    card.dataset.ah = '1';
                    card.addEventListener('mouseenter', function() {{ play(srcs[i]); }});
                    card.addEventListener('mouseleave', stop);
                    card.addEventListener('click', function() {{
                        var inputs = pdoc.querySelectorAll('input[type="radio"]');
                        if (inputs[i]) inputs[i].click();
                    }});
                }});
                return true;
            }} catch(e) {{ return false; }}
        }}
        var t = 0;
        var iv = setInterval(function() {{ if (attach() || ++t > 40) clearInterval(iv); }}, 150);
    }})();
    </script>
    """, height=0)

def save_to_history(song_name, artist, vibe, tags):
    hist_file = ".vibe_history.json"
    try:
        history = []
        if os.path.exists(hist_file):
            with open(hist_file) as f: history = json.load(f)
        today = datetime.datetime.now().strftime("%b %d")
        entry = {
            "date": today, "song": song_name, "artist": artist,
            "vibe": vibe, "tags": tags,
            "ts": datetime.datetime.now().isoformat()
        }
        history.insert(0, entry)
        history = history[:30]
        with open(hist_file, "w") as f: json.dump(history, f)
    except Exception:
        pass

def load_history():
    hist_file = ".vibe_history.json"
    try:
        if os.path.exists(hist_file):
            with open(hist_file) as f: return json.load(f)
    except Exception:
        pass
    return []

def get_dominant_tag(history):
    if not history: return "dreamer"
    tag_counts = {}
    for entry in history:
        for t in entry.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    return max(tag_counts, key=tag_counts.get) if tag_counts else "dreamer"

def get_week_vibes(history):
    seen_dates = {}
    for entry in history:
        d = entry.get("date", "")
        if d not in seen_dates: seen_dates[d] = entry.get("vibe", "")
    return list(seen_dates.items())[:7]

def compute_compat(history):
    if not history: return []
    tag_counts = {}
    for entry in history:
        for t in entry.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    total = sum(tag_counts.values()) or 1
    COMPAT_LABELS = {
        "main_character": ("The Main Character", "💅"),
        "villain":        ("The Villain",         "😈"),
        "healing":        ("The Healer",           "🌸"),
        "rotting":        ("Rotting Royalty",      "🛌"),
        "down_bad":       ("Down Bad Bestie",      "💀"),
        "unbothered":     ("The Unbothered",       "😏"),
        "dreamer":        ("The Dreamer",          "🌌"),
        "emotional":      ("Emotional Support Animal","✍️"),
        "chaotic":        ("Chaotic Neutral",      "🌪️"),
        "obsessive":      ("Obsessive Romantic",   "👁️"),
        "curated":        ("Playlist Perfectionist","🎧"),
        "gremlin":        ("Gremlin Hours",        "📲"),
        "healthy":        ("Psychologically Safe", "🐶"),
        "aloof":          ("Chronically Aloof",    "🫥"),
        "hype_energy":    ("Hype Machine",         "🔥"),
        "oversharer":     ("Oversharer Era",       "📖"),
        "gen_z_text":     ("lowercase only",       "💬"),
        "in_denial":      ("In Denial Era",        "🙈"),
        "unhinged_creative":("Unhinged Creative",  "🎤"),
        "chaotic_shuffle":("Shuffle Goblin",       "📻"),
    }
    sorted_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    result = []
    for tag, cnt in sorted_tags[:4]:
        if tag in COMPAT_LABELS:
            label, emoji = COMPAT_LABELS[tag]
            pct = min(int((cnt / total) * 100 * 3), 98)
            result.append({"label": label, "emoji": emoji, "pct": pct})
    return result


POSTCARDS_HTML = """
<div class="postcards-section">
    <div class="postcard postcard-pink">
        <span class="postcard-icon">🖱️</span>
        <div class="postcard-heading">Pink Sparkle Trail</div>
        <div class="postcard-desc">ur cursor leaves a Y2K sparkle trail everywhere it goes. main character behavior only.</div>
    </div>
    <div class="postcard postcard-purple">
        <span class="postcard-icon">🎵</span>
        <div class="postcard-heading">Song Title Bounce</div>
        <div class="postcard-desc">when ur result drops, the song title literally bounces to the beat. it's giving rhythm.</div>
    </div>
    <div class="postcard postcard-lime">
        <span class="postcard-icon">🌸</span>
        <div class="postcard-heading">Soft Girl Mode</div>
        <div class="postcard-desc">tap the toggle (top left) to flip into pastel light mode. ur either dark academia or cottagecore, no in-between.</div>
    </div>
    <div class="postcard postcard-gold">
        <span class="postcard-icon">🏆</span>
        <div class="postcard-heading">Rare Vibe Badge</div>
        <div class="postcard-desc">get a rare tag combo and unlock a golden badge. only 1-3% of users ever see it. are u built different?</div>
    </div>
    <div class="postcard postcard-teal">
        <span class="postcard-icon">🔮</span>
        <div class="postcard-heading">Vibe Horoscope</div>
        <div class="postcard-desc">ai-generated 2-line forecast based on ur dominant vibe + today's energy. refreshes daily. no zodiac required.</div>
    </div>
</div>
"""

# ── SIDEBAR renderer ────────────────────────────────────────────
def render_sidebar(horoscope_text=None):
    votd = get_votd()
    history = load_history()
    compat = compute_compat(history)

    yt_q   = f"{votd['song']} {votd['artist']} official audio".replace(" ", "+")
    yt_url = f"https://www.youtube.com/results?search_query={yt_q}"

    hist_html = ""
    if history:
        for h in history[:6]:
            hist_html += f"""
            <div class="hist-item">
                <span class="hist-date">{h['date']}</span>
                <span class="hist-song">{h['song']}</span>
                <span class="hist-vibe">{h['vibe']}</span>
            </div>"""
    else:
        hist_html = '<div class="hist-empty">no vibes logged yet<br>take the quiz! 🎧</div>'

    days_short = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    streak_html = '<div class="streak-row">'
    for i, d in enumerate(days_short):
        found = ""
        for entry in history:
            try:
                ts = datetime.datetime.fromisoformat(entry.get("ts",""))
                if ts.weekday() == i and (datetime.datetime.now() - ts).days < 7:
                    found = "active"; break
            except Exception: pass
        streak_html += f'<div class="streak-chip {found}">{d}</div>'
    streak_html += "</div>"

    if compat:
        compat_html = ""
        for c in compat:
            compat_html += f"""
            <div class="compat-row">
                <span class="compat-vibe">{c['emoji']}</span>
                <div style="flex:1">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <span class="compat-name">{c['label']}</span>
                        <span class="compat-pct">{c['pct']}%</span>
                    </div>
                    <div class="compat-bar-wrap"><div class="compat-bar" style="width:{c['pct']}%"></div></div>
                </div>
            </div>"""
    else:
        compat_html = '<div class="hist-empty">take the quiz to unlock<br>ur personality type 🔍</div>'

    if horoscope_text:
        lines = horoscope_text.strip().split("\n")
        formatted = "<br>".join(l.strip() for l in lines if l.strip())
        horoscope_block = f"""
        <div class="horoscope-card">
            <div class="horoscope-title">🔮 ur vibe forecast</div>
            <div class="horoscope-text">{formatted}</div>
        </div>"""
    else:
        horoscope_block = f"""
        <div class="horoscope-card">
            <div class="horoscope-title">🔮 ur vibe forecast</div>
            <div class="horoscope-text" style="color:rgba(130,80,255,0.4);font-style:italic;font-size:11px;">take the quiz to unlock ur daily forecast ✨</div>
        </div>"""

    # theme-aware colours for the isolated iframe
    text_color  = '#fff'        if st.session_state.dark_mode else '#2d0a1a'
    text_dim    = 'rgba(255,255,255,0.4)'  if st.session_state.dark_mode else 'rgba(45,10,26,0.5)'
    text_dimmer = 'rgba(255,255,255,0.2)'  if st.session_state.dark_mode else 'rgba(45,10,26,0.3)'
    border_col  = 'rgba(255,255,255,0.08)' if st.session_state.dark_mode else 'rgba(255,100,160,0.2)'
    box_bg      = 'rgba(255,255,255,0.03)' if st.session_state.dark_mode else 'rgba(255,150,190,0.08)'

    sidebar_html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,400;0,500;0,600&display=swap');
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: transparent; font-family: 'DM Sans', sans-serif; color: {text_color}; }}
    .side-box {{ background:{box_bg}; border:1px solid {border_col}; border-radius:18px; padding:18px 16px; margin-bottom:14px; }}
    .side-box-title {{ font-family:'Bebas Neue',sans-serif; font-size:12px; letter-spacing:0.18em; color:{text_dimmer}; margin-bottom:12px; text-transform:uppercase; }}
    .votd-card {{ background:linear-gradient(135deg,rgba(255,45,120,0.14) 0%,rgba(255,45,120,0.04) 100%); border:1px solid rgba(255,45,120,0.28); border-radius:18px; padding:18px 16px; margin-bottom:14px; }}
    .votd-emoji {{ font-size:26px; margin-bottom:4px; }}
    .votd-vibe  {{ font-family:'Bebas Neue',sans-serif; font-size:16px; letter-spacing:1.5px; color:#ff2d78; line-height:1.1; margin-bottom:3px; }}
    .votd-song  {{ font-size:14px; font-weight:600; color:{text_color}; margin-bottom:2px; }}
    .votd-artist{{ font-size:11px; color:{text_dim}; margin-bottom:8px; }}
    .votd-note  {{ font-size:10px; color:{text_dimmer}; font-style:italic; border-top:1px solid {border_col}; padding-top:8px; margin-top:4px; }}
    .votd-btn   {{ display:inline-block; margin-top:10px; color:#ff2d78; font-size:11px; font-weight:600; text-decoration:none; border:1px solid rgba(255,45,120,0.3); border-radius:999px; padding:4px 14px; }}
    .hist-item  {{ display:flex; align-items:center; gap:8px; padding:7px 0; border-bottom:1px solid {border_col}; font-size:11px; }}
    .hist-item:last-child {{ border-bottom:none; padding-bottom:0; }}
    .hist-date  {{ color:{text_dimmer}; min-width:36px; font-size:9px; }}
    .hist-song  {{ color:{text_color}; font-weight:600; flex:1; font-size:11px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:110px; }}
    .hist-vibe  {{ font-size:9px; background:rgba(255,45,120,0.1); border:1px solid rgba(255,45,120,0.18); border-radius:999px; padding:2px 7px; color:#ff2d78; white-space:nowrap; }}
    .hist-empty {{ font-size:11px; color:{text_dimmer}; font-style:italic; text-align:center; padding:10px 0; }}
    .streak-row {{ display:flex; gap:5px; flex-wrap:wrap; margin-top:6px; }}
    .streak-chip {{ background:{box_bg}; border:1px solid {border_col}; border-radius:999px; padding:3px 9px; font-size:9px; color:{text_dimmer}; }}
    .streak-chip.active {{ background:rgba(255,45,120,0.12); border-color:rgba(255,45,120,0.3); color:#ff2d78; }}
    .compat-row {{ display:flex; gap:8px; align-items:flex-start; padding:7px 0; border-bottom:1px solid {border_col}; font-size:11px; }}
    .compat-row:last-child {{ border-bottom:none; }}
    .compat-vibe {{ font-size:16px; width:22px; text-align:center; padding-top:1px; }}
    .compat-name {{ flex:1; color:{text_dim}; font-weight:500; font-size:11px; }}
    .compat-pct  {{ color:#ff2d78; font-weight:700; font-size:12px; min-width:32px; text-align:right; }}
    .compat-bar-wrap {{ width:100%; height:2px; background:{border_col}; border-radius:2px; margin-top:4px; }}
    .compat-bar {{ height:2px; border-radius:2px; background:#ff2d78; }}
    .horoscope-card {{ background:linear-gradient(135deg,rgba(130,80,255,0.12),rgba(255,45,120,0.06)); border:1px solid rgba(130,80,255,0.25); border-radius:18px; padding:18px 16px; margin-bottom:14px; }}
    .horoscope-title {{ font-family:'Bebas Neue',sans-serif; font-size:12px; letter-spacing:0.18em; color:rgba(130,80,255,0.7); margin-bottom:10px; text-transform:uppercase; }}
    .horoscope-text  {{ font-size:13px; color:{text_color}; line-height:1.7; font-style:italic; }}
    </style>

    <div class="votd-card">
        <div class="side-box-title">✨ vibe of the day</div>
        <div class="votd-emoji">{votd['emoji']}</div>
        <div class="votd-vibe">{votd['vibe']}</div>
        <div class="votd-song">{votd['song']}</div>
        <div class="votd-artist">— {votd['artist']}</div>
        <div class="votd-note">{votd['note']}</div>
        <a class="votd-btn" href="{yt_url}" target="_blank">↗ listen now</a>
    </div>

    {horoscope_block}

    <div class="side-box">
        <div class="side-box-title">📼 vibe history</div>
        {hist_html}
        <div style="margin-top:10px;">
            <div class="side-box-title" style="margin-bottom:6px;">this week</div>
            {streak_html}
        </div>
    </div>

    <div class="side-box">
        <div class="side-box-title">🔮 ur personality type</div>
        {compat_html}
    </div>
    """
    return sidebar_html


# ═══════════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════════
left_col, mid_col, right_col = st.columns([1, 1.6, 1], gap="large")

with left_col:
    st.markdown('<div class="section-lbl">🆕 what\'s new</div>', unsafe_allow_html=True)
    st.markdown(POSTCARDS_HTML, unsafe_allow_html=True)

with right_col:
    horoscope_text = st.session_state.get("horoscope", None)
    sidebar_html = render_sidebar(horoscope_text)
    components.html(sidebar_html, height=1200, scrolling=True)

with mid_col:
    # ── eye counter ──
    vc = st.session_state.view_count
    st.markdown(
        f'<div class="eye-counter"><span>👁</span>{vc:,}</div>' if isinstance(vc, int)
        else f'<div class="eye-counter"><span>👁</span>{vc}</div>',
        unsafe_allow_html=True,
    )

    # ── dark/light toggle ──
    if st.button(TOGGLE_LABEL, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    # ════════════════════════════════════════════════════════════
    # START SCREEN
    # ════════════════════════════════════════════════════════════
    if st.session_state.step == "start":

        # ── Hero block ──
        st.markdown(f"""
        <div class="hero-wrap">
            <div class="hero-noise-line"></div>
            <div class="hero-glow-ring"></div>
            <div class="hero-glow-ring-2"></div>
            <div class="hero-title-row">
                <span class="vibe-title">VibeCheck.ai</span>
                <span class="vibe-knife">🔪</span>
            </div>
            <div class="vibe-sub">5 questions. 1 song. no mercy.</div>
            <div class="made-by">built on 3hrs of sleep &amp; spite by khushi ☕</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-lbl">pick ur genre (optional)</div>', unsafe_allow_html=True)
        genre = st.radio("Genre", GENRES, key="genre_radio", label_visibility="collapsed")
        st.session_state.genre = genre
        st.markdown(render_genre_cards(GENRES, genre), unsafe_allow_html=True)
        attach_genre_audio(GENRES)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("let's fix it 🎯"):
            st.session_state.step = "quiz"
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.selected_tag = None
            st.rerun()

    # ════════════════════════════════════════════════════════════
    # QUIZ
    # ════════════════════════════════════════════════════════════
    elif st.session_state.step == "quiz":
        q_idx = st.session_state.current_q
        q = QUESTIONS[q_idx]
        dots_html = '<div class="dots-row">' + "".join([
            f'<div class="pdot {"active" if i == q_idx else "done" if i < q_idx else ""}"></div>'
            for i in range(len(QUESTIONS))
        ]) + '</div>'
        st.markdown(dots_html, unsafe_allow_html=True)
        st.markdown(f'<div class="q-label">{q["emoji"]} {q["text"]}</div>', unsafe_allow_html=True)
        option_labels = [o["label"] for o in q["options"]]
        option_tags   = [o["tag"]   for o in q["options"]]
        choice = st.radio("hidden", option_labels, label_visibility="hidden", key=f"q_{q_idx}")
        chosen_tag = option_tags[option_labels.index(choice)]
        st.session_state.selected_tag = chosen_tag
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            btn_label = "next →" if q_idx < len(QUESTIONS) - 1 else "fix my playlist 🔪"
            if st.button(btn_label):
                st.session_state.answers.append(chosen_tag)
                if q_idx < len(QUESTIONS) - 1:
                    st.session_state.current_q += 1
                    st.session_state.selected_tag = None
                    st.rerun()
                else:
                    st.session_state.step = "result"
                    st.rerun()

    # ════════════════════════════════════════════════════════════
    # RESULT
    # ════════════════════════════════════════════════════════════
    elif st.session_state.step == "result":
        user_tags = st.session_state.answers
        genre = st.session_state.genre if st.session_state.genre != "no preference" else None

        if st.session_state.result is None:
            with st.spinner("diagnosing ur taste..."):
                top   = get_top_match(user_tags, genre_filter=genre)
                roast = generate_roast(top, user_tags, st.session_state.genre)
                top["roast"] = roast
                st.session_state.result = top
                save_to_history(top["song"], top["artist"], top["vibe"], user_tags)
                history  = load_history()
                dominant = get_dominant_tag(history)
                st.session_state.horoscope = generate_vibe_horoscope(dominant)
                st.rerun()

        r        = st.session_state.result
        yt_query = f"{r['song']} {r['artist']} official audio".replace(" ", "+")
        yt_url   = f"https://www.youtube.com/results?search_query={yt_query}"

        rare      = get_rare_badge(user_tags)
        rare_html = ""
        if rare:
            badge_name, badge_stat, badge_emoji = rare
            rare_html = f'<div class="rare-badge">{badge_emoji} {badge_name} &nbsp;·&nbsp; {badge_stat}</div>'

        safe_song   = html_lib.escape(r['song'])
        safe_artist = html_lib.escape(r['artist'])
        safe_vibe   = html_lib.escape(r['vibe'])
        safe_roast  = html_lib.escape(r['roast'])
        safe_genre  = html_lib.escape(r['genre'])

        st.markdown(f"""
        <div class="result-wrap">
            {rare_html}
            <div class="res-song-name">{safe_song}</div>
            <div class="res-artist-name">— {safe_artist}</div>
            <div class="vibe-tag">{safe_vibe}</div>
            <div class="res-reason">{safe_roast}</div>
            <div class="match-info">match score: {r['score']:.0%} &nbsp;·&nbsp; genre: {safe_genre}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("see ur top 3 matches"):
            top3 = recommend(user_tags, genre_filter=genre, top_k=3)
            for i, s in enumerate(top3):
                st.markdown(f"**{i+1}. {s['song']}** — {s['artist']}  `{s['score']:.0%} match` · _{s['vibe']}_")

        roast_line = ROASTS[st.session_state.retries % len(ROASTS)]
        st.markdown(f'<p class="roast-txt">{roast_line}</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("yeah fine, again 😒"):
                st.session_state.step       = "start"
                st.session_state.answers    = []
                st.session_state.result     = None
                st.session_state.current_q  = 0
                st.session_state.selected_tag = None
                st.session_state.retries   += 1
                st.rerun()