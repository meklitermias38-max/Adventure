import streamlit as st
import streamlit.components.v1 as components
import random
import json
from datetime import date, timedelta

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="DayRise Adventures",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
# LIGHT AESTHETICS — VISUAL SHELL
# ============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Poppins', sans-serif;
}

/* ---------- LIGHT MODE APP BACKGROUND ---------- */
.stApp {
    background: radial-gradient(circle at 15% 0%, rgba(255,75,75,0.05) 0%, transparent 50%),
                radial-gradient(circle at 85% 15%, rgba(0,210,255,0.05) 0%, transparent 50%),
                #f8fafc;
    color: #1e293b;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* ---------- TYPOGRAPHY ---------- */
h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    color: #0f172a !important;
}

.drx-hero-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 900;
    font-size: 3rem;
    background: linear-gradient(90deg, #ff4b4b 0%, #ff9d00 50%, #00b4d8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
    line-height: 1.1;
}

.drx-hero-sub {
    color: #64748b;
    font-size: 1.05rem;
    font-weight: 500;
    margin-top: 4px;
    margin-bottom: 1.6rem;
}

.drx-section-header {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.3rem;
    color: #334155;
    margin: 24px 0 0.6rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ---------- BRIGHT ADVENTURE CARDS ---------- */
.drx-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.drx-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.08);
}

.drx-card-coral { border-top: 4px solid #ff4b4b; }
.drx-card-cyan { border-top: 4px solid #00b4d8; }
.drx-card-gold { border-top: 4px solid #ffbc00; }

.drx-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.drx-tag-weekday { background: #e0f7fa; color: #00838f; }
.drx-tag-weekend { background: #ffebee; color: #c62828; }

.drx-quest-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    margin-bottom: 8px;
    color: #1e293b;
}

.drx-quest-desc {
    color: #475569;
    font-size: 1rem;
    line-height: 1.6;
}

/* ---------- BUTTONS ---------- */
div.stButton > button {
    background: linear-gradient(135deg, #ff4b4b 0%, #ff7a45 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 4px 12px rgba(255,75,75,0.2);
    transition: all 0.15s ease;
    width: 100%;
}
div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(255,75,75,0.35);
    color: white;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.4rem;
}

.drx-cc-header {
    font-family: 'Poppins', sans-serif;
    font-weight: 900;
    font-size: 1.2rem;
    color: #0f172a;
    margin-bottom: 2px;
}
.drx-cc-sub {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.drx-profile-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
}

.drx-archive-item {
    background: #f8fafc;
    border-left: 3px solid #00b4d8;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 8px;
    border-top: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
}
.drx-archive-title {
    font-weight: 700;
    font-size: 0.85rem;
    color: #334155;
}
.drx-archive-date {
    font-size: 0.7rem;
    color: #64748b;
}

.drx-module-frame {
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    overflow: hidden;
    margin-top: 6px;
    background: #ffffff;
}

hr.drx-divider {
    border: none;
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================================
# BROWSER COOKIES / LOCALSTORAGE SYNC CONTROLLER
# ============================================================================
query_params = st.query_params

if "player_name" not in st.session_state:
    st.session_state.player_name = query_params.get("saved_name", "")
if "archive_data" not in st.session_state:
    try:
        st.session_state.archive_data = json.loads(query_params.get("saved_archive", "[]"))
    except:
        st.session_state.archive_data = []
if "persona" not in st.session_state:
    st.session_state.persona = query_params.get("saved_persona", "Urban Explorer 🌃")

def sync_browser_storage(name, persona, archive):
    archive_json = json.dumps(archive)
    js_code = f"""
    <script>
    const parentUrl = new URL(window.parent.location.href);
    if (!parentUrl.searchParams.has("saved_name") && localStorage.getItem("drx_name")) {{
        parentUrl.searchParams.set("saved_name", localStorage.getItem("drx_name") || "");
        parentUrl.searchParams.set("saved_persona", localStorage.getItem("drx_persona") || "Urban Explorer 🌃");
        parentUrl.searchParams.set("saved_archive", localStorage.getItem("drx_archive") || "[]");
        window.parent.location.href = parentUrl.href;
    }}
    localStorage.setItem("drx_name", "{name}");
    localStorage.setItem("drx_persona", "{persona}");
    localStorage.setItem("drx_archive", `{archive_json}`);
    </script>
    """
    components.html(js_code, height=0, width=0)

sync_browser_storage(st.session_state.player_name, st.session_state.persona, st.session_state.archive_data)

# ============================================================================
# APP STATE INITIALIZATION
# ============================================================================
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
    st.markdown('<div class="drx-cc-header">☕ FREE SPACE</div>', unsafe_allow_html=True)
    st.markdown('<div class="drx-cc-sub">Your Mindful Dashboard</div>', unsafe_allow_html=True)

    name_input = st.text_input("Adventurer Name", value=st.session_state.player_name, placeholder="Enter your name to join...")
    if name_input != st.session_state.player_name:
        st.session_state.player_name = name_input
        st.query_params["saved_name"] = name_input
        st.rerun()

    if st.session_state.player_name:
        pname = st.session_state.player_name.strip()

        selected_persona = st.selectbox(
            "Current Persona",
            PERSONAS,
            index=PERSONAS.index(st.session_state.persona) if st.session_state.persona in PERSONAS else 0,
        )
        if selected_persona != st.session_state.persona:
            st.session_state.persona = selected_persona
            st.query_params["saved_persona"] = selected_persona
            st.rerun()

        st.markdown('<div class="drx-profile-card">', unsafe_allow_html=True)
        profile_html = (
            '<div style="display:flex; align-items:center; gap:12px;">'
            '<div>'
            '<div style="font-weight:800; font-size:1.1rem; color:#0f172a;">__NAME__</div>'
            '<div style="font-size:0.8rem; color:#64748b;">__PERSONA__</div>'
            '</div>'
            '</div>'
        ).replace("__NAME__", pname).replace("__PERSONA__", st.session_state.persona)
        st.markdown(profile_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr class="drx-divider">', unsafe_allow_html=True)
        st.markdown('<div class="drx-section-header">📜 Completed Quests</div>', unsafe_allow_html=True)

        if st.session_state.archive_data:
            for entry in st.session_state.archive_data[:12]:
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
                '<div style="color:#94a3b8; font-size:0.85rem; font-style:italic;">A clean slate. Finish an adventure to add it here.</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("👋 Type your name above to setup your persistent dashboard space.")

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.markdown('<div class="drx-hero-title">🌅 DayRise Adventures</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="drx-hero-sub">Turn every ordinary day into a quest worth logging. No scores, just presence.</div>',
    unsafe_allow_html=True,
)

if not st.session_state.player_name:
    st.markdown(
        """
        <div class="drx-card drx-card-cyan">
            <div class="drx-quest-title">👋 Welcome to DayRise</div>
            <div class="drx-quest-desc">
                Set your name in the sidebar to reveal today's quest. 
                Everything is kept inside your local browser memory, making it your private personal sanctuary.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

pname = st.session_state.player_name.strip()
today_str = today.isoformat()

already_completed_today = any(item.get("date") == today_str for item in st.session_state.archive_data)

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
        while new_quest["title"] == quest["title"]:
            new_quest = random.choice(quest_pool)
        st.session_state.current_quest = new_quest
        st.rerun()

    if already_completed_today:
        st.success("✅ Logged for today!")
    else:
        if st.button("🏁 Log Complete"):
            new_archive = list(st.session_state.archive_data)
            new_archive.insert(0, {
                "date": today_str,
                "title": quest["title"],
                "emoji": quest["emoji"],
                "category": quest["category"],
                "day_type": "Weekend" if is_weekend else "Weekday",
            })
            st.session_state.archive_data = new_archive
            st.query_params["saved_archive"] = json.dumps(new_archive)
            st.session_state.just_completed = True
            st.rerun()

# --- CONFETTI EXPLOSION TRIGGER ---
if st.session_state.just_completed:
    CONFETTI_JS = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
        window.parent.confetti({
            particleCount: 180,
            spread: 85,
            origin: { y: 0.6 },
            colors: ['#ff4b4b', '#ffbc00', '#00b4d8', '#4caf50', '#ff7a45']
        });
    </script>
    """
    components.html(CONFETTI_JS, height=0, width=0)
    st.markdown(
        """
        <div class="drx-card drx-card-gold">
            <div class="drx-quest-title">🏆 Adventure Logged!</div>
            <div class="drx-quest-desc">This task has been recorded into your local browser log. See you tomorrow!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.just_completed = False

st.markdown('<hr class="drx-divider">', unsafe_allow_html=True)

# ============================================================================
# INTERACTIVE MODULES — LIGHT THEME INTERFACES
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
        '<div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">__LANG__</div>'
        '<div class="drx-quest-title" style="margin-bottom:2px;">__WORD__</div>'
        '</div>'
        '</div>'
        '<div style="margin-top:14px; padding:14px; background:#f0fdfa; border-radius:12px; border:1px solid #b2f2bb;">'
        '<div style="font-size:0.72rem; color:#0e7490; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">🔊 Read Aloud Guide</div>'
        '<div style="font-family:\'Poppins\',sans-serif; font-weight:800; font-size:1.3rem; color:#0e7490;">__PRON__</div>'
        '</div>'
        '<div class="drx-quest-desc" style="margin-top:14px; font-style:italic; color:#334155;">"__MEANING__"</div>'
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
        '<div class="drx-quest-desc">Pick a vibrant neon tone, alter your brush width, and doodle cleanly across the canvas guide layout.</div></div>',
        unsafe_allow_html=True,
    )
    PAINT_HTML = """
    <div style="background:#ffffff; padding:14px; font-family:Inter,sans-serif;">
      <div id="toolbar" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
        <span style="color:#64748b; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Brush:</span>
        <button onclick="setColor('#ff4b4b')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#ff4b4b;cursor:pointer;box-shadow:0 0 6px #ff4b4b;"></button>
        <button onclick="setColor('#00b4d8')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#00b4d8;cursor:pointer;box-shadow:0 0 6px #00b4d8;"></button>
        <button onclick="setColor('#ffbc00')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#ffbc00;cursor:pointer;box-shadow:0 0 6px #ffbc00;"></button>
        <button onclick="setColor('#4caf50')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#4caf50;cursor:pointer;box-shadow:0 0 6px #4caf50;"></button>
        <button onclick="setColor('#1e293b')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#1e293b;cursor:pointer;box-shadow:0 0 6px #1e293b;"></button>
        <span style="color:#64748b; font-size:0.75rem; margin-left:12px;">Size:</span>
        <input type="range" min="2" max="24" value="6" id="brushSize" style="width:100px;">
        <button onclick="clearCanvas()" style="background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1; padding:6px 14px; border-radius:10px; font-weight:700; cursor:pointer;">Clear</button>
      </div>
      <canvas id="zenCanvas" width="760" height="420" style="width:100%; max-width:760px; border-radius:14px; background:#f8fafc; border:1px solid #e2e8f0; touch-action:none; cursor:crosshair;"></canvas>
    </div>
    <script>
      const canvas = document.getElementById('zenCanvas');
      const ctx = canvas.getContext('2d');
      let drawing = false;
      let currentColor = '#00b4d8';
      let lastX = 0, lastY = 0;

      function drawGuide() {
        ctx.clearRect(0,0,canvas.width, canvas.height);
        ctx.strokeStyle = 'rgba(148, 163, 184, 0.25)';
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
        '<div class="drx-quest-desc">Start the 3-minute breathing break to align your target intentions.</div></div>',
        unsafe_allow_html=True,
    )
    TIMER_HTML = """
    <div style="background:#ffffff; padding:24px; border-radius:16px; text-align:center; font-family:Inter,sans-serif;">
      <div id="display" style="font-family:'Poppins',sans-serif; font-size:4rem; font-weight:900; color:#00b4d8; letter-spacing:2px;">03:00</div>
      <div style="margin-top:14px; display:flex; justify-content:center; gap:12px;">
        <button onclick="startTimer()" style="background:#00b4d8; color:#fff; border:none; padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">▶ Start</button>
        <button onclick="pauseTimer()" style="background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1; padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">⏸ Pause</button>
        <button onclick="resetTimer()" style="background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1; padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">↺ Reset</button>
      </div>
      <div id="celebration" style="margin-top:18px; font-size:1.2rem; font-weight:800; color:#ffbc00; display:none;">
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
            document.getElementById('display').style.color = '#ffbc00';
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
        document.getElementById('display').style.color = '#00b4d8';
        render();
      }
      render();
    </script>
    """
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(TIMER_HTML, height=260, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

elif category == "chaos":
    opt1, opt2 = st.session_state.current_chaos
    st.markdown(
        '<div class="drx-card drx-card-coral"><span class="drx-tag drx-tag-weekend">🪙 THE DESTINY FLIP</span>'
        '<div class="drx-quest-desc">Let random design choices solve minor mental lockups. Tap below to spin.</div></div>',
        unsafe_allow_html=True,
    )
    COIN_HTML = """
    <div style="background:#ffffff; padding:24px; text-align:center; font-family:Inter,sans-serif;">
      <div style="display:flex; justify-content:space-around; margin-bottom:18px; color:#64748b; font-weight:700; font-size:0.85rem;">
        <div>🅰️ __OPT1__</div>
        <div>🅱️ __OPT2__</div>
      </div>
      <div id="scene" style="perspective:600px; display:flex; justify-content:center;">
        <div id="coin" onclick="flipCoin()" style="width:100px; height:100px; border-radius:50%; position:relative; transform-style:preserve-3d; transition:transform 1.1s cubic-bezier(.2,.8,.2,1); cursor:pointer; background:radial-gradient(circle at 35% 30%, #fff3b0, #ffbc00 70%, #d4a373 100%); box-shadow:0 4px 10px rgba(0,0,0,0.1); display:flex; align-items:center; justify-content:center; font-size:2rem;">🪙</div>
      </div>
      <div id="result" style="margin-top:20px; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.4rem; color:#ff4b4b; min-height:2rem;"></div>
      <button onclick="flipCoin()" style="margin-top:10px; background:#ff4b4b; color:white; border:none; padding:10px 24px; border-radius:12px; font-weight:800; cursor:pointer; box-shadow:0 4px 12px rgba(255,75,75,0.2);">Flip the Coin</button>
    </div>
    <script>
      const options = ["__OPT1__", "__OPT2__"];
      function flipCoin() {
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

st.markdown(
    '<div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:40px;">Rise. Quest. Repeat. 🌅</div>',
    unsafe_allow_html=True,
)
