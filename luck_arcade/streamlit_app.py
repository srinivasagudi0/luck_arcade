import datetime
import random
import time

import streamlit as st


def init_state():
    defaults = {
        "coin_attempts_total": 0,
        "coin_round_attempts": 0,
        "coin_wins": 0,
        "dice_attempts_total": 0,
        "dice_round_attempts": 0,
        "dice_wins": 0,
        "random_attempts_total": 0,
        "random_round_attempts": 0,
        "random_wins": 0,
        "random_target": None,
        "random_level": None,
        "streak_current": 0,
        "streak_best": 0,
        "history_attempts": [],
        "daily_target": None,
        "daily_attempts": 0,
        "daily_completed": False,
        "daily_key": None,
        "blitz_runs": 0,
        "blitz_best_hits": 0,
        "theme_choice": "Arcade Neon",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)



def reset_stats():
    for key in list(st.session_state.keys()):
        if key.endswith("_wins") or key.endswith("_attempts_total") or key.endswith("_round_attempts"):
            st.session_state[key] = 0
    st.session_state.streak_current = 0
    st.session_state.streak_best = 0
    st.session_state.history_attempts = []
    st.session_state.daily_attempts = 0
    st.session_state.daily_completed = False
    st.session_state.blitz_runs = 0
    st.session_state.blitz_best_hits = 0


THEMES = {
    "Arcade Neon": {
        "font": "'Space Grotesk', 'Helvetica Neue', sans-serif",
        "bg": """radial-gradient(circle at 20% 20%, rgba(0,169,173,0.18), transparent 25%),
                 radial-gradient(circle at 80% 0%, rgba(255,140,0,0.18), transparent 25%),
                 linear-gradient(135deg, #0b1b2b 0%, #0f2435 45%, #0f1f2d 100%)""",
        "card": "rgba(255,255,255,0.06)",
        "accent": "#00f0ff",
        "text": "#e6f1ff",
    },
    "Retro Pixel": {
        "font": "'Press Start 2P', 'Courier New', monospace",
        "bg": """linear-gradient(135deg, #111 0%, #1a1a1a 45%, #111 100%),
                 repeating-linear-gradient(90deg, rgba(255,255,255,0.04), rgba(255,255,255,0.04) 1px, transparent 1px, transparent 10px)""",
        "card": "rgba(32,32,32,0.8)",
        "accent": "#ffdf00",
        "text": "#f4f4f4",
    },
}


def render_style(theme: str):
    data = THEMES[theme]
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=Press+Start+2P&display=swap');
        html, body, [class*="css"] {{
            font-family: {data['font']};
        }}
        .app-bg {{
            background: {data['bg']};
            padding: 2rem;
            border-radius: 16px;
            color: {data['text']};
            animation: float-bg 14s ease-in-out infinite alternate;
        }}
        .card {{
            background: {data['card']};
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 20px 45px rgba(0,0,0,0.25);
            transition: transform 0.35s ease, box-shadow 0.35s ease;
        }}
        .card:hover {{
            transform: translateY(-6px);
            box-shadow: 0 25px 60px rgba(0,0,0,0.35);
        }}
        .hero-title {{
            font-size: 2.2rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
            animation: glow 6s ease-in-out infinite;
            color: {data['accent']};
        }}
        .hero-sub {{
            color: #c7d7f2;
            margin-bottom: 1rem;
        }}
        .metric-chip {{
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            text-align: center;
        }}
        .metric-chip h3 {{
            margin: 0;
            font-size: 1.4rem;
        }}
        .metric-chip small {{
            color: #c7d7f2;
        }}
        @keyframes float-bg {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 100% 50%; }}
        }}
        @keyframes glow {{
            0% {{ text-shadow: 0 0 10px rgba(0,255,255,0.15); }}
            50% {{ text-shadow: 0 0 24px rgba(0,255,255,0.35); }}
            100% {{ text-shadow: 0 0 10px rgba(0,255,255,0.15); }}
        }}
        .pulse {{
            position: relative;
            overflow: hidden;
        }}
        .pulse::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 55%);
            animation: pulse 2.8s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(0.9); opacity: 0.8; }}
            50% {{ transform: scale(1.05); opacity: 0.4; }}
            100% {{ transform: scale(0.9); opacity: 0.8; }}
        }}
        .pill {{
            display: inline-block;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.12);
            background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
            color: {data['text']};
            font-size: 0.85rem;
        }}
        .glow-line {{
            height: 1px;
            background: linear-gradient(90deg, transparent, {data['accent']}, transparent);
            margin: 1.2rem 0;
        }}
        .progress-shell {{
            width: 100%;
            background: rgba(255,255,255,0.08);
            border-radius: 999px;
            padding: 4px;
            border: 1px solid rgba(255,255,255,0.12);
        }}
        .progress-fill {{
            height: 12px;
            border-radius: 999px;
            background: linear-gradient(90deg, {data['accent']}, #ff6f61);
            width: 0%;
            transition: width 0.4s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def stats_bar():
    total_attempts = (
        st.session_state.coin_attempts_total
        + st.session_state.dice_attempts_total
        + st.session_state.random_attempts_total
    )
    total_wins = (
        st.session_state.coin_wins
        + st.session_state.dice_wins
        + st.session_state.random_wins
    )
    win_rate = f"{(total_wins / total_attempts * 100):.0f}%" if total_attempts else "—"

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-chip"><small>Total attempts</small><h3>{total_attempts}</h3></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-chip"><small>Total wins</small><h3>{total_wins}</h3></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-chip"><small>Win rate</small><h3>{win_rate}</h3></div>', unsafe_allow_html=True)
    c4.markdown(
        f'<div class="metric-chip"><small>Streak</small><h3>{st.session_state.streak_current} / {st.session_state.streak_best} best</h3></div>',
        unsafe_allow_html=True,
    )

    if st.session_state.history_attempts:
        st.caption("Attempts trend (last 30):")
        st.line_chart(st.session_state.history_attempts, height=150)


def log_attempt():
    total_attempts = (
        st.session_state.coin_attempts_total
        + st.session_state.dice_attempts_total
        + st.session_state.random_attempts_total
    )
    st.session_state.history_attempts.append(total_attempts)
    st.session_state.history_attempts = st.session_state.history_attempts[-30:]


def record_win():
    st.session_state.streak_current += 1
    st.session_state.streak_best = max(st.session_state.streak_best, st.session_state.streak_current)
    if st.session_state.streak_current and st.session_state.streak_current % 3 == 0:
        st.snow()


def reset_streak():
    st.session_state.streak_current = 0


def streak_meter():
    milestone = max(3, ((st.session_state.streak_current // 3) + 1) * 3)
    progress = min(st.session_state.streak_current / milestone, 1.0) if milestone else 0
    percent = int(progress * 100)
    st.markdown(
        f"""
        <div class="progress-shell">
            <div class="progress-fill" style="width:{percent}%"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Current streak: {st.session_state.streak_current} · Next milestone: {milestone}")


def status_row():
    daily_status = "Completed" if st.session_state.daily_completed else "Open"
    next_goal = max(1, st.session_state.streak_best + 1)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<span class="pill">Theme: {st.session_state.theme_choice}</span>', unsafe_allow_html=True)
    c2.markdown(f'<span class="pill">Daily: {daily_status}</span>', unsafe_allow_html=True)
    c3.markdown(f'<span class="pill">Best streak: {st.session_state.streak_best} · Next: {next_goal}</span>', unsafe_allow_html=True)


def coin_game():
    st.subheader("Flip a Coin · easy")
    st.write("Pick your side and try to match the flip.")

    side = st.radio("Choose your side", ("Heads", "Tails"), horizontal=True, key="coin_side")
    flip_placeholder = st.empty()

    if st.button("Flip the coin", use_container_width=True, key="coin_flip"):
        # Quick flip animation before revealing the result
        for _ in range(10):
            flip_placeholder.markdown(f"### {random.choice(['Heads', 'Tails'])}")
            time.sleep(0.08)

        st.session_state.coin_attempts_total += 1
        st.session_state.coin_round_attempts += 1
        result = random.choice(["Heads", "Tails"])
        flip_placeholder.markdown(f"### Result: {result}")
        log_attempt()
        if result == side:
            st.session_state.coin_wins += 1
            record_win()
            st.success(
                f"The coin shows {result}! You guessed it in {st.session_state.coin_round_attempts} attempt(s)."
            )
            st.balloons()
            st.session_state.coin_round_attempts = 0
        else:
            st.info(f"The coin shows {result}. Try again!")
            reset_streak()

    st.caption(f"Attempts this round: {st.session_state.coin_round_attempts}")


def dice_game():
    st.subheader("Roll a Dice · medium")
    st.write("Choose your lucky number and roll until you hit it.")

    lucky_number = st.slider("Choose your lucky number", min_value=1, max_value=6, value=3, key="dice_slider")
    roll_placeholder = st.empty()

    if st.button("Roll the dice", use_container_width=True, key="dice_roll"):
        # Rolling animation
        for _ in range(12):
            roll_placeholder.markdown(f"### 🎲 {random.randint(1, 6)}")
            time.sleep(0.06)

        st.session_state.dice_attempts_total += 1
        st.session_state.dice_round_attempts += 1
        roll = random.randint(1, 6)
        roll_placeholder.markdown(f"### Result: 🎲 {roll}")
        log_attempt()
        if roll == lucky_number:
            st.session_state.dice_wins += 1
            record_win()
            st.success(
                f"You rolled a {roll}! Jackpot in {st.session_state.dice_round_attempts} attempt(s)."
            )
            st.balloons()
            st.session_state.dice_round_attempts = 0
        else:
            st.warning(f"You rolled a {roll}. No match yet.")
            reset_streak()

    st.caption(f"Attempts this round: {st.session_state.dice_round_attempts}")


def random_number_game():
    st.subheader("Pick a Random Number · hard")
    st.write("Select a difficulty, then guess the secret number.")

    levels = {
        "Easy (1-10)": 10,
        "Medium (1-50)": 50,
        "Hard (1-100)": 100,
        "Nightmare (1-500)": 500,
    }

    level_label = st.selectbox("Choose difficulty", list(levels.keys()), key="level_select")
    max_number = levels[level_label]

    def reset_target():
        st.session_state.random_level = level_label
        st.session_state.random_target = random.randint(1, max_number)
        st.session_state.random_round_attempts = 0

    if st.session_state.random_target is None:
        reset_target()
    elif st.session_state.random_level != level_label:
        reset_target()

    guess = st.number_input(
        f"Enter your guess (1 to {max_number})",
        min_value=1,
        max_value=max_number,
        value=1,
        step=1,
        key="guess_input",
    )

    if st.button("Submit guess", use_container_width=True, key="submit_guess"):
        st.session_state.random_attempts_total += 1
        st.session_state.random_round_attempts += 1
        target = st.session_state.random_target
        log_attempt()

        if guess == target:
            st.session_state.random_wins += 1
            record_win()
            st.success(
                f"YOU NAILED IT! The number was {target}. "
                f"It took you {st.session_state.random_round_attempts} attempt(s)."
            )
            st.balloons()
            reset_target()
        elif guess < target:
            st.info("Too low! Aim higher.")
            reset_streak()
        else:
            st.info("Too high! Aim lower.")
            reset_streak()

    if st.button("Start a new number", key="new_number", use_container_width=True):
        reset_target()
        st.toast("New number picked! Start guessing.", icon="🎯")

    st.caption(f"Attempts this round: {st.session_state.random_round_attempts}")

    st.markdown("#### Daily Challenge (1-100)")
    today = datetime.date.today().isoformat()
    if st.session_state.daily_key != today or st.session_state.daily_target is None:
        st.session_state.daily_key = today
        seeded = random.Random(int(datetime.date.today().strftime("%Y%m%d")))
        st.session_state.daily_target = seeded.randint(1, 100)
        st.session_state.daily_attempts = 0
        st.session_state.daily_completed = False

    daily_guess = st.number_input("Daily guess", min_value=1, max_value=100, value=50, step=1, key="daily_guess")
    if st.button("Submit daily guess", key="daily_submit", use_container_width=True, disabled=st.session_state.daily_completed):
        st.session_state.daily_attempts += 1
        st.session_state.random_attempts_total += 1
        log_attempt()
        if daily_guess == st.session_state.daily_target:
            st.session_state.daily_completed = True
            st.session_state.random_wins += 1
            record_win()
            st.success(f"Daily cracked! The number was {st.session_state.daily_target}. Attempts: {st.session_state.daily_attempts}.")
            st.balloons()
        elif daily_guess < st.session_state.daily_target:
            st.info("Too low for today’s number.")
            reset_streak()
        else:
            st.info("Too high for today’s number.")
            reset_streak()

    if st.session_state.daily_completed:
        st.toast("Daily challenge done. Come back tomorrow!", icon="✅")


def time_attack():
    st.subheader("Time Attack Blitz")
    st.write("Auto-rolls a burst of dice—maximize hits on your chosen number.")

    target = st.slider("Pick your target", min_value=1, max_value=6, value=3, key="blitz_target")
    rolls = st.slider("Number of rolls", min_value=6, max_value=24, value=12, step=2, key="blitz_rolls")
    speed_ms = st.slider("Speed per roll (ms)", min_value=40, max_value=180, value=80, step=10, key="blitz_speed")

    placeholder = st.empty()
    if st.button("Start blitz", use_container_width=True, key="blitz_start"):
        hits = 0
        for i in range(rolls):
            roll = random.randint(1, 6)
            placeholder.markdown(f"### Roll {i + 1}/{rolls}: 🎲 {roll}")
            if roll == target:
                hits += 1
            time.sleep(speed_ms / 1000)

        st.session_state.blitz_runs += 1
        st.session_state.blitz_best_hits = max(st.session_state.blitz_best_hits, hits)
        st.info(f"Blitz over! You hit {hits} out of {rolls}. Best: {st.session_state.blitz_best_hits}")
        st.session_state.dice_attempts_total += rolls
        st.session_state.dice_wins += hits
        st.session_state.dice_round_attempts = 0
        log_attempt()
        if hits:
            record_win()
            st.balloons()
        else:
            st.warning("No hits this time—go again!")
            reset_streak()


def main():
    st.set_page_config(page_title="Luck Arcade", page_icon="🎲", layout="wide")
    init_state()

    with st.container():
        st.markdown('<div class="app-bg">', unsafe_allow_html=True)
        st.session_state.theme_choice = st.sidebar.radio("Theme", ["Arcade Neon", "Retro Pixel"], index=0)
        render_style(st.session_state.theme_choice)
        st.markdown('<div class="hero-title">Luck Arcade</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Play quick-fire chance games with sleek feedback, light animations, and live stats.</div>', unsafe_allow_html=True)
        status_row()
        streak_meter()
        stats_bar()
        reset_col = st.columns(3)[2]
        with reset_col:
            if st.button("Reset stats", key="reset_stats"):
                reset_stats()
                st.toast("Stats cleared. Fresh start!", icon="♻️")
        st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)
        st.markdown("---")
        tabs = st.tabs(["Flip a Coin", "Roll a Dice", "Pick a Random Number", "Time Attack"])

        with tabs[0]:
            st.markdown('<div class="card pulse">', unsafe_allow_html=True)
            coin_game()
            st.markdown('</div>', unsafe_allow_html=True)

        with tabs[1]:
            st.markdown('<div class="card pulse">', unsafe_allow_html=True)
            dice_game()
            st.markdown('</div>', unsafe_allow_html=True)

        with tabs[2]:
            st.markdown('<div class="card pulse">', unsafe_allow_html=True)
            random_number_game()
            st.markdown('</div>', unsafe_allow_html=True)

        with tabs[3]:
            st.markdown('<div class="card pulse">', unsafe_allow_html=True)
            time_attack()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
