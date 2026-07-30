from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).parents[1] / "streamlit_app.py"
SECTION_NAMES = {"Today", "Archive", "Random", "About"}


def launch_app() -> AppTest:
    return AppTest.from_file(str(APP_PATH)).run()


def test_app_launches_and_shows_core_experience() -> None:
    app = launch_app()

    assert not app.exception
    assert any(title.value == "Folly" for title in app.title)
    assert app.button(key="remember_rain").label == "Remember one drop"
    assert SECTION_NAMES.issubset({header.value for header in app.header})


def test_primary_button_changes_the_cloud() -> None:
    app = launch_app()
    initial_caption = app.caption[0].value

    app.button(key="remember_rain").click().run()

    assert not app.exception
    assert app.caption[0].value != initial_caption
    assert app.caption[0].value == "Rain remembered: 1 / 5"


def test_reset_restores_the_initial_state_and_sections() -> None:
    app = launch_app()
    app.button(key="remember_rain").click().run()
    app.button(key="remember_rain").click().run()
    assert app.caption[0].value == "Rain remembered: 2 / 5"

    app.button(key="reset_rain").click().run()

    assert not app.exception
    assert app.caption[0].value == "Rain remembered: 0 / 5"
    assert SECTION_NAMES.issubset({header.value for header in app.header})
