import random
import textwrap
import streamlit as st

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Horde Roller",
    page_icon="🎲",
    layout="centered",
)

# ── Fantasy CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cinzel:wght@400;600&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

.stApp {
    background-color: #0d0d0d;
    background-image: radial-gradient(ellipse at top, #1c1408 0%, #0d0d0d 70%);
}
#MainMenu, footer, header { visibility: hidden; }

.title-text {
    font-family: 'Cinzel Decorative', serif;
    font-size: 2.6rem;
    color: #c9a84c;
    text-align: center;
    text-shadow: 0 0 18px #c9a84c88, 0 2px 4px #000;
    letter-spacing: 3px;
    margin-bottom: 0.2rem;
}
.subtitle-text {
    font-family: 'Crimson Text', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #8a7560;
    text-align: center;
    margin-bottom: 1.5rem;
}
.rune-divider {
    text-align: center;
    color: #c9a84c;
    font-size: 1.3rem;
    letter-spacing: 12px;
    margin: 1.0rem 0;
    opacity: 0.6;
}
.section-header {
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    color: #c9a84c;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid #3a2e1a;
    padding-bottom: 0.4rem;
}
label, .stSelectbox label, .stNumberInput label, .stRadio label, .stTextInput label {
    font-family: 'Cinzel', serif !important;
    color: #c9a84c !important;
    font-size: 0.8rem !important;
    letter-spacing: 1px !important;
}
input[type=number], input[type=text], .stSelectbox > div > div {
    background-color: #1a1408 !important;
    border: 1px solid #5a4a2a !important;
    color: #e8d9b0 !important;
    font-family: 'Crimson Text', serif !important;
    font-size: 1.05rem !important;
    border-radius: 4px !important;
}

/* Main roll button */
.stButton > button[kind="primary"], div[data-testid="stButton"] > button {
    font-family: 'Cinzel', serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 3px !important;
    color: #0d0d0d !important;
    background: linear-gradient(135deg, #c9a84c 0%, #f0d080 50%, #c9a84c 100%) !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    box-shadow: 0 0 20px #c9a84c55 !important;
}
.stButton > button:hover {
    box-shadow: 0 0 35px #c9a84c99 !important;
    transform: translateY(-1px) !important;
}

/* Result block per target */
.target-result {
    background: linear-gradient(160deg, #1c1408 0%, #120f05 100%);
    border: 1px solid #5a4a2a;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: inset 0 0 20px #00000088;
}
.target-result .target-name {
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    color: #c9a84c;
    letter-spacing: 2px;
    border-bottom: 1px solid #3a2e1a;
    padding-bottom: 0.4rem;
    margin-bottom: 0.7rem;
}
.target-result .target-ac {
    font-family: 'Crimson Text', serif;
    font-style: italic;
    font-size: 0.9rem;
    color: #8a7560;
    margin-left: 0.5rem;
}
.stat-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 0.6rem; }
.stat-box {
    flex: 1;
    min-width: 80px;
    background: #0d0d0d;
    border: 1px solid #3a2e1a;
    border-radius: 4px;
    padding: 0.5rem 0.4rem;
    text-align: center;
}
.stat-box .stat-label {
    font-family: 'Cinzel', serif;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    color: #6a5a40;
    text-transform: uppercase;
}
.stat-box .stat-value {
    font-family: 'Cinzel Decorative', serif;
    font-size: 1.5rem;
    line-height: 1.2;
}
.stat-value.success { color: #6dbf67; text-shadow: 0 0 10px #6dbf6755; }
.stat-value.failure { color: #c04c4c; text-shadow: 0 0 10px #c04c4c55; }
.stat-value.neutral { color: #c9a84c; }
.stat-value.damage  { color: #e07b39; text-shadow: 0 0 10px #e07b3955; font-size: 1.8rem; }

/* Damage row gets a slightly warmer border to distinguish it */
.damage-row .stat-box { border-color: #5a3a1a; }

.bar-track {
    background: #0d0d0d;
    border: 1px solid #3a2e1a;
    border-radius: 3px;
    height: 10px;
    margin-top: 0.5rem;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #4a9a44, #6dbf67);
}
</style>
""", unsafe_allow_html=True)


# ── Core logic ────────────────────────────────────────────────────
def roll_damage(die_sides: int, num_damage_dice: int, dmg_modifier: int, is_crit: bool) -> int:
    """
    Roll damage for one hit.
    Normal : (sum of dice + modifier)
    Crit   : (sum of dice + modifier) x 2   ← homebrew rule
    """
    roll = sum(random.randint(1, die_sides) for _ in range(num_damage_dice))
    total = roll + dmg_modifier
    return total * 2 if is_crit else total


def roll_horde(
    num_dice: int,
    atk_modifier: int,
    threshold: int,
    advantage: int,
    die_sides: int,
    num_damage_dice: int,
    dmg_modifier: int,
) -> dict:
    def single_roll():
        if advantage == 0:
            return random.randint(1, 20)
        a, b = random.randint(1, 20), random.randint(1, 20)
        return max(a, b) if advantage == 1 else min(a, b)

    total_damage  = 0
    crit_damage   = 0
    normal_damage = 0
    successes = 0
    nat_20s   = 0
    nat_1s    = 0

    for _ in range(num_dice):
        raw = single_roll()
        atk_total = raw + atk_modifier

        if raw == 20:
            is_crit = True
            hit     = True
        elif raw == 1:
            is_crit = False
            hit     = False
        else:
            is_crit = False
            hit     = atk_total >= threshold

        if raw == 20:
            nat_20s += 1
        if raw == 1:
            nat_1s += 1

        if hit:
            successes += 1
            dmg = roll_damage(die_sides, num_damage_dice, dmg_modifier, is_crit)
            total_damage += dmg
            if is_crit:
                crit_damage += dmg
            else:
                normal_damage += dmg

    failures     = num_dice - successes
    normal_hits  = successes - nat_20s

    return {
        "successes":    successes,
        "failures":     failures,
        "nat_20s":      nat_20s,
        "nat_1s":       nat_1s,
        "hit_rate":     successes / num_dice * 100,
        "total_damage": total_damage,
        "crit_damage":  crit_damage,
        "normal_damage":normal_damage,
        "avg_dmg_hit":  total_damage / successes if successes else 0,
    }


# ── Session state ─────────────────────────────────────────────────
if "targets" not in st.session_state:
    st.session_state.targets = [
        {"name": "Fighter", "ac": 18, "adv": "Normal"},
        {"name": "Rogue",   "ac": 15, "adv": "Normal"},
        {"name": "Wizard",  "ac": 12, "adv": "Normal"},
        {"name": "Cleric",  "ac": 16, "adv": "Normal"},
    ]

def add_target():
    st.session_state.targets.append({
        "name": f"Target {len(st.session_state.targets) + 1}",
        "ac": 14,
        "adv": "Normal",
    })

def remove_target(i):
    st.session_state.targets.pop(i)


# ── Header ────────────────────────────────────────────────────────
st.markdown('<div class="title-text">⚔ Horde Roller ⚔</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">For the Glory of the Clerics</div>', unsafe_allow_html=True)
st.markdown('<div class="rune-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

# ── Horde Settings ────────────────────────────────────────────────
st.markdown('<div class="section-header">⚔ Horde Settings</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    num_dice     = st.number_input("Number of Dice", min_value=1, max_value=10000, value=500, step=50)
with col2:
    atk_modifier = st.number_input("Attack Modifier", min_value=-20, max_value=20, value=3, step=1)

# ── Damage Settings ───────────────────────────────────────────────
st.markdown('<div class="section-header" style="margin-top:1rem;">🩸 Damage</div>', unsafe_allow_html=True)

die_options = {"d4": 4, "d6": 6, "d8": 8, "d10": 10, "d12": 12, "d20": 20}

col3, col4, col5 = st.columns(3)
with col3:
    num_damage_dice = st.number_input("No. of Damage Dice", min_value=1, max_value=20, value=1, step=1)
with col4:
    die_label  = st.selectbox("Die Type", options=list(die_options.keys()), index=1)
    die_sides  = die_options[die_label]
with col5:
    dmg_modifier = st.number_input("Damage Modifier", min_value=-20, max_value=20, value=3, step=1)

dmg_sign = "+" if dmg_modifier >= 0 else ""
st.markdown(
    f'<div style="font-family:Crimson Text,serif;font-style:italic;color:#8a7560;font-size:0.95rem;margin-top:-0.3rem;">'
    f'Damage formula: {num_damage_dice}{die_label}{dmg_sign}{dmg_modifier} &nbsp;|&nbsp; '
    f'Crit: ({num_damage_dice}{die_label}{dmg_sign}{dmg_modifier}) × 2'
    f'</div>',
    unsafe_allow_html=True,
)

adv_map = {"Normal": 0, "Advantage": 1, "Disadvantage": -1}

st.markdown('<div class="rune-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

# ── Targets ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">🛡 Targets</div>', unsafe_allow_html=True)

adv_options    = ["Normal", "Advantage", "Disadvantage"]
targets_to_remove = None

for i, target in enumerate(st.session_state.targets):
    col_name, col_ac, col_adv, col_remove = st.columns([2.5, 1.1, 1.8, 0.7])
    with col_name:
        st.session_state.targets[i]["name"] = st.text_input(
            "Name", value=target["name"], key=f"name_{i}", label_visibility="collapsed"
        )
    with col_ac:
        st.session_state.targets[i]["ac"] = st.number_input(
            "AC", min_value=1, max_value=30, value=target["ac"], key=f"ac_{i}", label_visibility="collapsed"
        )
    with col_adv:
        st.session_state.targets[i]["adv"] = st.selectbox(
            "Roll Mode",
            options=adv_options,
            index=adv_options.index(target.get("adv", "Normal")),
            key=f"adv_{i}",
            label_visibility="collapsed",
        )
    with col_remove:
        if st.button("✕", key=f"remove_{i}", help="Remove target"):
            targets_to_remove = i

if targets_to_remove is not None:
    remove_target(targets_to_remove)
    st.rerun()

st.button("+ Add Target", on_click=add_target)

st.markdown('<div class="rune-divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

# ── Roll button ───────────────────────────────────────────────────
if st.button("⚔  ROLL THE HORDE  ⚔"):
    if not st.session_state.targets:
        st.warning("Add at least one target before rolling.")
    else:
        atk_sign = "+" if atk_modifier >= 0 else ""
        st.markdown(
            f'<div style="font-family:Crimson Text,serif;font-style:italic;color:#8a7560;text-align:center;margin-bottom:0.5rem;">'
            f'{num_dice}d20 {atk_sign}{atk_modifier} &nbsp;·&nbsp; '
            f'Damage: {num_damage_dice}{die_label}{dmg_sign}{dmg_modifier}'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-header">📜 Results</div>', unsafe_allow_html=True)

        for target in st.session_state.targets:
            target_adv = target.get("adv", "Normal")
            result = roll_horde(
                num_dice, atk_modifier, target["ac"], adv_map[target_adv],
                die_sides, num_damage_dice, dmg_modifier,
            )
            html = textwrap.dedent(f"""
<div class="target-result">
<div class="target-name">{target['name']}<span class="target-ac">AC {target['ac']} · {target_adv}</span></div>
<div class="stat-row">
<div class="stat-box"><div class="stat-label">Hits</div><div class="stat-value success">{result['successes']}</div></div>
<div class="stat-box"><div class="stat-label">Misses</div><div class="stat-value failure">{result['failures']}</div></div>
<div class="stat-box"><div class="stat-label">Hit Rate</div><div class="stat-value neutral">{result['hit_rate']:.1f}%</div><div class="bar-track"><div class="bar-fill" style="width:{result['hit_rate']}%"></div></div></div>
<div class="stat-box"><div class="stat-label">Nat 20s</div><div class="stat-value success">{result['nat_20s']}</div></div>
<div class="stat-box"><div class="stat-label">Nat 1s</div><div class="stat-value failure">{result['nat_1s']}</div></div>
</div>
<div class="stat-row damage-row">
<div class="stat-box"><div class="stat-label">Total Damage</div><div class="stat-value damage">{result['total_damage']}</div></div>
<div class="stat-box"><div class="stat-label">Normal Dmg</div><div class="stat-value neutral">{result['normal_damage']}</div></div>
<div class="stat-box"><div class="stat-label">Crit Dmg</div><div class="stat-value neutral">{result['crit_damage']}</div></div>
<div class="stat-box"><div class="stat-label">Avg / Hit</div><div class="stat-value neutral">{result['avg_dmg_hit']:.1f}</div></div>
</div>
</div>
""")
            st.markdown(html, unsafe_allow_html=True)
