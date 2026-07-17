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
# EXPANDED QUEST BANKS (ADDED DANCE, PLAYFULNESS, AND EXPEDITIONS)
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
    {"title": "The Kitchen Counter Dance-Off", "desc": "While waiting for your morning coffee or water to boil, clear a 3-foot space and execute an uninhibited, energetic 45-second solo dance routine. Nobody is watching.", "category": "dance", "emoji": "💃"},
    {"title": "The Secret Agent Walk", "desc": "Match your steps precisely to the rhythm of whatever upbeat track is in your head right now. Navigate your next walk like you are the lead character in a high-stakes film.", "category": "dance", "emoji": "🕺"},
    {"title": "The Soundscape Symphony", "desc": "Close your eyes for 60 seconds anywhere you are. Isolate the highest pitch sound and the lowest bass sound around you. Treat it like a musical composition.", "category": "sensory", "emoji": "🎵"},
    {"title": "The 5-Minute Declutter Blitz", "desc": "Set a 5-minute timer and clear one chaotic surface — your desk, bag, or car. Stop the instant the timer ends.", "category": "physical", "emoji": "🧹"},
]

WEEKEND_QUESTS = [
    {"title": "The Horizon Hunter", "desc": "Find the highest accessible point near you — a hill, rooftop, parking garage — and watch the horizon for ten full minutes, no phone.", "category": "physical", "emoji": "🌄"},
    {"title": "The Neighborhood Grid-Run", "desc": "Pick a direction and walk exactly six blocks in a square pattern, turning only right. Map what you discover.", "category": "physical", "emoji": "🗺️"},
    {"title": "The Analog Solo Trek", "desc": "Go for a walk or hike with zero devices except a watch. Bring only a small notebook to jot down thoughts.", "category": "mindfulness", "emoji": "🥾"},
    {"title": "The Farmers Market Linguist", "desc": "Visit a market or store and use today's foreign vocabulary word while chatting with a vendor about their produce.", "category": "language", "emoji": "🧺"},
    {"title": "The Sketchbook Summit", "desc": "Find a scenic spot and sketch what you see for fifteen minutes using the Zen Painting Deck or real paper — no erasing allowed.", "category": "art", "emoji": "🖌️"},
    {"title": "The Midnight Dance Ritual", "desc": "Turn off all the lights in a room, queue up a song with a heavy bassline, and move your body strictly based on what feels right in the pitch dark. No choreography allowed.", "category": "dance", "emoji": "🌌"},
    {"title": "The Flavor Alchemist", "desc": "Bake or cook something simple today, but consciously swap out one foundational sugar, spice, or base liquid for a dynamic, experimental alternative you have in your cupboards.", "category": "creative", "emoji": "🍪"},
    {"title": "The Coin Toss Explorer", "desc": "At every unplanned fork in your day, let the Destiny Flip choose your direction. Follow it for at least three decisions.", "category": "chaos", "emoji": "🪙"},
    {"title": "The Urban Photography Safari", "desc": "Shoot ten photos of things people usually walk past — textures, shadows, forgotten signage. Curate your best three.", "category": "art", "emoji": "📸"},
    {"title": "The Secondhand Treasure Dive", "desc": "Visit a thrift store or flea market and find one object under $10 that tells an imaginary story you invent on the spot.", "category": "creative", "emoji": "🕵️"},
    {"title": "The Street Food Gambler", "desc": "Order a dish you've never tried from a place you've never visited. Rate it on taste, risk, and surprise.", "category": "sensory", "emoji": "🌮"},
    {"title": "The Park Bench Philosopher", "desc": "Sit on a public bench for twenty minutes and write down every question that crosses your mind, no matter how strange.", "category": "mindfulness", "emoji": "🪑"},
    {"title": "The Cloud Shape Cartographer", "desc": "Lie down outside and map five cloud shapes into a tiny story connecting them all.", "category": "creative", "emoji": "☁️"},
    {"title": "The Silent Retreat Hour", "desc": "Spend one full hour in total intentional silence — no music, talking, or scrolling. Notice how your mind behaves by minute 40.", "category": "mindfulness", "emoji": "🤫"},
    {"title": "The Waterfront Wanderer", "desc": "Find any body of water nearby — river, lake, fountain, coast — and spend ten minutes just watching it move.", "category": "mindfulness", "emoji": "🌊"},
]

VOCAB_BANK = [
    {"language": "Spanish", "flag": "🇪🇸", "word": "Duende", "meaning": "A heightened state of raw emotion and authenticity, especially felt during art or performance.", "pronunciation": "dwen-deh"},
    {"language": "Amharic", "flag": "🇪🇹", "word": "Buna", "meaning": "Coffee — but truly a ceremony of slowing down and connecting with the people around you.", "pronunciation": "boo-nah"},
    {"language": "Japanese", "flag": "🇯🇵", "word": "Komorebi", "meaning": "The dappled sunlight that filters through leaves in a forest canopy.", "pronunciation": "koh-moh-reh-bee"},
    {"language": "French", "flag": "🇫🇷", "word": "Dépaysement", "meaning": "The disorienting, alive feeling of being somewhere unfamiliar, outside your usual context.", "pronunciation": "day-pay-eez-mahn"},
    {"language": "Portuguese", "flag": "🇵🇹", "word": "Saudade", "meaning": "A deep, bittersweet longing for someone or something absent, tinged with love.", "pronunciation": "sow-dah-jee"},
    {"language": "German", "flag": "🇩🇪", "word": "Waldeinsamkeit", "meaning": "The peaceful feeling of being alone in the woods, connected to nature.", "pronunciation": "vald-ine-zahm-kite"},
]

CHAOS_OPTIONS = [
    ("Turn Left", "Turn Right"),
    ("Order something new", "Stick to the classics"),
    ("Take the stairs", "Take the elevator"),
    ("Say yes immediately", "Say no gently"),
    ("The scenic route", "The fastest route"),
]

PERSONAS = [
    "Urban Explorer 🌃",
    "Chaos Monk 🧘",
    "Creative Renegade 🎨",
    "Polyglot Nomad 🗺️",
]

# ============================================================================
# LIGHT AESTHETICS & CUSTOM CSS
# ============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Poppins', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 15% 0%, rgba(255,75,75,0.05) 0%, transparent 50%),
                radial-gradient(circle at 85% 15%, rgba(0,210,255,0.05) 0%, transparent 50%),
                #f8fafc;
    color: #1e293b;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 800 !important;
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

.drx-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.drx-card-coral { border-top: 4px solid #ff4b4b; }
.drx-card-cyan { border-top: 4px solid #00b4d8; }
.drx-card-gold { border-top: 4px solid #ffbc00; }
.drx-card-purple { border-top: 4px solid #9c27b0; }

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

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}

.drx-profile-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 16px;
}

.drx-archive-item {
    background: #f8fafc;
    border-left: 3px solid #00b4d8;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 8px;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #00b4d8;
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

# Reveal States
if "quest_revealed" not in st.session_state:
    st.session_state.quest_revealed = False

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
        profile_html = f"""
        <div style="display:flex; align-items:center; gap:12px;">
            <div>
                <div style="font-weight:800; font-size:1.1rem; color:#0f172a;">{pname}</div>
                <div style="font-size:0.8rem; color:#64748b;">{st.session_state.persona}</div>
            </div>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr class="drx-divider">', unsafe_allow_html=True)
        st.markdown('<div class="drx-section-header">📜 Completed Quests</div>', unsafe_allow_html=True)

        if st.session_state.archive_data:
            for entry in st.session_state.archive_data[:12]:
                item_html = f"""
                <div class="drx-archive-item">
                    <div class="drx-archive-title">{entry.get('emoji', '⭐')} {entry['title']}</div>
                    <div class="drx-archive-date">{entry['date']} · {entry.get('day_type', '')}</div>
                </div>
                """
                st.markdown(item_html, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#94a3b8; font-size:0.85rem; font-style:italic;">A clean slate. Finish an adventure to add it here.</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Type your name above to setup your persistent dashboard space.")

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.markdown('<div class="drx-hero-title">🌅 DayRise Adventures</div>', unsafe_allow_html=True)
st.markdown('<div class="drx-hero-sub">Turn every ordinary day into a quest worth logging. No scores, just presence.</div>', unsafe_allow_html=True)

if not st.session_state.player_name:
    st.markdown("""
        <div class="drx-card drx-card-cyan">
            <div class="drx-quest-title">👋 Welcome to DayRise</div>
            <div class="drx-quest-desc">Set your name in the sidebar to reveal today's quest.</div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

pname = st.session_state.player_name.strip()
today_str = today.isoformat()

already_completed_today = any(item.get("date") == today_str for item in st.session_state.archive_data)

pool_key = f"{pname}-{today_str}"
if st.session_state.quest_pool_key != pool_key or st.session_state.current_quest is None:
    st.session_state.current_quest = random.choice(quest_pool)
    st.session_state.quest_pool_key = pool_key
    st.session_state.quest_revealed = False  # Reset reveal frame for new day

quest = st.session_state.current_quest

# Category Theme Color Router
category = quest["category"]
if category == "dance":
    card_class = "drx-card-purple"
elif is_weekend:
    card_class = "drx-card-coral"
else:
    card_class = "drx-card-cyan"

tag_class = "drx-tag-weekend" if is_weekend else "drx-tag-weekday"

# ============================================================================
# INTERACTIVE DICE ROLLER / TAP TO REVEAL CONTROLLER
# ============================================================================
if not st.session_state.quest_revealed and not already_completed_today:
    st.markdown('<div class="drx-section-header">🎲 Today\'s Quest Uncharted</div>', unsafe_allow_html=True)
    
    DICE_HTML = """
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:20px; padding:40px; text-align:center; box-shadow:0 4px 6px -1px rgba(0,0,0,0.05);">
        <div id="dice-graphic" style="font-size:5.5rem; cursor:pointer; display:inline-block; transition: transform 0.6s ease;">🎲</div>
        <div style="font-family:'Poppins', sans-serif; font-weight:800; font-size:1.4rem; color:#1e293b; margin-top:15px;">Tap or Roll to Discover Today's Adventure</div>
        <div style="color:#64748b; font-size:0.92rem; margin-bottom:20px;">Ready to see where your intuition takes you?</div>
    </div>
    <script>
        const dice = document.getElementById('dice-graphic');
        const faces = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
        dice.addEventListener('click', () => {
            let count = 0;
            const interval = setInterval(() => {
                dice.style.transform = 'rotate(' + (count * 45) + 'deg) scale(1.1)';
                dice.innerText = faces[Math.floor(Math.random() * faces.length)];
                count++;
                if(count > 10) {
                    clearInterval(interval);
                    dice.style.transform = 'rotate(0deg) scale(1)';
                    dice.innerText = '✨';
                }
            }, 60);
        });
    </script>
    """
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(DICE_HTML, height=270, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🎲 Roll Dice for Today's Quest"):
        st.session_state.quest_revealed = True
        st.rerun()
        
else:
    # --- DISPLAY ACTIVE REVEALED QUEST ---
    col_main, col_actions = st.columns([3, 1])

    with col_main:
        quest_card_html = f"""
        <div class="drx-card {card_class}">
            <span class="drx-tag {tag_class}">{day_type_label} · {category.upper()}</span>
            <div class="drx-quest-title">{quest['emoji']} {quest['title']}</div>
            <div class="drx-quest-desc">{quest['desc']}</div>
        </div>
        """
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
            colors: ['#ff4b4b', '#ffbc00', '#00b4d8', '#4caf50', '#9c27b0']
        });
    </script>
    """
    components.html(CONFETTI_JS, height=0, width=0)
    st.markdown("""
        <div class="drx-card drx-card-gold">
            <div class="drx-quest-title">🏆 Adventure Logged!</div>
            <div class="drx-quest-desc">This task has been recorded into your local browser log. See you tomorrow!</div>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.just_completed = False

st.markdown('<hr class="drx-divider">', unsafe_allow_html=True)

# ============================================================================
# INTERACTIVE MODULES — LIGHT THEME INTERFACES
# ============================================================================
st.markdown('<div class="drx-section-header">🧩 Interactive Adventure Module</div>', unsafe_allow_html=True)

if category in ["language", "dance"]:  # Fallback helper for language or movement items
    vocab = st.session_state.current_vocab
    vocab_html = f"""
    <div class="drx-card drx-card-cyan">
        <span class="drx-tag drx-tag-weekday">🗣️ POLYGLOT CORE</span>
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="font-size:2rem;">{vocab['flag']}</div>
            <div>
                <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1px;">{vocab['language']}</div>
                <div class="drx-quest-title" style="margin-bottom:2px;">{vocab['word']}</div>
            </div>
        </div>
        <div style="margin-top:14px; padding:14px; background:#f0fdfa; border-radius:12px; border:1px solid #b2f2bb;">
            <div style="font-size:0.72rem; color:#0e7490; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">🔊 Read Aloud Guide</div>
            <div style="font-family:'Poppins',sans-serif; font-weight:800; font-size:1.3rem; color:#0e7490;">{vocab['pronunciation']}</div>
        </div>
        <div class="drx-quest-desc" style="margin-top:14px; font-style:italic; color:#334155;">"{vocab['meaning']}"</div>
    </div>
    """
    st.markdown(vocab_html, unsafe_allow_html=True)
    if st.button("🔁 Shuffle Vocabulary Word"):
        st.session_state.current_vocab = random.choice(VOCAB_BANK)
        st.rerun()

elif category == "art":
    st.markdown("""
        <div class="drx-card drx-card-gold"><span class="drx-tag drx-tag-weekend">🎨 ZEN PAINTING DECK</span>
        <div class="drx-quest-desc">Pick a vibrant neon tone, alter your brush width, and doodle cleanly across the canvas guide layout.</div></div>
    """, unsafe_allow_html=True)
    PAINT_HTML = """
    <div style="background:#ffffff; padding:14px; font-family:Inter,sans-serif;">
      <div id="toolbar" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
        <span style="color:#64748b; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Brush:</span>
        <button onclick="setColor('#ff4b4b')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#ff4b4b;cursor:pointer;box-shadow:0 0 6px #ff4b4b;"></button>
        <button onclick="setColor('#00b4d8')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#00b4d8;cursor:pointer;box-shadow:0 0 6px #00b4d8;"></button>
        <button onclick="setColor('#ffbc00')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#ffbc00;cursor:pointer;box-shadow:0 0 6px #ffbc00;"></button>
        <button onclick="setColor('#1e293b')" style="width:28px;height:28px;border-radius:50%;border:2px solid #fff;background:#1e293b;cursor:pointer;box-shadow:0 0 6px #1e293b;"></button>
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
        ctx.beginPath(); ctx.arc(150, 210, 90, 0, Math.PI*2); ctx.stroke();
      }
      drawGuide();

      function setColor(c) { currentColor = c; }
      function clearCanvas() { drawGuide(); }
      function getPos(e) {
        const rect = canvas.getBoundingClientRect();
        if (e.touches && e.touches.length > 0) {
          return { x: (e.touches[0].clientX - rect.left) * (canvas.width / rect.width), y: (e.touches[0].clientY - rect.top) * (canvas.height / rect.height) };
        }
        return { x: (e.clientX - rect.left) * (canvas.width / rect.width), y: (e.clientY - rect.top) * (canvas.height / rect.height) };
      }
      canvas.addEventListener('mousedown', (e) => { drawing = true; const p = getPos(e); lastX = p.x; lastY = p.y; });
      canvas.addEventListener('mouseup', () => drawing = false);
      canvas.addEventListener('mousemove', (e) => {
        if (!drawing) return;
        const p = getPos(e);
        ctx.strokeStyle = currentColor; ctx.lineWidth = document.getElementById('brushSize').value; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(lastX, lastY); ctx.lineTo(p.x, p.y); ctx.stroke();
        lastX = p.x; lastY = p.y;
      });
    </script>
    """
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(PAINT_HTML, height=520, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

elif category == "mindfulness":
    st.markdown("""
        <div class="drx-card drx-card-cyan"><span class="drx-tag drx-tag-weekday">⏱️ MIND-SYNC TIMER</span>
        <div class="drx-quest-desc">Start the 3-minute breathing break to align your target intentions.</div></div>
    """, unsafe_allow_html=True)
    TIMER_HTML = """
    <div style="background:#ffffff; padding:24px; border-radius:16px; text-align:center; font-family:Inter,sans-serif;">
      <div id="display" style="font-family:'Poppins',sans-serif; font-size:4rem; font-weight:900; color:#00b4d8; letter-spacing:2px;">03:00</div>
      <div style="margin-top:14px; display:flex; justify-content:center; gap:12px;">
        <button onclick="startTimer()" style="background:#00b4d8; color:#fff; border:none; padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">▶ Start</button>
        <button onclick="pauseTimer()" style="background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1; padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">⏸ Pause</button>
        <button onclick="resetTimer()" style="background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1; padding:10px 22px; border-radius:12px; font-weight:800; cursor:pointer;">↺ Reset</button>
      </div>
      <div id="celebration" style="margin-top:18px; font-size:1.2rem; font-weight:800; color:#ffbc00; display:none;">🎉 Beautifully done. You're centered. 🎉</div>
    </div>
    <script>
      let remaining = 180, intervalId = null;
      function render() {
        document.getElementById('display').innerText = Math.floor(remaining / 60).toString().padStart(2,'0') + ':' + (remaining % 60).toString().padStart(2,'0');
      }
      function startTimer() {
        if (intervalId) return;
        intervalId = setInterval(() => {
          if (remaining > 0) { remaining--; render(); }
          else { clearInterval(intervalId); document.getElementById('celebration').style.display = 'block'; }
        }, 1000);
      }
      function pauseTimer() { clearInterval(intervalId); intervalId = null; }
      function resetTimer() { pauseTimer(); remaining = 180; document.getElementById('celebration').style.display = 'none'; render(); }
    </script>
    """
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(TIMER_HTML, height=260, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

elif category == "chaos":
    opt1, opt2 = st.session_state.current_chaos
    st.markdown("""
        <div class="drx-card drx-card-coral"><span class="drx-tag drx-tag-weekend">🪙 THE DESTINY FLIP</span>
        <div class="drx-quest-desc">Let random design choices solve minor mental lockups. Tap below to spin.</div></div>
    """, unsafe_allow_html=True)
    COIN_HTML = f"""
    <div style="background:#ffffff; padding:24px; text-align:center; font-family:Inter,sans-serif;">
      <div style="display:flex; justify-content:space-around; margin-bottom:18px; color:#64748b; font-weight:700; font-size:0.85rem;">
        <div>🅰️ {opt1}</div>
        <div>🅱️ {opt2}</div>
      </div>
      <div id="scene" style="perspective:600px; display:flex; justify-content:center;">
        <div id="coin" onclick="flipCoin()" style="width:100px; height:100px; border-radius:50%; position:relative; transform-style:preserve-3d; transition:transform 1.1s cubic-bezier(.2,.8,.2,1); cursor:pointer; background:radial-gradient(circle at 35% 30%, #fff3b0, #ffbc00 70%, #d4a373 100%); display:flex; align-items:center; justify-content:center; font-size:2rem;">🪙</div>
      </div>
      <div id="result" style="margin-top:20px; font-family:'Poppins',sans-serif; font-weight:900; font-size:1.4rem; color:#ff4b4b; min-height:2rem;"></div>
    </div>
    <script>
      function flipCoin() {{
        const coin = document.getElementById('coin');
        const finalIndex = Math.random() < 0.5 ? 0 : 1;
        coin.style.transform = 'rotateY(' + (1440 + (finalIndex === 0 ? 0 : 180)) + 'deg)';
        document.getElementById('result').innerText = '';
        setTimeout(() => {{ document.getElementById('result').innerText = '✨ ' + (finalIndex === 0 ? "{opt1}" : "{opt2}") + ' ✨'; }}, 1150);
      }
    </script>
    """
    st.markdown('<div class="drx-module-frame">', unsafe_allow_html=True)
    components.html(COIN_HTML, height=290, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔁 New Dilemma"):
        st.session_state.current_chaos = random.choice(CHAOS_OPTIONS)
        st.rerun()

st.markdown('<div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:40px;">Rise. Quest. Repeat. 🌅</div>', unsafe_allow_html=True)
