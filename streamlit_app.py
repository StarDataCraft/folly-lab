"""Folly: a tiny, offline-friendly Streamlit experiment."""

import streamlit as st


FOLLY_NAME = "The Button That Remembers Rain"
RAIN_STAGES = (
    "☁",
    "☁  ·",
    "☁  ·  ·",
    "☁  ┆  ·",
    "☁  ┆  ┆",
    "☁  ╎  ┆  ╎",
)


st.set_page_config(page_title="Folly", page_icon="☁️", layout="centered")

if "rain_memory" not in st.session_state:
    st.session_state.rain_memory = 0

st.title("Folly")
st.subheader(FOLLY_NAME)
st.write("Each click teaches this small cloud to remember one more trace of rain.")

if st.button("Remember one drop", type="primary", key="remember_rain"):
    st.session_state.rain_memory = min(
        st.session_state.rain_memory + 1,
        len(RAIN_STAGES) - 1,
    )

if st.button("Reset the sky", key="reset_rain"):
    st.session_state.rain_memory = 0

st.markdown(f"## {RAIN_STAGES[st.session_state.rain_memory]}")
st.caption(f"Rain remembered: {st.session_state.rain_memory} / 5")

st.header("Today")
st.write("A cloud practices the smallest possible kind of memory.")

st.header("Archive")
st.write("Day 1 — The Button That Remembers Rain.")

st.header("Random")
st.write("Today there is only one Folly, so chance returns you to the rain.")

st.header("About")
st.write("Folly is a tiny daily experiment: one idea, one interaction, then stop.")
