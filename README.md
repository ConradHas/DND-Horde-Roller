# Horde Roller

A D&D tool for simulating a large number of attacks at once. Built with Python and Streamlit.

## Features

- Roll hundreds or thousands of D20s in a single click
- Set an attack modifier and per-target AC
- Per-target advantage / disadvantage
- Damage calculator with configurable dice (d4 through d20) and a flat modifier
- Homebrew critical hit rule: full damage (roll + modifier) is doubled on a nat 20
- Add and remove targets on the fly — great for tracking a full party in one roll

## How to Run Locally

**Requirements:** Python 3.8+

```
pip install streamlit
streamlit run horde_roller_app.py
```

Then open `http://localhost:8501` in your browser.

## How to Use

1. Set your **Number of Dice** and **Attack Modifier** under Horde Settings
2. Configure your **Damage** dice, die type, and damage modifier
3. Add your party members as targets — each with their own AC and roll mode
4. Hit **Roll the Horde** to see hits, misses, and total damage per target

## Crit Rule

This tool uses a homebrew critical hit rule. Instead of rolling extra dice, the full damage value (dice roll + modifier) is doubled.

**Example:** 1d6+3 rolls a 4 → 4+3 = 7 → crit deals 14
