# Folly

Folly is a tiny Streamlit experiment built to prove a compact delivery loop:

> IDEA → BUILD → TEST → REPAIR → PULL REQUEST → DEPLOY

The first demonstration is **The Button That Remembers Rain**. Click the primary
button and a text-based cloud remembers progressively more rain. Reset returns
the sky to its initial state.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app is self-contained and does not require network access at runtime.

## Test

```bash
python -m pytest
python -m compileall -q streamlit_app.py tests
```

The tests use Streamlit AppTest to verify launch, interaction, reset behavior,
and the permanent Today, Archive, Random, and About sections.
