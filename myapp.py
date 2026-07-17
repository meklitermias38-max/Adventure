import streamlit as st
import random
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
# COMPLETE QUEST BANKS & VOCAB ENTRIES
# ============================================================================
WEEKDAY_QUESTS = [
    {
        "title": "The Kitchen Counter Dance-Off", 
        "desc": "While waiting for morning prep work or water to boil, clear a 3-foot space and execute an uninhibited, energetic 45-second solo dance routine. Nobody is watching.", 
        "category": "dance", "emoji": "💃",
        "assistance": "💡 *Need a track? Put on a high-tempo song right now before you chicken out!*"
    },
    {
        "title": "The Secret Agent Walk", 
        "desc": "Match your steps precisely to the rhythm of whatever upbeat track is in your head right now. Navigate your next walk like you are the lead character in a high-stakes film.", 
        "category": "dance", "emoji": "🕺",
        "assistance": "💡 *Keep your chin up, shoulders back, and time your pace precisely to the rhythm.*"
    },
    {
        "title": "The Desktop Conductor", 
        "desc": "Put on an intense track at your desk. Use your hands and arms to dramatically conduct the music for 60 seconds as if leading an invisible orchestra.", 
        "category": "dance", "emoji": "🪄",
        "assistance": "💡 *Lean into the crescendo! Perfect for a quick, mid-day mental clarity break.*"
    },
    {
        "title": "The Dynamic Drink Call", 
        "desc": "Send a spontaneous text to a nearby friend: 'Free for a quick drink or coffee in the next 48 hours? Catch up with zero fixed agendas.'", 
        "category": "social", "emoji": "🍹",
        "assistance": "💡 *Stuck on who? Open your message app, scroll down to the 5th person on your list, and hit them up.*"
    },
    {
        "title": "The One-Word Compliment Drop", 
        "desc": "Give three different people a genuine one-word compliment today. Track their reactions — see who lights up the most.", 
        "category": "social", "emoji": "💬",
        "assistance": "💡 *Impactful words that work nicely: 'Radiant', 'Stellar', 'Impactful', or 'Unstoppable'.*"
    },
    {
        "title": "The Reverse Commute Explorer", 
        "desc": "Take one different turn, street, or exit on your way home today. Document one new thing you spotted.", 
        "category": "sensory", "emoji": "🔄",
        "assistance": "💡 *Look closely for dynamic architectural lines or unique storefronts you usually pass by.*"
    },
    {
        "title": "The Left-Handed Rebel", 
        "desc": "Do an ordinary task right now — like unlocking a door or navigating your phone — using your non-dominant hand.", 
        "category": "chaos", "emoji": "✋",
        "assistance": "💡 *Use your personalized Destiny Flip tool below to choose which basic task you should force your hand to try first!*"
    },
    {
        "title": "The Cultural Language Integration",
        "desc": "Take a beautifully descriptive word from another culture and intentionally inject it into a text, conversation, or journal entry today.",
        "category": "vocab", "emoji": "🌐",
        "assistance": "💡 *Check out the randomized Concept Vocabulary module at the bottom of your screen to source your word!*"
    }
]

WEEKEND_QUESTS = [
    {
        "title": "The Midnight Dance Ritual", 
        "desc": "Turn off all the lights in a room, queue up a song with a heavy bassline, and move your body strictly based on what feels right in the pitch dark.", 
        "category": "dance", "emoji": "🌌",
        "assistance": "💡 *Close your eyes even if it's already dark. Let go of what you look like entirely.*"
    },
    {
        "title": "The Flavor Alchemist", 
        "desc": "Bake or cook something simple today, but consciously swap out one foundational sugar, spice, or base liquid for a dynamic alternative you have in your cupboards.", 
        "category": "creative", "emoji": "🍪",
        "assistance": "💡 *Unsure which direction to head? Use the Destiny Flip below to choose between a flavor switch or a texture modification.*"
    },
    {
        "title": "The Coin Toss Explorer", 
        "desc": "At every unplanned fork in your day, let your custom preference matrix choose your direction.", 
        "category": "chaos", "emoji": "🪙",
        "assistance": "💡 *The Destiny Flip tool below is completely calibrated to your profile choices and ready.*"
    },
    {
        "title": "The Soundscape Iso-Check", 
        "desc": "Sit somewhere outside for 3 minutes with your eyes closed. Isolate the single highest-pitched sound and the lowest-frequency sound around you.", 
        "category": "sensory", "emoji": "🎧",
        "assistance": "💡 *Block out passing cars if you can, and listen instead for wind rustles or deep bird calls.*"
    }
]

VOCAB_BANK = [
    {"language": "Spanish", "flag": "🇪🇸", "word": "Duende", "meaning": "A heightened state of raw emotion and authenticity, especially felt during art or performance.", "pronunciation": "dwen-deh"},
    {"language": "Amharic", "flag": "🇪🇹", "word": "Buna", "meaning": "Coffee — but truly a ceremony of slowing down and connecting with the people around you.", "pronunciation": "boo-nah"},
    {"language": "Japanese", "flag": "🇯🇵", "word": "Komorebi", "meaning": "The dappled sunlight that filters through leaves in a forest canopy.", "pronunciation": "koh-moh-reh-bee"},
    {"language": "Swedish", "flag": "🇸🇪", "word": "Gökotta", "meaning": "Waking up early in the morning intentionally to go outside and hear the first birds sing.", "pronunciation": "goh-kot-tah"}
]

# --- ADVENTUROUS MEANINGS MATRIX ---
PREFIX_DATA = {
    "Vesper": {"theme": "Shadow/Night", "desc": "A quiet catalyst operating in twilight hours", "color": "#d8b4fe"},
    "Atlas": {"theme": "Mapping/Earth", "desc": "A structural anchor testing the boundaries of routine", "color": "#7dd3fc"},
    "Echo": {"theme": "Rhythm/Sound", "desc": "An atmospheric force expanding sensory signals", "color": "#fca5a5"},
    "Sable": {"theme": "Stealth/Focus", "desc": "A sleek, highly observant disruption agent", "color": "#94a3b8"},
    "Nova": {"theme": "Cosmic/Energy", "desc": "A sudden burst of bright, chaotic behavioral shifts", "color": "#fde047"},
    "Zephyr": {"theme": "Air/Movement", "desc": "A free-flowing entity shifting paths fluidly", "color": "#86efac"}
}
SUFFIX_DATA = {
    "Rogue": "who shatters established guidelines to uncover hidden micro-moments.",
    "Vortex": "who pulls nearby structures into a swirl of deliberate spontaneity.",
    "Sage": "who calculates precise, thoughtful deviations from the everyday norm.",
    "Wilder": "who roams through urban and creative spaces with uninhibited curiosity.",
    "Flux": "who constantly shifts states to keep external environments off-balance.",
    "Chrono": "who bends the daily timeline to extract extra life from standard hours."
}

# ============================================================================
# PERSISTENT SESSION STATE VALUES
# ============================================================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light Mode ☀️"
if "actual_name" not in st.session_state:
    st.session_state.actual_name = ""
if "name_ledger" not in st.session_state:
    st.session_state.name_ledger = {}
if "quest_revealed" not in st.session_state:
    st.session_state.quest_revealed = False
if "current_quest" not in st.session_state:
    st.session_state.current_quest = None
if "current_vocab" not in st.session_state:
    st.session_state.current_vocab = random.choice(VOCAB_BANK)
if "flip_result" not in st.session_state:
    st.session_state.flip_result = None

today = date.today()
is_weekend = today.weekday() >= 5
quest_pool = WEEKEND_QUESTS if is_weekend else WEEKDAY_QUESTS

if st.session_state.current_quest is None:
    st.session_state.current_quest = random.choice(quest_pool)
quest = st.session_state.current_quest

# ============================================================================
# VISUAL STYLING ENGINE (DYNAMIC THEME SWITCHER)
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
    accent_purple = "#d8b4fe"
    accent_coral = "#fca5a5"
    accent_cyan = "#7dd3fc"
else:
    bg_color = "#f8fafc"
    text_color = "#1e293b"
    sub_color = "#64748b"
    card_bg = "#ffffff"
    card_border = "#e2e8f0"
    tag_bg = "#f1f5f9"
    tag_text = "#475569"
    assistance_bg = "#f1f5f9"
    accent_purple = "#9c27b0"
    accent_coral = "#ff4b4b"
    accent_cyan = "#00b4d8"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'Inter', sans-serif; background-color: {bg_color} !important; color: {text_color}; }}
.drx-title {{ font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 2.5rem; color: {text_color}; margin-bottom: 0; }}
.drx-sub {{ color: {sub_color}; font-size: 1rem; margin-bottom: 2rem; }}
.drx-card {{ background: {card_bg}; border: 1px solid {card_border}; border-radius: 16px; padding: 24px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); }}
.drx-card-purple {{ border-top: 5px solid {accent_purple}; }}
.drx-card-coral {{ border-top: 5px solid {accent_coral}; }}
.drx-card-cyan {{ border-top: 5px solid {accent_cyan}; }}
.drx-tag {{ display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 12px; background: {tag_bg}; color: {tag_text}; }}
.drx-quest-title {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.35rem; color: {text_color}; margin-bottom: 8px; }}
.drx-assistance {{ background-color: {assistance_bg}; padding: 12px; border-left: 4px solid {sub_color}; border-radius: 4px; font-size: 0.95rem; margin-top: 14px; color: {text_color}; }}
.profile-banner {{ background: linear-gradient(135deg, {accent_cyan}, {accent_purple}); padding: 16px; border-radius: 12px; color: white; font-weight: 600; margin-bottom: 4px; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONTROL PANEL
# ============================================================================
with st.sidebar:
    st.title("⚙️ Control Hub")
    st.session_state.theme_mode = st.radio("App Skin Style", ["Light Mode ☀️", "Dark Mode 🌙"], index=0 if st.session_state.theme_mode == "Light Mode ☀️" else 1)
    st.markdown("---")
    
    st.subheader("👤 Login Registry")
    name_typed = st.text_input("Enter Your Actual Name:", value=st.session_state.actual_name).strip()
    
    current_adventurous_name = ""
    name_meaning = ""
    theme_color = "#3b82f6"
    active_profile = None

    if name_typed:
        lookup_key = name_typed.lower()
        
        if lookup_key not in st.session_state.name_ledger:
            used_names = [p["adventurous_name"] for p in st.session_state.name_ledger.values()]
            while True:
                p_choice = random.choice(list(PREFIX_DATA.keys()))
                s_choice = random.choice(list(SUFFIX_DATA.keys()))
                candidate = f"{p_choice} {s_choice}"
                if candidate not in used_names or len(used_names) >= 50:
                    break
            
            st.session_state.name_ledger[lookup_key] = {
                "adventurous_name": candidate,
                "prefix": p_choice,
                "suffix": s_choice,
                "archive": [],
                "preferences": [("Go Out 🏃‍♂️", "Stay In 🏠"), ("Run Quick ⚡", "Walk Slow 🚶‍♂️")]
            }
            st.toast(f"Adventurous identity generated: {candidate}!")
        
        st.session_state.actual_name = name_typed
        active_profile = st.session_state.name_ledger[lookup_key]
        current_adventurous_name = active_profile["adventurous_name"]
        
        p_val = active_profile["prefix"]
        s_val = active_profile["suffix"]
        name_meaning = f"**{p_val}** ({PREFIX_DATA[p_val]['desc']}) + **{s_val}** {SUFFIX_DATA[s_val]}"
        theme_color = PREFIX_DATA[p_val]["color"]
        
        st.markdown(f"""
        <div class="profile-banner" style="background: linear-gradient(135deg, {theme_color}, #475569);">
            🚀 Adventurer Code Assigned:<br>
            <span style="font-size:1.35rem; font-weight:800;">{current_adventurous_name}</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"📖 *Lore:* {name_meaning}")
        
        # --- CUSTOMISABLE THIS OR THAT SECTIONS ---
        st.markdown("---")
        st.subheader("🎨 Custom Preference Matrix")
        st.caption("Define your customized 'This or That' parameters for the flipper below.")
        
        st.markdown("**Dilemma Axis 1**")
        p1_this = st.text_input("This (Option A)", value=active_profile["preferences"][0][0], key="p1_this")
        p1_that = st.text_input("That (Option B)", value=active_profile["preferences"][0][1], key="p1_that")
        
        st.markdown("**Dilemma Axis 2**")
        p2_this = st.text_input("This (Option A)", value=active_profile["preferences"][1][0], key="p2_this")
        p2_that = st.text_input("That (Option B)", value=active_profile["preferences"][1][1], key="p2_that")
        
        active_profile["preferences"] = [(p1_this, p1_that), (p2_this, p2_that)]

        st.markdown("---")
        st.subheader("📜 Completed Milestones")
        if active_profile["archive"]:
            for item in active_profile["archive"]:
                st.markdown(f"✅ **{item}**")
        else:
            st.caption("No entries logged yet.")

# ============================================================================
# MAIN HUB VIEW INTERFACE
# ============================================================================
st.markdown('<div class="drx-title">🌅 DayRise Adventures</div>', unsafe_allow_html=True)
st.markdown('<div class="drx-sub">A personalized tactical framework for routine breaking.</div>', unsafe_allow_html=True)

if not st.session_state.actual_name:
    st.info("👋 To begin tracking your progress, please type your Actual Name inside the sidebar registry console.")
    st.stop()

if quest["category"] in ["dance", "movement"]:
    card_theme = "drx-card-purple"
elif quest["category"] in ["social", "vocab"]:
    card_theme = "drx-card-coral"
else:
    card_theme = "drx-card-cyan"

if not st.session_state.quest_revealed:
    st.markdown("### 🎲 Strategic Objective Locked")
    st.markdown(f"""
    <div style="background: {card_bg}; border: 2px dashed {card_border}; border-radius: 16px; padding: 40px; text-align: center;">
        <span style="font-size: 4.5rem;">🎲</span>
        <h4 style="margin-top: 12px; font-family: 'Poppins', sans-serif; color: {text_color};">Welcome Back, {current_adventurous_name}</h4>
        <p style="color: {sub_color}; font-size: 0.95rem;">Unleash your action modifier for the day.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 UNLOCK ACTIVE INJECTOR FEED", use_container_width=True):
        st.session_state.quest_revealed = True
        st.rerun()

else:
    st.markdown(f"""
    <div class="drx-card {card_theme}">
        <span class="drx-tag">{quest['category'].upper()} COMPONENT</span>
        <div class="drx-quest-title">{quest['emoji']} {quest['title']}</div>
        <p style="color: {text_color}; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0;">{quest['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="drx-assistance">{quest["assistance"]}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🏁 Log Quest as Finished", use_container_width=True):
            if quest["title"] not in active_profile["archive"]:
                active_profile["archive"].insert(0, quest["title"])
            st.balloons()
            
            # Colored Name-Matched Burst Mechanic
            st.markdown(f"""
            <div style="background: {theme_color}22; border: 2px solid {theme_color}; border-radius: 12px; padding: 16px; text-align: center; margin-top: 14px;">
                <h4 style="color: {theme_color}; margin: 0; font-family: 'Poppins', sans-serif;">🎉 MILESTONE SECURED BY {current_adventurous_name.upper()}!</h4>
                <p style="margin: 4px 0 0 0; font-size: 0.9rem; color: {text_color};">Registry profile updated successfully.</p>
            </div>
            """, unsafe_allow_html=True)
    with col_b:
        if st.button("🔀 Alternate Reroll Quest Pool", use_container_width=True):
            st.session_state.current_quest = random.choice(quest_pool)
            st.rerun()

# ============================================================================
# PERSISTENT COMPANION MODULES
# ============================================================================
st.markdown("---")
st.markdown("### 🪙 Global Device: The Destiny Coin Flip")
st.caption("An overarching helper utility calibrated with your customized choice vectors.")

pool = active_profile["preferences"]
opt_a1, opt_a2 = pool[0]
opt_b1, opt_b2 = pool[1]

col_c, col_d = st.columns(2)
with col_c:
    st.markdown(f"""
    <div style="background: {card_bg}; border: 1px solid {card_border}; padding: 16px; border-radius: 12px; text-align: center; margin-bottom:10px;">
        <span style="font-weight:600; color:{accent_coral};">Dilemma Matrix One</span><br>
        <strong>A:</strong> {opt_a1} | <strong>B:</strong> {opt_a2}
    </div>
    """, unsafe_allow_html=True)
    if st.button("🪙 Flip Matrix One", use_container_width=True):
        with st.spinner("Spinning coin..."):
            time.sleep(0.3)
        st.session_state.flip_result = f"✨ Fate chose: **{random.choice([opt_a1, opt_a2])}**"

with col_d:
    st.markdown(f"""
    <div style="background: {card_bg}; border: 1px solid {card_border}; padding: 16px; border-radius: 12px; text-align: center; margin-bottom:10px;">
        <span style="font-weight:600; color:{accent_cyan};">Dilemma Matrix Two</span><br>
        <strong>A:</strong> {opt_b1} | <strong>B:</strong> {opt_b2}
    </div>
    """, unsafe_allow_html=True)
    if st.button("🪙 Flip Matrix Two", use_container_width=True):
        with st.spinner("Spinning coin..."):
            time.sleep(0.3)
        st.session_state.flip_result = f"✨ Fate chose: **{random.choice([opt_b1, opt_b2])}**"

if st.session_state.flip_result:
    st.info(st.session_state.flip_result)

# ============================================================================
# LANGUAGE ENGINE LAYOVER VIEW
# ============================================================================
if quest["category"] == "vocab":
    st.markdown("---")
    st.markdown("### 🌐 Active Target Concept Card")
    v = st.session_state.current_vocab
    
    st.markdown(f"""
    <div class="drx-card" style="border-left: 5px solid #ff9800; background: {card_bg};">
        <div style="font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color:{text_color};">{v['flag']} {v['word']}</div>
        <div style="color: {sub_color}; font-size: 0.9rem; margin-bottom: 12px;">Language: {v['language']} | Phonetic: *{v['pronunciation']}*</div>
        <p style="font-size: 1rem; margin-bottom: 0; color:{text_color};"><strong>Concept Meaning:</strong> {v['meaning']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Rotate Concept Vocabulary Card", use_container_width=True):
        st.session_state.current_vocab = random.choice(VOCAB_BANK)
        st.rerun()
