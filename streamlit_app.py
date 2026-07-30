"""Folly: tiny, offline-friendly digital playgrounds."""

import streamlit as st


TODAY_NAME = "The Constellation That Waited for You"
RAIN_NAME = "The Button That Remembers Rain"
SECTIONS = ("Today", "Archive", "Random", "About")
EXPERIMENTS = (TODAY_NAME, RAIN_NAME)
STAR_POSITIONS = (
    (17, 26, "✦"),
    (76, 20, "·"),
    (48, 48, "✧"),
    (25, 72, "·"),
    (82, 69, "✦"),
    (59, 82, "·"),
)
STAR_LINES = (
    (17, 26, 76, 20),
    (76, 20, 48, 48),
    (48, 48, 25, 72),
    (48, 48, 82, 69),
    (82, 69, 59, 82),
)


def constellation_markup(star_count: int) -> str:
    """Return the deterministic pocket sky for the current interaction state."""
    stars = "".join(
        (
            f'<span class="star" style="left:{x}%;top:{y}%">'
            f"{symbol}</span>"
        )
        for x, y, symbol in STAR_POSITIONS[:star_count]
    )
    lines = "".join(
        (
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'
        )
        for x1, y1, x2, y2 in STAR_LINES[: max(0, star_count - 1)]
    )
    message = (
        "The sky is listening."
        if star_count == 0
        else "A small pattern is beginning."
        if star_count < len(STAR_POSITIONS)
        else "It was waiting to become this."
    )
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
    .sky-note { position:absolute; left:1.4rem; bottom:1.2rem; color:#d8d3e7;
        font-size:.78rem; letter-spacing:.08em; }
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

if "star_count" not in st.session_state:
    st.session_state.star_count = 0
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
        '<p class="intro">Place six quiet stars. They will decide how they know one another.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(constellation_markup(st.session_state.star_count), unsafe_allow_html=True)
    placed = st.session_state.star_count
    left, right = st.columns(2)
    if left.button(
        "Place a star" if placed < len(STAR_POSITIONS) else "All stars placed",
        type="primary",
        key="place_star",
        disabled=placed >= len(STAR_POSITIONS),
        use_container_width=True,
    ):
        st.session_state.star_count += 1
        st.rerun()
    if right.button("Clear the sky", key="reset_stars", use_container_width=True):
        st.session_state.star_count = 0
        st.rerun()
    st.caption(f"Stars placed: {placed} / {len(STAR_POSITIONS)}")

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
