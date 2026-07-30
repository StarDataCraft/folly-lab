"""Folly: tiny, offline-friendly digital playgrounds."""

from __future__ import annotations

import streamlit as st


TODAY_NAME = "The Constellation That Waited for You"
RAIN_NAME = "The Button That Remembers Rain"
SECTIONS = ("Today", "Archive", "Random", "About")
EXPERIMENTS = (TODAY_NAME, RAIN_NAME)
STAR_KINDS = {
    "Glow": {"symbol": "✦", "color": "#fff0ad", "voice": "warm"},
    "Drift": {"symbol": "·", "color": "#c9d9ff", "voice": "quiet"},
    "Dare": {"symbol": "✧", "color": "#ffc4df", "voice": "wild"},
}
STAR_POSITIONS = (
    (17, 26),
    (76, 20),
    (48, 48),
    (25, 72),
    (82, 69),
    (59, 82),
)
STAR_LINES = (
    (17, 26, 76, 20),
    (76, 20, 48, 48),
    (48, 48, 25, 72),
    (48, 48, 82, 69),
    (82, 69, 59, 82),
)


def constellation_result(star_path: tuple[str, ...]) -> tuple[str, str]:
    """Name a finished sky from the player's chosen sequence."""
    counts = {kind: star_path.count(kind) for kind in STAR_KINDS}
    if len(set(star_path)) == 1:
        return {
            "Glow": ("The Steadfast Lantern", "It kept one promise six times."),
            "Drift": ("The Patient Tide", "It crossed the sky without hurrying."),
            "Dare": ("The Beautiful Trouble", "It refused every straight answer."),
        }[star_path[0]]
    if star_path[0] == star_path[-1]:
        return "The Returning Comet", "It wandered far enough to choose its beginning."
    if all(count == 2 for count in counts.values()):
        return "The Impossible Balance", "Three instincts agreed to share one sky."
    dominant = max(STAR_KINDS, key=counts.get)
    return {
        "Glow": ("The Kind Conspiracy", "Its brightest stars quietly recruited the rest."),
        "Drift": ("The Sideways River", "It found a route the map had overlooked."),
        "Dare": ("The Unbuttoned Crown", "It became royal by ignoring the instructions."),
    }[dominant]


def constellation_markup(star_path: tuple[str, ...]) -> str:
    """Return the deterministic pocket sky for the current interaction state."""
    stars = "".join(
        (
            f'<span class="star" data-kind="{kind}" '
            f'style="left:{x}%;top:{y}%;color:{STAR_KINDS[kind]["color"]}">'
            f'{STAR_KINDS[kind]["symbol"]}</span>'
        )
        for (x, y), kind in zip(STAR_POSITIONS, star_path)
    )
    lines = "".join(
        (
            f'<line class="{star_path[index + 1].lower()}" '
            f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'
        )
        for index, (x1, y1, x2, y2) in enumerate(
            STAR_LINES[: max(0, len(star_path) - 1)]
        )
    )
    if not star_path:
        message = "The sky is listening."
    elif len(star_path) < 3:
        message = f"A {STAR_KINDS[star_path[-1]]['voice']} star has answered."
    elif len(star_path) < len(STAR_POSITIONS):
        leading = max(STAR_KINDS, key=star_path.count)
        message = f"It is leaning {STAR_KINDS[leading]['voice']}… for now."
    else:
        message = "The pattern has chosen its name."
    return (
        '<div class="sky" data-testid="constellation-sky">'
        '<div class="orbit"></div>'
        f'<svg class="threads" viewBox="0 0 100 100">{lines}</svg>'
        f"{stars}<span class=\"sky-note\">{message}</span></div>"
    )


st.set_page_config(page_title="Folly · a tiny digital playground", page_icon="✦")

st.markdown(
    """
    <style>
    :root { --ink:#242135; --plum:#5c3f78; --paper:#fbf8f2; --sun:#f2bb66; }
    .stApp {
        color:var(--ink);
        background:
          radial-gradient(circle at 8% 8%, #f6dfc5 0, transparent 26rem),
          radial-gradient(circle at 95% 45%, #e4dcf0 0, transparent 28rem),
          var(--paper);
    }
    .block-container { max-width:760px; padding-top:2.5rem; padding-bottom:3rem; }
    h1 { letter-spacing:-.055em !important; font-size:clamp(3rem, 10vw, 5.6rem) !important; }
    h2, h3 { letter-spacing:-.025em !important; }
    [data-testid="stCaptionContainer"] { color:#6e6878; }
    div[role="radiogroup"] {
        gap:.35rem; padding:.35rem; border:1px solid #ddd2c5; border-radius:999px;
        background:rgba(255,255,255,.58);
    }
    div[role="radiogroup"] label {
        flex:1; justify-content:center; margin:0; padding:.35rem .6rem;
        border-radius:999px;
    }
    div[role="radiogroup"] label:has(input:checked) { background:#fff; box-shadow:0 2px 12px #48345418; }
    div[role="radiogroup"] [data-testid="stMarkdownContainer"] p { font-size:.9rem; }
    .eyebrow { color:var(--plum); font-size:.72rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase; }
    .intro { font-size:1.15rem; max-width:35rem; color:#514b59; }
    .sky {
        height:clamp(300px, 52vw, 410px); position:relative; overflow:hidden;
        border-radius:2rem; margin:1.25rem 0 1rem;
        background:radial-gradient(circle at 48% 48%, #41416b 0, #252542 48%, #17172c 100%);
        box-shadow:0 24px 70px #2e244533, inset 0 0 80px #c7a6ff12;
    }
    .orbit { position:absolute; width:300px; height:300px; left:50%; top:50%;
        transform:translate(-50%,-50%) rotate(-12deg); border:1px solid #f4d6a71f; border-radius:50%; }
    .star { position:absolute; transform:translate(-50%,-50%); color:#fff4ce;
        font-size:1.65rem; text-shadow:0 0 15px #ffd999; animation:arrive .65s ease both; z-index:2; }
    .threads { position:absolute; inset:0; width:100%; height:100%; }
    .threads line { stroke:#edcfaa; stroke-width:.32; opacity:.62; }
    .threads line.glow { stroke:#fff0ad; }
    .threads line.drift { stroke:#aabfe8; stroke-dasharray:1.5 1; }
    .threads line.dare { stroke:#ffafd2; stroke-width:.5; }
    .sky-note { position:absolute; left:1.4rem; bottom:1.2rem; color:#d8d3e7;
        font-size:.78rem; letter-spacing:.08em; }
    .result-card { margin:.9rem 0; padding:1.1rem 1.3rem; border-radius:1.2rem;
        color:#fdf8ed; background:linear-gradient(120deg,#4f3f72,#854f73);
        box-shadow:0 12px 35px #4f3f7230; animation:arrive .65s ease both; }
    .result-card b { display:block; font-size:1.15rem; margin-bottom:.2rem; }
    .archive-card { padding:1.2rem 1.35rem; border:1px solid #ddd2c5; border-radius:1.3rem;
        background:rgba(255,255,255,.52); margin:.75rem 0; }
    .release { margin-top:3rem; padding-top:1rem; border-top:1px solid #ddd2c5; color:#7c7381; font-size:.75rem; }
    .stButton > button { border-radius:999px; min-height:2.8rem; font-weight:650; }
    @keyframes arrive { from { opacity:0; transform:translate(-50%,-50%) scale(2); } }
    @media(max-width:640px) {
        .block-container { padding:1.5rem 1rem 2rem; }
        div[role="radiogroup"] { gap:0; }
        div[role="radiogroup"] label { padding:.25rem .15rem; }
        .sky { border-radius:1.35rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "star_path" not in st.session_state:
    st.session_state.star_path = []
if "random_index" not in st.session_state:
    st.session_state.random_index = 0

st.markdown('<div class="eyebrow">One unnecessary joy at a time</div>', unsafe_allow_html=True)
st.title("Folly")
section = st.radio(
    "Explore Folly",
    SECTIONS,
    horizontal=True,
    label_visibility="collapsed",
    key="section_nav",
)

if section == "Today":
    st.caption("TODAY · FOLLY № 2")
    st.header(TODAY_NAME)
    st.markdown(
        '<p class="intro">Choose how each star arrives. Your six choices will name the sky.</p>',
        unsafe_allow_html=True,
    )
    star_path = tuple(st.session_state.star_path)
    st.markdown(constellation_markup(star_path), unsafe_allow_html=True)
    placed = len(star_path)
    st.radio(
        "How should the next star arrive?",
        STAR_KINDS,
        horizontal=True,
        key="star_kind",
        disabled=placed >= len(STAR_POSITIONS),
    )
    left, right = st.columns(2)
    if left.button(
        "Place a star" if placed < len(STAR_POSITIONS) else "All stars placed",
        type="primary",
        key="place_star",
        disabled=placed >= len(STAR_POSITIONS),
        use_container_width=True,
    ):
        st.session_state.star_path.append(st.session_state.star_kind)
        st.rerun()
    if right.button(
        "Try another sky" if placed == len(STAR_POSITIONS) else "Clear the sky",
        key="reset_stars",
        use_container_width=True,
    ):
        st.session_state.star_path = []
        st.rerun()
    st.caption(f"Stars placed: {placed} / {len(STAR_POSITIONS)}")
    if placed == len(STAR_POSITIONS):
        result_name, result_note = constellation_result(star_path)
        st.markdown(
            f'<div class="result-card" data-testid="constellation-result">'
            f"<b>{result_name}</b>{result_note}</div>",
            unsafe_allow_html=True,
        )

elif section == "Archive":
    st.header("Archive")
    st.write("A shelf for every finished piece of delightful nonsense.")
    st.markdown(
        f'<div class="archive-card"><b>№ 2 · {TODAY_NAME}</b><br>'
        "Place stars until a private constellation appears.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="archive-card"><b>№ 1 · {RAIN_NAME}</b><br>'
        "Click a button to add remembered rain to a text cloud.</div>",
        unsafe_allow_html=True,
    )

elif section == "Random":
    st.header("Random")
    st.write("Let chance choose a tiny place to begin.")
    if st.button("Surprise me", type="primary", key="random_folly"):
        st.session_state.random_index = (st.session_state.random_index + 1) % len(EXPERIMENTS)
    st.subheader(EXPERIMENTS[st.session_state.random_index])
    st.caption("A valid selection from the Folly archive.")

else:
    st.header("About")
    st.markdown(
        '<p class="intro">Folly is a tiny digital playground: one clear interaction, '
        "no practical purpose, and just enough surprise to make the day feel less inevitable.</p>",
        unsafe_allow_html=True,
    )
    st.write("Made offline with Python, Streamlit, session state, CSS, and unreasonable restraint.")

st.markdown(
    '<div class="release">FOLLY № 2 · JULY 2026 · NO DATA COLLECTED, NOTHING TO OPTIMIZE</div>',
    unsafe_allow_html=True,
)
