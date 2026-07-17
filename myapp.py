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
# COMPLETE COMPREHENSIVE QUEST BANKS (ALL TASKS + ASSISTANCE)
# ============================================================================
WEEKDAY_QUESTS = [
    {
        "title": "The Kitchen Counter Dance-Off", 
        "desc": "While waiting for your morning coffee or water to boil, clear a 3-foot space and execute an uninhibited, energetic 45-second solo dance routine. Nobody is watching.", 
        "category": "dance", "emoji": "💃", "requires_flip": False,
        "assistance": "💡 *Need a track? Put on a high-tempo song right now before you chicken out!*"
    },
    {
        "title": "The Secret Agent Walk", 
        "desc": "Match your steps precisely to the rhythm of whatever upbeat track is in your head right now. Navigate your next walk like you are the lead character in a high-stakes film.", 
        "category": "dance", "emoji": "🕺", "requires_flip": False,
        "assistance": "💡 *Keep your chin up, shoulders back, and time your pace precisely to the rhythm.*"
    },
    {
        "title": "The Desktop Conductor", 
        "desc": "Put on an intense classical or electronic track at your desk. Use your hands and arms to dramatically conduct the music for 60 seconds as if leading an invisible orchestra.", 
        "category": "dance", "emoji": "🪄", "requires_flip": False,
        "assistance": "💡 *Lean into the crescendo! Perfect for a quick, mid-day mental clarity break.*"
    },
    {
        "title": "The Slow-Motion Slip", 
        "desc": "Spend the next three minutes moving through your space at exactly 25% speed. Cross the room like you are walking on the moon or wading through deep water.", 
        "category": "movement", "emoji": "🧑‍🚀", "requires_flip": False,
        "assistance": "💡 *Focus completely on the balance of your weight switching slowly from heel to toe.*"
    },
    {
        "title": "The Dynamic Drink Call", 
        "desc": "Send a spontaneous text to a nearby friend: 'Free for a quick drink/coffee in the next 48 hours? First round is on me.' Catch up with zero fixed agendas.", 
        "category": "social", "emoji": "🍹", "requires_flip": False,
        "assistance": "💡 *Stuck on who? Open your message app, scroll down to the 5th person on your list, and hit them up.*"
    },
    {
        "title": "The One-Word Compliment Drop", 
        "desc": "Give three different people a genuine one-word compliment today. Track their reactions — see who lights up the most.", 
        "category": "social", "emoji": "💬", "requires_flip": False,
        "assistance": "💡 *Impactful words that work nicely: 'Radiant', 'Stellar', 'Impactful', or 'Unstoppable'.*"
    },
    {
        "title": "The Digital Postcard", 
        "desc": "Find a funny, beautiful, or bizarre photo in your camera roll from over a year ago. Text it to a friend out of the blue with just: 'This made me think of you today.'", 
        "category": "social", "emoji": "📸", "requires_flip": False,
        "assistance": "💡 *Go to your photo app search bar, type 'throwback' or 'trip', and pick the first nostalgic thing you see.*"
    },
    {
        "title": "The Reverse Commute Explorer", 
        "desc": "Take one different turn, street, or exit on your way home today. Document one new thing you spotted.", 
        "category": "sensory", "emoji": "🔄", "requires_flip": False,
        "assistance": "💡 *Look closely for dynamic architectural lines, old signposts, or unique storefronts you usually pass by.*"
    },
    {
        "title": "The Left-Handed Rebel", 
        "desc": "Do an ordinary task right now — like unlocking a door, pouring water, or navigating your phone — using your non-dominant hand.", 
        "category": "chaos", "emoji": "✋", "requires_flip": True,
        "assistance": "💡 *Use the Destiny Flip tool below to choose which basic task you should force your non-dominant hand to try first!*"
    },
    {
        "title": "The Emoji Only Texter", 
        "desc": "Reply to your next three text messages using only emoji. Force yourself to be creatively precise.", 
        "category": "creative", "emoji": "📱", "requires_flip": False,
        "assistance": "💡 *If someone asks 'Where are you?', try 📍🏢🏃‍♂️ instead of spelling it out.*"
    },
    {
        "title": "The Desk Yoga Stealth Mission", 
        "desc": "Every hour today, execute one covert desk stretch so smooth your coworkers never suspect you're doing yoga.", 
        "category": "physical", "emoji": "🧘", "requires_flip": False,
        "assistance": "💡 *Try seated spinal twists or subtle shoulder blade squeezes while reading through an email.*"
    },
    {
        "title": "The Secret Keyboard Agent", 
        "desc": "For the next hour, type every message with unusual flair — sign off every casual message with a tiny secret code word.", 
        "category": "creative", "emoji": "⌨️", "requires_flip": False,
        "assistance": "💡 *Try ending with words like [Over&Out], [Alpha-7], or [RogerThat] to keep things interesting.*"
    },
    {
        "title": "The Cultural Language Integration",
        "desc": "Take a beautifully descriptive word from another culture and intentionally inject it into a text, conversation, or journal entry today.",
        "category": "vocab", "emoji": "🌐", "requires_flip": False,
        "assistance": "💡 *Check out the randomized Concept Vocabulary module at the bottom of your screen to source your word!*"
    }
]

WEEKEND_QUESTS = [
    {
        "title": "The Midnight Dance Ritual", 
        "desc": "Turn off all the lights in a room, queue up a song with a heavy bassline, and move your body strictly based on what feels right in the pitch dark.", 
        "category": "dance", "emoji": "🌌", "requires_flip": False,
        "assistance": "💡 *Close your eyes even if it's already dark. Let go of what you look like entirely.*"
    },
    {
        "title": "The Freeze-Frame Rhythm", 
        "desc": "Play an upbeat track. Every time you hit pause completely at random, you must hold whatever dramatic or expressive pose you're in for 5 full seconds without moving.", 
        "category": "dance", "emoji": "⏸️", "requires_flip": False,
        "assistance": "💡 *No cheating! Even if you are balanced precariously on one foot, lock your frame.*"
    },
    {
        "title": "The Flavor Alchemist", 
        "desc": "Bake or cook something simple today, but consciously swap out one foundational sugar, spice, or base liquid for a dynamic alternative you have in your cupboards.", 
        "category": "creative", "emoji": "🍪", "requires_flip": True,
        "assistance": "💡 *Unsure which direction to head? Use the Destiny Flip below to choose between a flavor switch or a texture modification.*"
    },
    {
        "title": "The Single-Spice Takeover", 
        "desc": "Pick one spice in your kitchen you rarely touch. Cook your next simple meal or snack built entirely around making that specific flavor the absolute star of the show.", 
        "category": "creative", "emoji": "🌶️", "requires_flip": False,
        "assistance": "💡 *Smell 3 different spice jars first. Pick the one that catches you off guard and look up a quick paring idea.*"
    },
    {
        "title": "The Typography Tracker", 
        "desc": "Go on a 10-minute neighborhood walk looking only at signs and storefront lettering. Identify the most beautiful piece of text and the absolute ugliest.", 
        "category": "art", "emoji": "🔤", "requires_flip": False,
        "assistance": "💡 *Look at fonts critically—notice spacing, color contrasts, and how line weight conveys personality.*"
    },
    {
        "title": "The Soundscape Iso-Check", 
        "desc": "Sit somewhere outside for 3 minutes with your eyes closed. Isolate the single highest-pitched sound and the lowest-frequency sound around you. Treat it like a song composition.", 
        "category": "sensory", "emoji": "🎧", "requires_flip": False,
        "assistance": "💡 *Block out passing cars if you can, and listen instead for wind rustles, deep plumbing hums, or bird calls.*"
    },
    {
        "title": "The Coin Toss Explorer", 
        "desc": "At every unplanned fork in your day, let a quick coin flip choose your direction. Follow it for at least three decisions.", 
        "category": "chaos", "emoji": "🪙", "requires_flip": True,
        "assistance": "💡 *The Destiny Flip tool below is active and ready to make your upcoming navigation choices.*"
    },
    {
        "title": "The Neighborhood Grid-Run", 
        "desc": "Pick a direction and walk exactly six blocks in a square pattern, turning only right. Map what you discover.", 
        "category": "physical", "emoji": "🗺️", "requires_flip": True,
        "assistance": "💡 *Flip below to decide if you begin your square walk by turning Left or Right out your front door.*"
    },
    {
        "title": "The Horizon Hunter", 
        "desc": "Find the highest accessible point near you — a hill, rooftop, parking garage — and watch the horizon for ten full minutes, no phone.", 
        "category": "physical", "emoji": "🌄", "requires_flip": False,
        "assistance": "💡 *Leave your device safely tucked deep in your pocket. Let your focus drift completely out to the farthest line.*"
    }
]

VOCAB_BANK = [
    {"language": "Spanish", "flag": "🇪🇸", "word": "Duende", "meaning": "A heightened state of raw emotion and authenticity, especially felt during art or performance.", "pronunciation": "dwen-deh"},
    {"language": "Amharic", "flag": "🇪🇹", "word": "Buna", "meaning": "Coffee — but truly a ceremony of slowing down and connecting with the people around you.", "pronunciation": "boo-nah"},
    {"language": "Japanese", "flag": "🇯🇵", "word": "Komorebi", "meaning": "The dappled sunlight that filters through leaves in a forest canopy.", "pronunciation": "koh-moh-reh-bee"},
    {"language": "Swedish", "flag": "🇸🇪", "word": "Gökotta", "meaning": "Waking up early in the morning intentionally to go outside and hear the first birds sing.", "pronunciation": "goh-kot-tah"}
]

CHAOS_OPTIONS = [
    ("Turn Left 🪟", "Turn Right 🧱"),
    ("Try a local spiced tea/herbal infusion 🫖", "Stick to default black coffee/espresso ☕"),
    ("Use phone with left hand 📱", "Write notes with left hand ✍️"),
    ("Order something brand new 🍛", "Stick to your classic favorite ☕"),
    ("Listen to acoustic instrumentals 🎻", "Listen to high-tempo electronic bass 🎛️"),
]

# --- NAME RANDOMIZER GENERATORS ---
FIRST_NAMES = ["Neo", "Vesper", "Atlas", "Echo", "Sable", "Nova", "Zephyr", "Lyra", "Orion", "Kai"]
LAST_NAMES = ["Rogue", "Sparke", "Vortex", "Sage", "Wilder", "Flux", "Chrono", "Sol", "Strider", "Zen"]
PERSONAS = ["Urban Explorer 🌃", "Chaos Monk 🧘", "Creative Renegade 🎨", "Rhythm Alchemist 💃"]

# ============================================================================
# INITIALIZE STATE
# ============================================================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light Mode ☀️"
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "archive_data" not in st.session_state:
    st.session_state.archive_data = []
if "persona" not in st.session_state:
    st.session_state.persona = "Urban Explorer 🌃"
if "quest_revealed" not in st.session_state:
    st.session_state.quest_revealed = False
if "current_quest" not in st.session_state:
    st.session_state.current_quest = None
if "current_chaos" not in st.session_state:
    st.session_state.current_chaos = random.choice(CHAOS_OPTIONS)
if "current_vocab" not in st.session_state:
    st.session_state.current_vocab = random.choice(VOCAB_BANK)

today = date.today()
is_weekend = today.weekday() >= 5
quest_pool = WEEKEND_QUESTS if is_weekend else WEEKDAY_QUESTS

# Ensure stable quest assignment
if st.session_state.current_quest is None:
    st.session_state.current_quest = random.choice(quest_pool)

quest = st.session_state.current_quest

# ============================================================================
# STYLING (DYNAMIC LIGHT/DARK ENGINE)
# ============================================================================
if st.session_state.theme_mode == "Dark Mode 🌙":
    bg_color = "#0f172a"
    text_color = "#f1f5f9"
    sub_color = "#94a3b8"
    card_bg = "#1e293b"
    card_border = "#334155"
    tag_bg = "#475569"
    tag_text = "#f8fafc"
    assistance_bg = "#334155"
else:
    bg_color = "#f8fafc"
    text_color = "#1e293b"
    sub_color = "#64748b"
    card_bg = "#ffffff"
    card_border = "#e2e8f0"
    tag_bg = "#f1f5f9"
    tag_text = "#475569"
    assistance_bg = "#f8fafc"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'Inter', sans-serif; background-color: {bg_color} !important; color: {text_color}; }}
.drx-title {{ font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 2.5rem; color: {text_color}; margin-bottom: 0; }}
.drx-sub {{ color: {sub_color}; font-size: 1rem; margin-bottom: 2rem; }}
.drx-card {{ background: {card_bg}; border: 1px solid {card_border}; border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); }}
.drx-card-purple {{ border-top: 5px solid #9c27b0; }}
.drx-card-coral {{ border-top: 5px solid #ff4b4b; }}
.drx-card-cyan {{ border-top: 5px solid #00b4d8; }}
.drx-tag {{ display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 12px; background: {tag_bg}; color: {tag_text}; }}
.drx-quest-title {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.35rem; color: {text_color}; margin-bottom: 8px; }}
.drx-assistance {{ background-color: {assistance_bg}; padding: 12px; border-left: 4px solid #64748b; border-radius: 4px; font-size: 0.95rem; margin-top: 14px; color: {sub_color}; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR SETUP SPACE & THEME CONTROLLER
# ============================================================================
with st.sidebar:
    st.title("⚙️ Customization Deck")
    
    # Theme Selection UI
    st.session_state.theme_mode = st.radio("App Skin Style", ["Light Mode ☀️", "Dark Mode 🌙"], index=0 if st.session_state.theme_mode == "Light Mode ☀️" else 1)

    st.markdown("---")
    st.subheader("👤 Identity Profile")
    
    # Profile Profile Randomization Trigger
    if st.button("🎲 Randomize Profile Info", use_container_width=True):
        st.session_state.player_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        st.session_state.persona = random.choice(PERSONAS)
        st.rerun()
        
    name_input = st.text_input("Adventurer Code/Name", value=st.session_state.player_name, placeholder="Type custom handle...")
    if name_input != st.session_state.player_name:
        st.session_state.player_name = name_input
        st.rerun()

    if st.session_state.player_name:
        st.session_state.persona = st.selectbox("Archetype Matrix", PERSONAS, index=PERSONAS.index(st.session_state.persona) if st.session_state.persona in PERSONAS else 0)
        st.markdown("---")
        st.subheader("📜 History Today")
        if st.session_state.archive_data:
            for item in st.session_state.archive_data:
                st.markdown(f"✅ **{item['title']}**")
        else:
            st.caption("No entries finalized yet.")

# ============================================================================
# MAIN INTERFACE RUNNER
# ============================================================================
st.markdown('<div class="drx-title">🌅 DayRise Adventures</div>', unsafe_allow_html=True)
st.markdown('<div class="drx-sub">Your personal tactical framework for micro-routine disruption.</div>', unsafe_allow_html=True)

if not st.session_state.player_name:
    st.info("👋 Assign an Identity inside the Customization Deck sidebar to unlock.")
    st.stop()

# Theme Border Color Mapping Logic
if quest["category"] in ["dance", "movement"]:
    card_theme = "drx-card-purple"
elif quest["category"] in ["social", "vocab"]:
    card_theme = "drx-card-coral"
else:
    card_theme = "drx-card-cyan"

# --- ADVENTURE CONTAINER MODULE ---
if not st.session_state.quest_revealed:
    st.markdown("### 🎲 Primary Objective Locked")
    
    st.markdown(f"""
    <div style="background: {card_bg}; border: 2px dashed {card_border}; border-radius: 16px; padding: 40px; text-align: center;">
        <span style="font-size: 4.5rem;">🎲</span>
        <h4 style="margin-top: 12px; font-family: 'Poppins', sans-serif; color: {text_color};">Tap to Load Today's Core Strategy</h4>
        <p style="color: {sub_color}; font-size: 0.95rem;">Unleash your unique challenge modifier.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 UNLOCK ADVENTURE INJECTOR", use_container_width=True):
        with st.spinner("Calculating randomized sequence variables..."):
            time.sleep(0.5)
        st.session_state.quest_revealed = True
        st.rerun()

else:
    # --- QUEST REVEALED ACCORDINGLY ---
    st.markdown(f"""
    <div class="drx-card {card_theme}">
        <span class="drx-tag">{quest['category'].upper()} COMPONENT</span>
        <div class="drx-quest-title">{quest['emoji']} {quest['title']}</div>
        <p style="color: {text_color}; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0;">{quest['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Universal Assistance Injection Layer
    st.markdown(f'<div class="drx-assistance">{quest["assistance"]}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🏁 Log Quest as Finished", use_container_width=True):
            if not any(item['title'] == quest['title'] for item in st.session_state.archive_data):
                st.session_state.archive_data.insert(0, {"title": quest["title"], "date": today.isoformat()})
            st.balloons()
            st.success("Milestone achieved and written to profile log memory!")
    with col_b:
        if st.button("🔀 Alternate Reroll Quest Pool", use_container_width=True):
            st.session_state.current_quest = random.choice(quest_pool)
            st.rerun()

    # ============================================================================
    # CONTEXT SYSTEM BARS (CONDITIONAL ON TASK REQ)
    # ============================================================================
    if quest.get("requires_flip", False) or quest["category"] == "chaos":
        st.markdown("---")
        st.markdown("### 🪙 Context Tool: The Destiny Flip")
        opt1, opt2 = st.session_state.current_chaos

        st.markdown(f"""
        <div style="background: {card_bg}; border: 1px solid {card_border}; padding: 22px; border-radius: 12px; text-align: center;">
            <div style="display: flex; justify-content: space-around; font-weight: 600; font-size: 1.1rem;">
                <span style="color: #ff4b4b;">Choice A: {opt1}</span>
                <span style="color: #00b4d8;">Choice B: {opt2}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_c, col_d = st.columns(2)
        with col_c:
            if st.button("🪙 Execute Coin Flip Decision", use_container_width=True):
                chosen = random.choice([opt1, opt2])
                st.info(f"✨ Tactical Choice Evaluated: Go with **{chosen}**")
        with col_d:
            if st.button("🔄 Shuffle Chaos Dilemma Matrix", use_container_width=True):
                st.session_state.current_chaos = random.choice(CHAOS_OPTIONS)
                st.rerun()

    # ============================================================================
    # INTEGRATED LANGUAGE COMPANION (CONDITIONAL ON TASK REQ)
    # ============================================================================
    if quest["category"] == "vocab":
        st.markdown("---")
        st.markdown("### 🌐 Active Target Concept Card")
        v = st.session_state.current_vocab
        
        st.markdown(f"""
        <div class="drx-card" style="border-left: 5px solid #ff9800;">
            <div style="font-size: 1.4rem; font-weight: 700; margin-bottom: 4px;">{v['flag']} {v['word']}</div>
            <div style="color: {sub_color}; font-size: 0.9rem; margin-bottom: 12px;">Language: {v['language']} | Phonetic: *{v['pronunciation']}*</div>
            <p style="font-size: 1rem; margin-bottom: 0;"><strong>Concept Meaning:</strong> {v['meaning']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Rotate Concept Vocabulary Card", use_container_width=True):
            st.session_state.current_vocab = random.choice(VOCAB_BANK)
            st.rerun()
