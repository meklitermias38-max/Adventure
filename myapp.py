import streamlit as st
import random
import json
import time
from datetime import date

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
# EXPANDED QUEST BANKS (MORE ADVENTURES, DANCE, & DO THIS/DO THAT)
# ============================================================================
WEEKDAY_QUESTS = [
    {"title": "The Kitchen Counter Dance-Off", "desc": "While waiting for your morning coffee or water to boil, clear a 3-foot space and execute an uninhibited, energetic 45-second solo dance routine. Nobody is watching.", "category": "dance", "emoji": "💃"},
    {"title": "The Secret Agent Walk", "desc": "Match your steps precisely to the rhythm of whatever upbeat track is in your head right now. Navigate your next walk like you are the lead character in a high-stakes film.", "category": "dance", "emoji": "🕺"},
    {"title": "The Reverse Commute Explorer", "desc": "Take one different turn, street, or exit on your way home today. Document one new thing you spotted.", "category": "sensory", "emoji": "🔄"},
    {"title": "The Left-Handed Rebel", "desc": "Do one ordinary task today — brushing teeth, opening a door, writing a note — with your non-dominant hand.", "category": "chaos", "emoji": "✋"},
    {"title": "The Emoji Only Texter", "desc": "Reply to your next three text messages using only emoji. Force yourself to be creatively precise.", "category": "creative", "emoji": "📱"},
    {"title": "The Desk Yoga Stealth Mission", "desc": "Every hour today, execute one covert desk stretch so smooth your coworkers never suspect you're doing yoga.", "category": "physical", "emoji": "🧘"},
    {"title": "The One-Word Compliment Drop", "desc": "Give three different people a genuine one-word compliment today. Track their reactions.", "category": "social", "emoji": "💬"},
    {"title": "The Secret Keyboard Agent", "desc": "For the next hour, type every message with unusual flair — sign off every Slack/email with a tiny secret code word.", "category": "creative", "emoji": "⌨️"},
]

WEEKEND_QUESTS = [
    {"title": "The Midnight Dance Ritual", "desc": "Turn off all the lights in a room, queue up a song with a heavy bassline, and move your body strictly based on what feels right in the pitch dark.", "category": "dance", "emoji": "🌌"},
    {"title": "The Flavor Alchemist", "desc": "Bake or cook something simple today, but consciously swap out one foundational sugar, spice, or base liquid for an experimental alternative you have in your cupboards.", "category": "creative", "emoji": "🍪"},
    {"title": "The Coin Toss Explorer", "desc": "At every unplanned fork in your day, let a quick coin flip choose your direction. Follow it for at least three decisions.", "category": "chaos", "emoji": "🪙"},
    {"title": "The Neighborhood Grid-Run", "desc": "Pick a direction and walk exactly six blocks in a square pattern, turning only right. Map what you discover.", "category": "physical", "emoji": "🗺️"},
    {"title": "The Horizon Hunter", "desc": "Find the highest accessible point near you — a hill, rooftop, parking garage — and watch the horizon for ten full minutes, no phone.", "category": "physical", "emoji": "🌄"},
    {"title": "The Urban Photography Safari", "desc": "Shoot ten photos of things people usually walk past — textures, shadows, forgotten signage.", "category": "art", "emoji": "📸"},
]

VOCAB_BANK = [
    {"language": "Spanish", "flag": "🇪🇸", "word": "Duende", "meaning": "A heightened state of raw emotion and authenticity, especially felt during art or performance.", "pronunciation": "dwen-deh"},
    {"language": "Amharic", "flag": "🇪🇹", "word": "Buna", "meaning": "Coffee — but truly a ceremony of slowing down and connecting with the people around you.", "pronunciation": "boo-nah"},
    {"language": "Japanese", "flag": "🇯🇵", "word": "Komorebi", "meaning": "The dappled sunlight that filters through leaves in a forest canopy.", "pronunciation": "koh-moh-reh-bee"},
]

CHAOS_OPTIONS = [
    ("Turn Left", "Turn Right"),
    ("Order something new", "Stick to the classics"),
    ("Take the stairs", "Take the elevator"),
]

PERSONAS = ["Urban Explorer 🌃", "Chaos Monk 🧘", "Creative Renegade 🎨"]

# ============================================================================
# STYLING (CLEAN LIGHT THEME)
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #1e293b; }
.drx-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 2.5rem; color: #0f172a; margin-bottom: 0; }
.drx-sub { color: #64748b; font-size: 1rem; margin-bottom: 2rem; }
.drx-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.drx-card-purple { border-top: 5px solid #9c27b0; }
.drx-card-cyan { border-top: 5px solid #00b4d8; }
.drx-card-coral { border-top: 5px solid #ff4b4b; }
.drx-tag { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 12px; background: #f1f5f9; color: #475569; }
.drx-quest-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.35rem; margin-bottom: 8px; }
/* Big Tap Container styling */
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# STATE TRACKING
# ============================================================================
query_params = st.query_params

if "player_name" not in st.session_state:
    st.session_state.player_name = query_params.get("saved_name", "")
if "archive_data" not in st.session_state:
    st.session_state.archive_data = []
if "persona" not in st.session_state:
    st.session_state.persona = "Urban Explorer 🌃"
if "quest_revealed" not in st.session_state:
    st.session_state.quest_revealed = False
if "current_quest" not in st.session_state:
    st.session_state.current_quest = None
if "current_vocab" not in st.session_state:
    st.session_state.current_vocab = random.choice(VOCAB_BANK)
if "current_chaos" not in st.session_state:
    st.session_state.current_chaos = random.choice(CHAOS_OPTIONS)

today = date.today()
is_weekend = today.weekday() >= 5
quest_pool = WEEKEND_QUESTS if is_weekend else WEEKDAY_QUESTS

# ============================================================================
# SIDEBAR CONTROL PANEL
# ============================================================================
with st.sidebar:
    st.title("⚙️ Setup Space")
    name_input = st.text_input("Adventurer Name", value=st.session_state.player_name, placeholder="Type your name...")
    if name_input != st.session_state.player_name:
        st.session_state.player_name = name_input
        st.rerun()

    if st.session_state.player_name:
        st.session_state.persona = st.selectbox("Your Archetype", PERSONAS, index=0)
        st.markdown("---")
        st.subheader("📜 Completed Today")
        if st.session_state.archive_data:
            for item in st.session_state.archive_data:
                st.markdown(f"✅ **{item['title']}** ({item['date']})")
        else:
            st.caption("No adventures completed yet today.")

# ============================================================================
# MAIN INTERFACE
# ============================================================================
st.markdown('<div class="drx-title">🌅 DayRise Adventures</div>', unsafe_allow_html=True)
st.markdown('<div class="drx-sub">Your lightweight tactical hub for routine breaking.</div>', unsafe_allow_html=True)

if not st.session_state.player_name:
    st.info("👋 Enter your name in the sidebar to begin.")
    st.stop()

# Select a stable quest for the session if none exists
if st.session_state.current_quest is None:
    st.session_state.current_quest = random.choice(quest_pool)

quest = st.session_state.current_quest

# Determine color theme mapping
if quest["category"] == "dance":
    card_theme = "drx-card-purple"
elif is_weekend:
    card_theme = "drx-card-coral"
else:
    card_theme = "drx-card-cyan"

# --- THE QUEST LOCKER / TAP MECHANISM ---
if not st.session_state.quest_revealed:
    st.markdown("### 🎲 Today's Quest is Locked")
    
    # Large tactile block layout built using a clean column layout
    st.markdown("""
    <div style="background: #ffffff; border: 2px dashed #cbd5e1; border-radius: 16px; padding: 40px; text-align: center;">
        <span style="font-size: 4.5rem;">🎲</span>
        <h4 style="margin-top: 12px; font-family: 'Poppins', sans-serif;">Tap Below to Roll for Today's Adventure</h4>
        <p style="color: #64748b; font-size: 0.95rem;">Unleash your action prompt for the day.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 ROLL / TAP FOR TODAY'S QUEST", use_container_width=True):
        with st.spinner("Rolling the dice... ⚀ ⚄ ⚃"):
            time.sleep(0.8)  # Mimic animation speed cleanly
        st.session_state.quest_revealed = True
        st.rerun()

else:
    # --- QUEST REVEALED ACCORDINGLY ---
    st.markdown(f"""
    <div class="drx-card {card_theme}">
        <span class="drx-tag">{quest['category'].upper()} MODE</span>
        <div class="drx-quest-title">{quest['emoji']} {quest['title']}</div>
        <p style="color: #475569; font-size: 1.05rem; line-height: 1.6;">{quest['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🏁 Log Quest as Finished", use_container_width=True):
            st.session_state.archive_data.insert(0, {"title": quest["title"], "date": today.isoformat()})
            st.success("Adventure logged into sidebar profile memory!")
    with col_b:
        if st.button("🔀 Alternate Reroll", use_container_width=True):
            st.session_state.current_quest = random.choice(quest_pool)
            st.rerun()

st.markdown("---")

# ============================================================================
# COMPANION MODULES (DO THIS OR DO THAT)
# ============================================================================
st.markdown("### 🪙 Context Tool: The Destiny Flip")
opt1, opt2 = st.session_state.current_chaos

st.markdown(f"""
<div style="background: white; border: 1px solid #e2e8f0; padding: 18px; border-radius: 12px;">
    <div style="display: flex; justify-content: space-around; margin-bottom: 12px; font-weight: 600;">
        <span style="color: #ff4b4b;">Option A: {opt1}</span>
        <span style="color: #00b4d8;">Option B: {opt2}</span>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🪙 Flip to Decide Between This or That", use_container_width=True):
    chosen = random.choice([opt1, opt2])
    st.balloons()
    st.info(f"✨ Fate chose: **{chosen}**")

if st.button("🔄 Swap Dilemma Pool Options", use_container_width=True):
    st.session_state.current_chaos = random.choice(CHAOS_OPTIONS)
    st.rerun()
