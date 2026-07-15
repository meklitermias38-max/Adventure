import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
from datetime import datetime, date, timedelta

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="DayRise Adventures",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dayrise_data.json")

# ============================================================================
# PERSISTENCE LAYER
# ============================================================================
def load_all_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_all_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def default_player(persona="Urban Explorer 🌃"):
    return {
        "persona": persona,
        "xp": 0,
        "level": 1,
        "streak": 0,
        "last_completed_date": None,
        "last_seen_date": None,
        "archive": [],
        "total_completed": 0,
    }


def get_level_info(xp):
    level = min(10, 1 + xp // 100)
    if level >= 10:
        progress_xp = 100
        percent = 100
    else:
        progress_xp = xp - (level - 1) * 100
        percent = int((progress_xp / 100) * 100)
    return level, progress_xp, percent


# ============================================================================
# QUEST BANKS
# ============================================================================
WEEKDAY_QUESTS = [
    {"title": "The Secret Keyboard Agent", "desc": "For the next hour, type every message with unusual flair — sign off every Slack/email with a tiny secret code word. See who notices your covert identity.", "category": "creative", "emoji": "⌨️"},
    {"title": "The Silent Lunch Sensor", "desc": "Eat one meal today in complete silence, phone face-down. Notice five things about the taste, texture, and smell of your food you'd normally miss.", "category": "mindfulness", "emoji": "🍽️"},
    {"title": "The Blind Grocery Grab", "desc": "Next store trip, pick one item you've never bought before without reading the label first — decide purely on packaging instinct. Reveal the surprise at checkout.", "category": "chaos", "emoji": "🛒"},
    {"title": "The Elevator Pitch Ninja", "desc": "Before your next elevator ride (real or imagined), prepare a 20-second pitch of your wildest business idea. Deliver it to a stranger, coworker, or your reflection.", "category": "social", "emoji": "🛗"},
    {"title": "The Desk Yoga Stealth Mission", "desc": "Every hour today, execute one covert desk stretch so smooth your coworkers never suspect you're doing yoga at your workstation.", "category": "physical", "emoji": "🧘"},
    {"title": "The One-Word Compliment Drop", "desc": "Give three different people a genuine one-word compliment today. Track their reactions — who lights up the most?", "category": "social", "emoji": "💬"},
    {"title": "The Coffee Cup Anthropologist", "desc": "Study the next coffee shop line like a field researcher. Silently guess each person's job from their order and posture. Never ask — just observe.", "category": "sensory", "emoji": "☕"},
    {"title": "The Polyglot Whisper", "desc": "Learn today's vocabulary word and use it in a real sentence with a real human, even if they have no idea what it means.", "category": "language", "emoji": "🗣️"},
    {"title": "The Stairwell Sprint", "desc": "Find the nearest stairwell and climb two flights faster than you think you can. Log your finishing thought at the top.", "category": "physical", "emoji": "🏃"},
    {"title": "The Doodle Diplomat", "desc": "Sketch a tiny doodle on a sticky note and leave it somewhere a stranger or coworker will find it today.", "category": "art", "emoji": "🎨"},
    {"title": "The Micro-Meditation Hacker", "desc": "Steal three minutes between meetings for the Mind-Sync breathing ritual. No skipping, no scrolling.", "category": "mindfulness", "emoji": "⏱️"},
    {"title": "The Reverse Commute Explorer", "desc": "Take one different turn, street, or exit on your way home today. Document one new thing you spotted.", "category": "sensory", "emoji": "🔄"},
    {"title": "The Emoji Only Texter", "desc": "Reply to your next three text messages using only emoji. Force yourself to be creatively precise.", "category": "creative", "emoji": "📱"},
    {"title": "The Left-Handed Rebel", "desc": "Do one ordinary task today — brushing teeth, opening a door, writing a note — with your non-dominant hand.", "category": "chaos", "emoji": "✋"},
    {"title": "The Silent Disco Walker", "desc": "Put on headphones, queue a song that hypes you up, and walk somewhere ordinary like you're headlining a stadium. Keep a straight face.", "category": "creative", "emoji": "🎧"},
    {"title": "The Mystery Playlist DJ", "desc": "Build a 5-song playlist blind — pick titles you don't recognize. Play it during a mundane task and rate the vibe.", "category": "creative", "emoji": "🎵"},
    {"title": "The Gratitude Ambush", "desc": "Send an unprompted thank-you message to someone who impacted you years ago and never got proper credit.", "category": "social", "emoji": "🙏"},
    {"title": "The Language Swap Barista", "desc": "Order your coffee or lunch today using today's foreign vocabulary word somewhere in the sentence, even loosely.", "category": "language", "emoji": "🌍"},
    {"title": "The Coin Flip Commander", "desc": "Let the Destiny Flip decide one small decision today that you'd normally overthink — lunch spot, route, or outfit.", "category": "chaos", "emoji": "🪙"},
    {"title": "The Standing Desk Warrior", "desc": "Work standing for one full hour today. Notice how your thinking shifts when your body isn't slouched.", "category": "physical", "emoji": "🧍"},
    {"title": "The Compliment Chain Reaction", "desc": "Compliment a stranger, then ask them to pass one along to someone else today. Track if the chain confirms it happened.", "category": "social", "emoji": "🔗"},
    {"title": "The 5-Minute Declutter Blitz", "desc": "Set a 5-minute timer and clear one chaotic surface — your desk, bag, or car. Stop the instant the timer ends.", "category": "physical", "emoji": "🧹"},
    {"title": "The Window Gazer's Journal", "desc": "Spend three uninterrupted minutes looking out a window. Write down exactly what you noticed, no filtering.", "category": "sensory", "emoji": "🪟"},
    {"title": "The Unexpected Thank You Note", "desc": "Handwrite a two-line thank-you note to a coworker or friend and physically hand it to them today.", "category": "social", "emoji": "✍️"},
    {"title": "The Office Plant Whisperer", "desc": "Find a plant near you (office, home, park) and give it a genuine 30 seconds of care — water, sunlight adjustment, or just attention.", "category": "sensory", "emoji": "🪴"},
    {"title": "The Sensory Reset Button", "desc": "Run the full 3-minute Mind-Sync timer with your eyes closed, focusing only on sounds around you. Name three you'd never noticed.", "category": "mindfulness", "emoji": "🎧"},
    {"title": "The Random Act Roulette", "desc": "Let the Destiny Flip choose between two kind acts you could do today. Whichever it lands on — commit fully.", "category": "chaos", "emoji": "🎡"},
    {"title": "The Vocabulary Vault Raid", "desc": "Learn today's vocabulary word, then teach it to someone else before the day ends. Bonus points if they remember it tomorrow.", "category": "language", "emoji": "📚"},
]

WEEKEND_QUESTS = [
    {"title": "The Horizon Hunter", "desc": "Find the highest accessible point near you — a hill, rooftop, parking garage — and watch the horizon for ten full minutes, no phone.", "category": "physical", "emoji": "🌄"},
    {"title": "The Neighborhood Grid-Run", "desc": "Pick a direction and walk exactly six blocks in a square pattern, turning only right. Map what you discover.", "category": "physical", "emoji": "🗺️"},
    {"title": "The Analog Solo Trek", "desc": "Go for a walk or hike with zero devices except a watch. Bring only a small notebook to jot down thoughts.", "category": "mindfulness", "emoji": "🥾"},
    {"title": "The Farmers Market Linguist", "desc": "Visit a market or store and use today's foreign vocabulary word while chatting with a vendor about their produce.", "category": "language", "emoji": "🧺"},
    {"title": "The Sketchbook Summit", "desc": "Find a scenic spot and sketch what you see for fifteen minutes using the Zen Painting Deck or real paper — no erasing allowed.", "category": "art", "emoji": "🖌️"},
    {"title": "The Silent Sunrise Vigil", "desc": "Wake before sunrise and watch it happen in full silence. No photos until the sun fully clears the horizon.", "category": "mindfulness", "emoji": "🌅"},
    {"title": "The Coin Toss Explorer", "desc": "At every unplanned fork in your day, let the Destiny Flip choose your direction. Follow it for at least three decisions.", "category": "chaos", "emoji": "🪙"},
    {"title": "The Urban Photography Safari", "desc": "Shoot ten photos of things people usually walk past — textures, shadows, forgotten signage. Curate your best three.", "category": "art", "emoji": "📸"},
    {"title": "The Secondhand Treasure Dive", "desc": "Visit a thrift store or flea market and find one object under $10 that tells an imaginary story you invent on the spot.", "category": "creative", "emoji": "🕵️"},
    {"title": "The Trail Less Traveled", "desc": "Choose the walking or hiking path with the fewest people. Note one plant, animal, or sound you've never noticed before.", "category": "physical", "emoji": "🌲"},
    {"title": "The Street Food Gambler", "desc": "Order a dish you've never tried from a place you've never visited. Rate it on taste, risk, and surprise.", "category": "sensory", "emoji": "🌮"},
    {"title": "The Park Bench Philosopher", "desc": "Sit on a public bench for twenty minutes and write down every question that crosses your mind, no matter how strange.", "category": "mindfulness", "emoji": "🪑"},
    {"title": "The Cloud Shape Cartographer", "desc": "Lie down outside and map five cloud shapes into a tiny story connecting them all.", "category": "creative", "emoji": "☁️"},
    {"title": "The Neighborhood Mural Hunt", "desc": "Find three pieces of public art or murals nearby you've never really looked at. Sketch or photograph your favorite.", "category": "art", "emoji": "🖼️"},
    {"title": "The Language Exchange Wanderer", "desc": "Strike up a short conversation with someone from a different cultural background and casually drop today's vocabulary word.", "category": "language", "emoji": "🌐"},
    {"title": "The Digital Detox Day", "desc": "Choose four consecutive hours today with your phone in airplane mode and out of sight. Journal what you noticed about your attention.", "category": "mindfulness", "emoji": "📵"},
    {"title": "The Random Bus Route Rider", "desc": "Hop on a bus or train line you've never taken, ride three stops further than needed, and walk back exploring the area.", "category": "chaos", "emoji": "🚌"},
    {"title": "The Rooftop Stargazer", "desc": "Find a dark-enough spot tonight and identify at least three constellations or simply watch the sky for fifteen minutes.", "category": "mindfulness", "emoji": "✨"},
    {"title": "The Farmers Field Forager", "desc": "Visit a garden, orchard, or market and learn the origin story of one fruit or vegetable you've never asked about.", "category": "sensory", "emoji": "🌾"},
    {"title": "The Solo Picnic Architect", "desc": "Build yourself a tiny solo picnic — one snack, one drink, one blanket — and eat it somewhere with a view.", "category": "creative", "emoji": "🧺"},
    {"title": "The Skyline Sketch Session", "desc": "Find a view of a skyline, rooftops, or treeline and sketch it using the Zen Painting Deck's neon brushes.", "category": "art", "emoji": "🏙️"},
    {"title": "The Silent Retreat Hour", "desc": "Spend one full hour in total intentional silence — no music, talking, or scrolling. Notice how your mind behaves by minute 40.", "category": "mindfulness", "emoji": "🤫"},
    {"title": "The Flea Market Negotiator", "desc": "Haggle playfully for one item at a market or garage sale, even if you don't plan to buy it. Track your best offer.", "category": "social", "emoji": "🤝"},
    {"title": "The Bike Path Odyssey", "desc": "Ride a bike, scooter, or walk a path twice as long as your usual route. Reward yourself at the furthest point.", "category": "physical", "emoji": "🚲"},
    {"title": "The Waterfront Wanderer", "desc": "Find any body of water nearby — river, lake, fountain, coast — and spend ten minutes just watching it move.", "category": "mindfulness", "emoji": "🌊"},
    {"title": "The Community Garden Volunteer", "desc": "Spend thirty minutes helping with any small community task — a garden, cleanup, or errand for a neighbor.", "category": "social", "emoji": "🌻"},
    {"title": "The Vintage Vinyl Hunter", "desc": "Dig through a record store, bookstore, or old media shelf and find one item made before you were born.", "category": "creative", "emoji": "💿"},
    {"title": "The Language Immersion Podcast Walk", "desc": "Take a walk listening to a short podcast or song in the language of today's vocabulary word, even without full understanding.", "category": "language", "emoji": "🎙️"},
]

VOCAB_BANK = [
    {"language": "Spanish", "flag": "🇪🇸", "word": "Duende", "meaning": "A heightened state of raw emotion and authenticity, especially felt during art or performance.", "pronunciation": "dwen-deh"},
    {"language": "Amharic", "flag": "🇪🇹", "word": "Buna", "meaning": "Coffee — but truly a ceremony of slowing down and connecting with the people around you.", "pronunciation": "boo-nah"},
    {"language": "Japanese", "flag": "🇯🇵", "word": "Komorebi", "meaning": "The dappled sunlight that filters through leaves in a forest canopy.", "pronunciation": "koh-moh-reh-bee"},
    {"language": "French", "flag": "🇫🇷", "word": "Dépaysement", "meaning": "The disorienting, alive feeling of being somewhere unfamiliar, outside your usual context.", "pronunciation": "day-pay-eez-mahn"},
    {"language": "Arabic", "flag": "🇸🇦", "word": "Tarab", "meaning": "A state of musical ecstasy, being emotionally swept away by a melody.", "pronunciation": "ta-rab"},
    {"language": "Portuguese", "flag": "🇵🇹", "word": "Saudade", "meaning": "A deep, bittersweet longing for someone or something absent, tinged with love.", "pronunciation": "sow-dah-jee"},
    {"language": "German", "flag": "🇩🇪", "word": "Waldeinsamkeit", "meaning": "The peaceful feeling of being alone in the woods, connected to nature.", "pronunciation": "vald-ine-zahm-kite"},
    {"language": "Italian", "flag": "🇮🇹", "word": "Ritrovarsi", "meaning": "To rediscover or find oneself again, often after being lost.", "pronunciation": "ree-troh-var-see"},
    {"language": "Amharic", "flag": "🇪🇹", "word": "Chigger Yellem", "meaning": "\"No worries\" — a phrase carrying a whole philosophy of easygoing resilience.", "pronunciation": "chig-gur yell-em"},
    {"language": "Japanese", "flag": "🇯🇵", "word": "Ikigai", "meaning": "Your reason for being — the intersection of what you love, what you're good at, and what the world needs.", "pronunciation": "ee-kee-guy"},
    {"language": "Welsh", "flag": "🏴", "word": "Hiraeth", "meaning": "A deep longing for a home or time you can't quite return to.", "pronunciation": "hee-rye-th"},
    {"language": "Arabic", "flag": "🇸🇦", "word": "Sabr", "meaning": "Patient perseverance through hardship, holding steady without complaint.", "pronunciation": "sah-br"},
]

CHAOS_OPTIONS = [
    ("Turn Left", "Turn Right"),
    ("Order the usual", "Order something new"),
    ("Text them first", "Wait for them to text"),
    ("Take the stairs", "Take the elevator"),
    ("Say yes", "Say no"),
    ("Window seat", "Aisle seat"),
    ("Go outside now", "Stay in for one more hour"),
    ("Call them", "Message them"),
    ("Save it for later", "Do it right now"),
    ("The scenic route", "The fastest route"),
    ("Try the spicy one", "Play it safe"),
    ("Solo mission", "Bring a friend"),
]

PERSONAS = [
    "Urban Explorer 🌃",
    "Chaos Monk 🧘",
    "Creative Renegade 🎨",
    "Polyglot Nomad 🗺️",
]

# ============================================================================
# CUSTOM CSS — THE VISUAL SHELL
# ============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Poppins', sans-serif;
}

/* ---------- APP BACKGROUND ---------- */
.stApp {
    background: radial-gradient(circle at 15% 0%, rgba(255,75,75,0.08) 0%, transparent 45%),
                radial-gradient(circle at 85% 15%, rgba(0,240,255,0.08) 0%, transparent 45%),
                radial-gradient(circle at 50% 100%, rgba(255,215,0,0.05) 0%, transparent 50%),
                #0d1117;
    color: #e6edf3;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* ---------- TYPOGRAPHY ---------- */
h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

.drx-hero-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 900;
    font-size: 3rem;
    background: linear-gradient(90deg, #ff4b4b 0%, #ffd700 50%, #00f0ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
    line-height: 1.1;
}

.drx-hero-sub {
    color: #8b949e;
    font-size: 1.05rem;
    font-weight: 500;
    margin-top: 4px;
    margin-bottom: 1.6rem;
}

.drx-section-header {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    color: #e6edf3;
    margin: 0 0 0.6rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ---------- GLASS ADVENTURE CARDS ---------- */
.drx-card {
    background: rgba(22, 27, 34, 0.75);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px 30px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.drx-card:hover {
    transform: translateY(-3px);
    border-color: rgba(255,255,255,0.16);
}

.drx-card-coral {
    box-shadow: 0 0 0px rgba(255,75,75,0.0), 0 8px 32px rgba(0,0,0,0.35);
    border-top: 2px solid rgba(255,75,75,0.55);
}
.drx-card-coral:hover { box-shadow: 0 0 40px rgba(255,75,75,0.28), 0 8px 32px rgba(0,0,0,0.4); }

.drx-card-cyan {
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    border-top: 2px solid rgba(0,240,255,0.55);
}
.drx-card-cyan:hover { box-shadow: 0 0 40px rgba(0,240,255,0.28), 0 8px 32px rgba(0,0,0,0.4); }

.drx-card-gold {
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    border-top: 2px solid rgba(255,215,0,0.55);
}
.drx-card-gold:hover { box-shadow: 0 0 40px rgba(255,215,0,0.28), 0 8px 32px rgba(0,0,0,0.4); }

.drx-tag {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.drx-tag-weekday { background: rgba(0,240,255,0.14); color: #00f0ff; border: 1px solid rgba(0,240,255,0.4); }
.drx-tag-weekend { background: rgba(255,75,75,0.14); color: #ff8080; border: 1px solid rgba(255,75,75,0.4); }

.drx-quest-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.65rem;
    margin-bottom: 10px;
    color: #f0f6fc;
}

.drx-quest-desc {
    color: #c9d1d9;
    font-size: 1.02rem;
    line-height: 1.65;
}

/* ---------- BUTTONS ---------- */
div.stButton > button {
    background: linear-gradient(135deg, #ff4b4b 0%, #ff7a45 100%);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.65rem 1.4rem;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 14px rgba(255,75,75,0.35);
    transition: all 0.18s ease;
    width: 100%;
}
div.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 26px rgba(255,75,75,0.55);
    color: white;
    border: none;
}
div.stButton > button:active {
    transform: translateY(0px) scale(0.98);
    box-shadow: 0 2px 8px rgba(255,75,75,0.4);
}

/* secondary-styled buttons via key prefix trick handled globally, all buttons share base gradient */

/* ---------- SIDEBAR: COMMAND CENTER ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10151c 0%, #0d1117 100%);
    border-right: 1px solid rgba(0,240,255,0.15);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.4rem;
}

.drx-cc-header {
    font-family: 'Poppins', sans-serif;
    font-weight: 900;
    font-size: 1.25rem;
    color: #00f0ff;
    text-shadow: 0 0 18px rgba(0,240,255,0.6);
    margin-bottom: 2px;
}
.drx-cc-sub {
    color: #6e7681;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.drx-profile-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
}

.drx-level-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ffd700, #ff9d00);
    color: #0d1117;
    font-weight: 900;
    font-size: 1.1rem;
    box-shadow: 0 0 20px rgba(255,215,0,0.5);
}

.xp-bar-container {
    width: 100%;
    height: 14px;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 8px;
    border: 1px solid rgba(255,255,255,0.08);
}
.xp-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #00f0ff, #ffd700);
    box-shadow: 0 0 12px rgba(0,240,255,0.7);
    transition: width 0.6s ease;
}

.drx-streak-box {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,75,75,0.08);
    border: 1px solid rgba(255,75,75,0.3);
    border-radius: 14px;
    padding: 12px 14px;
    margin-top: 10px;
}
.drx-streak-fire {
    font-size: 1.8rem;
    animation: flicker 1.4s infinite alternate;
}
@keyframes flicker {
    0%   { transform: scale(1) rotate(-2deg); filter: drop-shadow(0 0 4px #ff4b4b); }
    50%  { transform: scale(1.12) rotate(2deg); filter: drop-shadow(0 0 12px #ffd700); }
    100% { transform: scale(1) rotate(-1deg); filter: drop-shadow(0 0 6px #ff4b4b); }
}
.drx-streak-num {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.15rem;
    color: #ffb3b3;
}
.drx-streak-label {
    color: #8b949e;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.drx-archive-item {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #00f0ff;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
}
.drx-archive-title {
    font-weight: 700;
    font-size: 0.85rem;
    color: #e6edf3;
}
.drx-archive-date {
    font-size: 0.7rem;
    color: #6e7681;
}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: #00f0ff; }

/* ---------- MODULE FRAME (used around components.html iframes) ---------- */
.drx-module-frame {
    border-radius: 18px;
    border: 1px solid rgba(0,240,255,0.25);
    box-shadow: 0 0 30px rgba(0,240,255,0.12);
    overflow: hidden;
    margin-top: 6px;
}

/* ---------- METRIC PILLS ---------- */
.drx-pill-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px; }
.drx-pill {
    flex: 1;
    min-width: 90px;
    text-align: center;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 10px 6px;
}
.drx-pill-value {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.2rem;
    color: #ffd700;
}
.drx-pill-label {
    font-size: 0.65rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

hr.drx-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    margin: 18px 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "all_data" not in st.session_state:
    st.session_state.all_data = load_all_data()
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "current_quest" not in st.session_state:
    st.session_state.current_quest = None
if "quest_pool_key" not in st.session_state:
    st.session_state.quest_pool_key = None
if "current_vocab" not in st.session_state:
    st.session_state.current_vocab = random.choice(VOCAB_BANK)
if "current_chaos" not in st.session_state:
    st.session_state.current_chaos = random.choice(CHAOS_OPTIONS)
if "just_completed" not in st.session_state:
    st.session_state.just_completed = False

today = date.today()
is_weekend = today.weekday() >= 5
quest_pool = WEEKEND_QUESTS if is_weekend else WEEKDAY_QUESTS
day_type_label = "WEEKEND EXPEDITION" if is_weekend else "WEEKDAY MICRO-ESCAPE"

# ============================================================================
# SIDEBAR — PLAYER COMMAND CENTER
# ============================================================================
with st.sidebar:
    st.markdown('<div class="drx-cc-header">⚡ COMMAND CENTER</div>', unsafe_allow_html=True)
    st.markdown('<div class="drx-cc-sub">Player Profile Dashboard</div>', unsafe_allow_html=True)

    name_input = st.text_input("Player Name", value=st.session_state.player_name, placeholder="Enter your name...")
    if name_input != st.session_state.player_name:
        st.session_state.player_name = name_input
        st.session_state.current_quest = None

    if st.session_state.player_name:
        pname = st.session_state.player_name.strip()
        if pname not in st.session_state.all_data:
            st.session_state.all_data[pname] = default_player()
            save_all_data(st.session_state.all_data)

        player = st.session_state.all_data[pname]

        persona = st.selectbox(
            "Specialist Persona",
            PERSONAS,
            index=PERSONAS.index(player["persona"]) if player.get("persona") in PERSONAS else 0,
        )
        if persona != player.get("persona"):
            player["persona"] = persona
            save_all_data(st.session_state.all_data)

        level, progress_xp, percent = get_level_info(player["xp"])

        st.markdown('<div class="drx-profile-card">', unsafe_allow_html=True)
        profile_html = (
            '<div style="display:flex; align-items:center; gap:12px;">'
            '<div class="drx-level-badge">LV__LEVEL__</div>'
            '<div>'
            '<div style="font-weight:800; font-size:1.05rem; color:#f0f6fc;">__NAME__</div>'
            '<div style="font-size:0.78rem; color:#8b949e;">__PERSONA__</div>'
            '</div>'
            '</div>'
            '<div class="xp-bar-container"><div class="xp-bar-fill" style="width:__PERCENT__%;"></div></div>'
            '<div style="display:flex; justify-content:space-between; margin-top:4px;">'
            '<span style="font-size:0.72rem; color:#6e7681;">__PROGRESS__ / 100 XP</span>'
            '<span style="font-size:0.72rem; color:#6e7681;">Level __LEVEL__ / 10</span>'
            '</div>'
        )
        profile_html = (
            profile_html
            .replace("__LEVEL__", str(level))
            .replace("__NAME__", pname)
            .replace("__PERSONA__", player["persona"])
            .replace("__PERCENT__", str(percent))
            .replace("__PROGRESS__", str(progress_xp if level < 10 else 100))
        )
        st.markdown(profile_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        streak_html = (
            '<div class="drx-streak-box">'
            '<div class="drx-streak-fire">🔥</div>'
            '<div>'
            '<div class="drx-streak-num">__STREAK__ Days</div>'
            '<div class="drx-streak-label">Active Streak</div>'
            '</div>'
            '</div>'
        ).replace("__STREAK__", str(player["streak"]))
        st.markdown(streak_html, unsafe_allow_html=True)

        pill_html = (
            '<div class="drx-pill-row">'
            '<div class="drx-pill"><div class="drx-pill-value">__XP__</div><div class="drx-pill-label">Total XP</div></div>'
            '<div class="drx-pill"><div class="drx-pill-value">__DONE__</div><div class="drx-pill-label">Quests Done</div></div>'
            '</div>'
        ).replace("__XP__", str(player["xp"])).replace("__DONE__", str(player["total_completed"]))
        st.markdown(pill_html, unsafe_allow_html=True)

        st.markdown('<hr class="drx-divider">', unsafe_allow_html=True)
        st.markdown('<div class="drx-section-header">📜 Archive of Glory</div>', unsafe_allow_html=True)

        if player["archive"]:
            for entry in player["archive"][:12]:
                item_html = (
                    '<div class="drx-archive-item">'
                    '<div class="drx-archive-title">__EMOJI__ __TITLE__</div>'
                    '<div class="drx-archive-date">__DATE__ · __DAYTYPE__</div>'
                    '</div>'
                ).replace("__EMOJI__", entry.get("emoji", "⭐")) \
                 .replace("__TITLE__", entry["title"]) \
                 .replace("__DATE__", entry["date"]) \
                 .replace("__DAYTYPE__", entry.get("day_type", ""))
                st.markdown(item_html, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="color:#6e7681; font-size:0.85rem; font-style:italic;">No quests logged yet. Complete your first adventure to begin your archive!</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("👋 Enter your name above to activate your Command Center.")

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.markdown('<div class="drx-hero-title">🌅 DayRise Adventures</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="drx-hero-sub">Turn every ordinary day into a quest worth logging.</div>',
    unsafe_allow_html=True,
)

if not st.session_state.player_name:
    st.markdown(
        """
        <div class="drx-card drx-card-cyan">
            <div class="drx-quest-title">🎮 Welcome, Adventurer</div>
            <div class="drx-quest-desc">
                Set your name and persona in the Command Center on the left to unlock today's quest,
                start earning XP, and begin your Archive of Glory. Every day brings a brand new
                micro-adventure — weekdays are fast escapes, weekends are wild expeditions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

pname = st.session_state.player_name.strip()
player = st.session_state.all_data[pname]
today_str = today.isoformat()
already_completed_today = player.get("last_completed_date") == today_str

# --- generate / persist today's quest in session ---
pool_key = f"{pname}-{today_str}"
if st.session_state.quest_pool_key != pool_key or st.session_state.current_quest is None:
    st.session_state.current_quest = random.choice(quest_pool)
    st.session_state.quest_pool_key = pool_key

quest = st.session_state.current_quest

tag_class = "drx-tag-weekend" if is_weekend else "drx-tag-weekday"
card_class = "drx-card-coral" if is_weekend else "drx-card-cyan"

col_main, col_actions = st.columns([3, 1])

with col_main:
    quest_card_html = (
        '<div class="drx-card __CARDCLASS__">'
        '<span class="drx-tag __TAGCLASS__">__DAYTYPE__</span>'
        '<div class="drx-quest-title">__EMOJI__ __TITLE__</div>'
        '<div class="drx-quest-desc">__DESC__</div>'
        '</div>'
    )
    quest_card_html = (
        quest_card_html
        .replace("__CARDCLASS__", card_class)
        .replace("__TAGCLASS__", tag_class)
        .replace("__DAYTYPE__", day_type_label)
        .replace("__EMOJI__", quest["emoji"])
        .replace("__TITLE__", quest["title"])
        .replace("__DESC__", quest["desc"])
    )
    st.markdown(quest_card_html, unsafe_allow_html=True)

with col_actions:
    if st.button("🔀 Reroll Quest"):
        new_quest = random.choice(quest_pool)
        tries = 0
        while new_quest["title"] == quest["title"] and tries < 8:
            new_quest = random.choice(quest_pool)
            tries += 1
        st.session_state.current_quest = new_quest
        st.rerun()

    if already_completed_today:
        st.success("✅ Completed today!")
    else:
        if st.button("🏁 Complete Quest (+25 XP)"):
            yesterday_str = (today - timedelta(days=1)).isoformat()
            if player.get("last_completed_date") == yesterday_str:
                player["streak"] = player.get("streak", 0) + 1
            else:
                player["streak"] = 1
            player["last_completed_date"] = today_str
            player["xp"] = player.get("xp", 0) + 25
            player["level"] = get_level_info(player["xp"])[0]
            player["total_completed"] = player.get("total_completed", 0) + 1
            player.setdefault("archive", []).insert(0, {
                "date": today_str,
                "title": quest["title"],
                "emoji": quest["emoji"],
                "category": quest["category"],
                "day_type": "Weekend" if is_weekend else "Weekday",
            })
            save_all_data(st.session_state.all_data)
            st.session_state.just_completed = True
            st.balloons()
            st.rerun()

if st.session_state.just_completed:
    st.markdown(
        """
        <div class="drx-card drx-card-gold">
            <div class="drx-quest-title">🏆 Quest Complete!</div>
            <div class="drx-quest-desc">+25 XP banked, your streak is glowing, and your Archive of Glory just grew.
            Come back tomorrow for a brand new adventure.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.just_completed = False

st.markdown('<hr class="drx-divider">', unsafe_allow_html=True)

# ============================================================================
# INTERACTIVE MODULES — RENDERED BASED ON QUEST CATEGORY
# ============================================================================
category = quest["category"]

st.markdown('<div class="drx-section-header">🧩 Interactive Adventure Module</div>', unsafe_allow_html=True)

if category == "language":
    vocab = st.session_state.current_vocab
    vocab_html = (
        '<div class="drx-card drx-card-cyan">'
        '<span class="drx-tag drx-tag-weekday">🗣️ POLYGLOT CORE</span>'
        '<div style="display:flex; align-items:center; gap:10px;">'
        '<div style="font-size:2rem;">__FLAG__</div>'
        '<div>'
        '<div style="font-size:0.75rem; color:#8b949e; text-transform:uppercase; letter-spacing:1px;">__LANG__</div>'
        '<div class="drx-quest-title" style="margin-bottom:2px;">__WORD__</div>'
        '</div>'
        '</div>'
        '<div style="margin-top:14px; padding:14px; background:rgba(0,240,255,0.06); border-radius:12px; border:1px solid rgba(0,240,255,0.25);">'
        '<div style="font-size:0.72rem; color:#00f0ff; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">🔊 Read Aloud Guide</div>'
        '<div style="font-family:\'Poppins\',sans-serif; font-weight:800; font-size:1.3rem; color:#00f0ff; text-shadow:0 0 14px rgba(0,240,255,0.6);">__PRON__</div>'
        '</div>'
        '<div class="drx-quest-desc" style="margin-top:14px; font-style:italic;">"__MEANING__"</div>'
        '</div>'
    )
    vocab_html = (
        vocab_html
        .replace("__FLAG__", vocab["flag"])
        .replace("__LANG__", vocab["language"])
        .replace("__WORD__", vocab["word"])
        .replace("__PRON__", vocab["pronunciation"])
        .replace("__MEANING__", vocab["meaning"])
    )
    st.markdown(vocab_html, unsafe_allow_html=True)
    if st.button("🔁 Shuffle Vocabulary Word"):
        st.session_state.current_vocab = random.choice(VOCAB_BANK)
        st.rerun()

elif category == "art":
    st.markdown(
        '<div class="drx-card drx-card-gold"><span class="drx-tag drx-tag-weekend">🎨 ZEN PAINTING DECK</span>'
        '<div class="drx-quest-desc">Pick a neon brush, choose your size, and sketch freely over the guide outline below.</div></div>',
        unsafe_allow_html=True,
    )
    PAINT_HTML = """
    <div style="background:#0d1117; padding:14px; font-family:Inter,sans-serif;">
      <div id="toolbar" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
        <span style="color:#8b949e; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Brush:</span>
        <button onclick="setColor('#ff4b4b')" style="width:28px;height:28px;border-radius:50%;border:2px solid white;background:#ff4b4b;cursor:pointer;box-shadow:0 0 10px #ff4b4b;"></button>
        <button onclick="setColor('#00f0ff')" style="width:28px;height:28px;border-radius:50%;border:2px solid white;background:#00f0ff;cursor:pointer;box-shadow:0 0 10px #00f0ff;"></button>
        <button onclick="setColor('#ffd700')" style="width:28px;height:28px;border-radius:50%;border:2px solid white;background:#ffd700;cursor:pointer;box-shadow:0 0 10px #ffd700;"></button>
        <button onclick="setColor('#7CFC00')" style="width:28px;height:28px;border-radius:50%;border:2px solid white;background:#7CFC00;cursor:pointer;box-shadow:0 0 10px #7CFC00;"></button>
        <button onclick="setColor('#ffffff')" style="width:28px;height:28px;border-radius:50%;border:2px solid white;background:#ffffff;cursor:pointer;box-shadow:0 0 10px #ffffff;"></button>
        <span style="color:#8b949e; font-size:0.75rem; margin-left:12px;">Size:</span>
        <input type="range" min="2" max="24" value="6" id="brushSize" style="width:100px;">
        <button onclick="clearCanvas()" style="background:linear-gradient(135deg,#ff4b4b,#ff7a45); color:white; border:none; padding:6px 14px; border-radius:10px; font-weight:700; cursor:pointer;">Clear</button>
      </div>
      <canvas id="zenCanvas" width="760" height="420" style="width:100%; max-width:760px; border-radius:14px; background:#161b22; border:1px solid rgba(255,255,255,0.1); touch-action:none; cursor:crosshair;"></canvas>
    </div>
    <script>
      const canvas = document.getElementById('zenCanvas');
      const ctx = canvas.getContext('2d');
      let drawing = false;
      let currentColor = '#00f0ff';
      let lastX = 0, lastY = 0;

      function drawGuide() {
        ctx.clearRect(0,0,canvas.width, canvas.height);
        ctx.strokeStyle = 'rgba(255,255,255,0.18)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(150, 210, 90, 0, Math.PI*2);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(150, 120); ctx.lineTo(150, 300);
        ctx.moveTo(60, 210); ctx.lineTo(240, 210);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(320, 340);
        ctx.lineTo(440, 160);
        ctx.lineTo(520, 260);
        ctx.lineTo(620, 100);
        ctx.lineTo(720, 340);
        ctx.stroke();
      }
      drawGuide();

      function setColor(c) { currentColor = c; }
      function clearCanvas() { drawGuide(); }

      function getPos(e) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        if (e.touches && e.touches.length > 0) {
          return { x: (e.touches[0].clientX - rect.left) * scaleX, y: (e.touches[0].clientY - rect.top) * scaleY };
        }
        return { x: (e.clientX - rect.left) * scaleX, y: (e.clientY - rect.top) * scaleY };
      }

      function startDraw(e) {
        drawing = true;
        const pos = getPos(e);
        lastX = pos.x; lastY = pos.y;
      }
      function endDraw() { drawing = false; }
      function draw(e) {
        if (!drawing) return;
        e.preventDefault();
        const pos = getPos(e);
        const size = document.getElementById('brushSize').value;
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = size;
        ctx.lineCap = 'round';
        ctx.shadowBlur = 12;
        ctx.shadowColor = currentColor;
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
        lastX = pos.x; lastY = pos.y;
      }

      canvas.addEventListener('mousedown', startDraw);
      canvas.addEventListener('mouseup', endDraw);
      canvas.addEventListener('mouseout', endDraw);
      canvas.addEventListener('mousemove', draw);
      canvas.addEventListener('touchstart', startDraw);
      canvas.addEventListener('touchend', endDraw);
      canvas.addEventListener('touchmove', draw);
    </script>
    """
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(PAINT_HTML, height=520, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

elif category == "mindfulness":
    st.markdown(
        '<div class="drx-card drx-card-cyan"><span class="drx-tag drx-tag-weekday">⏱️ MIND-SYNC TIMER</span>'
        '<div class="drx-quest-desc">Start the 3-minute breathing pause and let your mind reset before the next move.</div></div>',
        unsafe_allow_html=True,
    )
    TIMER_HTML = """
    <div style="background:#0d1117; padding:24px; border-radius:16px; text-align:center; font-family:Inter,sans-serif;">
      <div id="display" style="font-family:'Poppins',sans-serif; font-size:4rem; font-weight:900; color:#00f0ff; text-shadow:0 0 26px rgba(0,240,255,0.7); letter-spacing:2px;">03:00</div>
      <div style="margin-top:14px; display:flex; justify-content:center; gap:12px;">
        <button onclick="startTimer()" style="background:linear-gradient(135deg,#00f0ff,#0090ff); color:#0d1117; border:none; padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer; box-shadow:0 0 16px rgba(0,240,255,0.4);">▶ Start</button>
        <button onclick="pauseTimer()" style="background:rgba(255,255,255,0.08); color:#e6edf3; border:1px solid rgba(255,255,255,0.2); padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">⏸ Pause</button>
        <button onclick="resetTimer()" style="background:rgba(255,255,255,0.08); color:#e6edf3; border:1px solid rgba(255,255,255,0.2); padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">↺ Reset</button>
      </div>
      <div id="celebration" style="margin-top:18px; font-size:1.4rem; font-weight:800; color:#ffd700; text-shadow:0 0 16px rgba(255,215,0,0.6); display:none;">
        🎉 Beautifully done. You're centered. 🎉
      </div>
    </div>
    <script>
      let totalSeconds = 180;
      let remaining = totalSeconds;
      let intervalId = null;

      function render() {
        const m = Math.floor(remaining / 60).toString().padStart(2,'0');
        const s = (remaining % 60).toString().padStart(2,'0');
        document.getElementById('display').innerText = m + ':' + s;
      }

      function startTimer() {
        if (intervalId) return;
        intervalId = setInterval(() => {
          if (remaining > 0) {
            remaining -= 1;
            render();
          } else {
            clearInterval(intervalId);
            intervalId = null;
            document.getElementById('celebration').style.display = 'block';
            document.getElementById('display').style.color = '#ffd700';
            document.getElementById('display').style.textShadow = '0 0 26px rgba(255,215,0,0.8)';
          }
        }, 1000);
      }
      function pauseTimer() {
        if (intervalId) { clearInterval(intervalId); intervalId = null; }
      }
      function resetTimer() {
        pauseTimer();
        remaining = totalSeconds;
        document.getElementById('celebration').style.display = 'none';
        document.getElementById('display').style.color = '#00f0ff';
        document.getElementById('display').style.textShadow = '0 0 26px rgba(0,240,255,0.7)';
        render();
      }
      render();
    </script>
    """
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(TIMER_HTML, height=280, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

elif category == "chaos":
    opt1, opt2 = st.session_state.current_chaos
    st.markdown(
        '<div class="drx-card drx-card-coral"><span class="drx-tag drx-tag-weekend">🪙 THE DESTINY FLIP</span>'
        '<div class="drx-quest-desc">Let fate resolve your decision paralysis. Tap the coin to flip it.</div></div>',
        unsafe_allow_html=True,
    )
    COIN_HTML = """
    <div style="background:#0d1117; padding:24px; text-align:center; font-family:Inter,sans-serif;">
      <div style="display:flex; justify-content:space-around; margin-bottom:18px; color:#8b949e; font-weight:700; font-size:0.85rem;">
        <div>🅰️ __OPT1__</div>
        <div>🅱️ __OPT2__</div>
      </div>
      <div id="scene" style="perspective:600px; display:flex; justify-content:center;">
        <div id="coin" onclick="flipCoin()" style="width:120px; height:120px; border-radius:50%; position:relative; transform-style:preserve-3d; transition:transform 1.1s cubic-bezier(.2,.8,.2,1); cursor:pointer; background:radial-gradient(circle at 35% 30%, #ffe97a, #ffd700 60%, #b8860b 100%); box-shadow:0 0 30px rgba(255,215,0,0.55); display:flex; align-items:center; justify-content:center; font-size:2.2rem;">🪙</div>
      </div>
      <div id="result" style="margin-top:20px; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.5rem; color:#ff8080; text-shadow:0 0 16px rgba(255,75,75,0.6); min-height:2rem;"></div>
      <button onclick="flipCoin()" style="margin-top:10px; background:linear-gradient(135deg,#ff4b4b,#ff7a45); color:white; border:none; padding:10px 24px; border-radius:12px; font-weight:800; cursor:pointer; box-shadow:0 0 16px rgba(255,75,75,0.4);">Flip the Coin</button>
    </div>
    <script>
      const options = ["__OPT1__", "__OPT2__"];
      let spins = 0;
      function flipCoin() {
        spins += 1;
        const coin = document.getElementById('coin');
        const extraTurns = 4 + Math.floor(Math.random()*3);
        const finalIndex = Math.random() < 0.5 ? 0 : 1;
        const finalAngle = extraTurns * 360 + (finalIndex === 0 ? 0 : 180);
        coin.style.transform = 'rotateY(' + finalAngle + 'deg)';
        document.getElementById('result').innerText = '';
        setTimeout(() => {
          document.getElementById('result').innerText = '✨ ' + options[finalIndex] + ' ✨';
        }, 1150);
      }
    </script>
    """
    COIN_HTML = COIN_HTML.replace("__OPT1__", opt1).replace("__OPT2__", opt2)
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(COIN_HTML, height=340, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔁 New Dilemma"):
        st.session_state.current_chaos = random.choice(CHAOS_OPTIONS)
        st.rerun()

else:
    st.markdown(
        '<div class="drx-card drx-card-gold"><span class="drx-tag drx-tag-weekend">⭐ FREESTYLE QUEST</span>'
        '<div class="drx-quest-desc">This adventure runs on pure willpower — no gadgets required. '
        'Just commit, execute, and log it in your Archive of Glory when you\'re done.</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="drx-divider">', unsafe_allow_html=True)

# ============================================================================
# MOBILE NOTIFICATIONS
# ============================================================================
st.markdown('<div class="drx-section-header">🔔 Wake-Up Alerts</div>', unsafe_allow_html=True)

NOTIF_HTML = """
<div style="background:#0d1117; padding:20px; border-radius:16px; font-family:Inter,sans-serif;">
  <div style="color:#c9d1d9; font-size:0.92rem; margin-bottom:14px;">
    Enable browser notifications so DayRise can ping you the moment a new quest drops.
  </div>
  <div style="display:flex; gap:12px; flex-wrap:wrap;">
    <button onclick="requestPerm()" style="background:linear-gradient(135deg,#00f0ff,#0090ff); color:#0d1117; border:none; padding:10px 20px; border-radius:12px; font-weight:800; cursor:pointer; box-shadow:0 0 16px rgba(0,240,255,0.4);">🔔 Enable Alerts</button>
    <button onclick="sendTest()" style="background:linear-gradient(135deg,#ffd700,#ff9d00); color:#0d1117; border:none; padding:10px 20px; border-radius:12px; font-weight:800; cursor:pointer; box-shadow:0 0 16px rgba(255,215,0,0.4);">📣 Send Test Notification</button>
  </div>
  <div id="notifStatus" style="margin-top:12px; font-size:0.85rem; color:#8b949e;"></div>
</div>
<script>
  function requestPerm() {
    if (!('Notification' in window)) {
      document.getElementById('notifStatus').innerText = 'This browser does not support notifications.';
      return;
    }
    Notification.requestPermission().then(function(perm) {
      document.getElementById('notifStatus').innerText = 'Permission: ' + perm;
    });
  }
  function sendTest() {
    if (!('Notification' in window)) {
      document.getElementById('notifStatus').innerText = 'This browser does not support notifications.';
      return;
    }
    if (Notification.permission === 'granted') {
      new Notification('🌅 DayRise Adventures', { body: "Today's quest is ready. Time to rise!" });
    } else {
      document.getElementById('notifStatus').innerText = 'Please enable alerts first.';
    }
  }
</script>
"""
st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
components.html(NOTIF_HTML, height=190, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📲 Integration Guide — Auto-Open on Your Lockscreen at 7:30 AM"):
    st.markdown(
        """
        <div class="drx-card drx-card-cyan">
            <div class="drx-quest-title">🍎 iOS Shortcuts Setup</div>
            <div class="drx-quest-desc">
                1. Deploy this app and copy its live URL.<br>
                2. Open the <b>Shortcuts</b> app → <b>Automation</b> tab → <b>+</b> → <b>Create Personal Automation</b>.<br>
                3. Choose <b>Time of Day</b> → set to <b>7:30 AM</b> → Daily.<br>
                4. Add action <b>Open App</b> → select <b>Safari</b>, or add <b>Open URL</b> with your DayRise link.<br>
                5. Turn off "Ask Before Running" so it fires automatically each morning.
            </div>
        </div>
        <div class="drx-card drx-card-coral">
            <div class="drx-quest-title">🤖 Android (MacroDroid / Tasker) Setup</div>
            <div class="drx-quest-desc">
                1. In <b>MacroDroid</b>, create a new macro.<br>
                2. Trigger: <b>Day/Time</b> → set to <b>7:30 AM</b>, repeat daily.<br>
                3. Action: <b>Launch Browser</b> or <b>Open URL</b> → paste your deployed DayRise URL.<br>
                4. Optional: chain a <b>Screen On</b> action beforehand so the phone wakes and slides open the app automatically.<br>
                5. Save and enable the macro — your quest will be ready the moment you wake up.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div style="text-align:center; color:#6e7681; font-size:0.8rem; margin-top:24px;">Rise. Quest. Repeat. 🌅</div>',
    unsafe_allow_html=True,
)
