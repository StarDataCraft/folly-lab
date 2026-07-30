from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).parents[1] / "streamlit_app.py"
SECTIONS = ("Today", "Archive", "Random", "About")
NEW_FOLLY = "The Constellation That Waited for You"
RAIN_FOLLY = "The Button That Remembers Rain"


def launch_app() -> AppTest:
    return AppTest.from_file(str(APP_PATH)).run(timeout=10)


def navigate(app: AppTest, section: str) -> AppTest:
    app.radio(key="section_nav").set_value(section).run()
    return app


def test_app_launches_with_navigation_and_new_folly() -> None:
    app = launch_app()

    assert not app.exception
    assert any(title.value == "Folly" for title in app.title)
    assert app.radio(key="section_nav").options == list(SECTIONS)
    assert any(header.value == NEW_FOLLY for header in app.header)
    assert app.radio(key="star_kind").options == ["Glow", "Drift", "Dare"]
    assert app.button(key="place_star").label == "Place a star"


def test_placing_a_star_changes_visible_state() -> None:
    app = launch_app()
    assert app.caption[-1].value == "Stars placed: 0 / 6"

    app.button(key="place_star").click().run()

    assert not app.exception
    assert app.caption[-1].value == "Stars placed: 1 / 6"
    sky = next(item.value for item in app.markdown if "constellation-sky" in item.value)
    assert 'data-kind="Glow"' in sky


def test_clear_sky_replays_from_initial_state() -> None:
    app = launch_app()
    app.button(key="place_star").click().run()
    app.button(key="place_star").click().run()
    assert app.caption[-1].value == "Stars placed: 2 / 6"

    app.button(key="reset_stars").click().run()

    assert not app.exception
    assert app.caption[-1].value == "Stars placed: 0 / 6"
    assert "The sky is listening." in " ".join(item.value for item in app.markdown)


def complete_path(app: AppTest, choices: list[str]) -> AppTest:
    for choice in choices:
        app.radio(key="star_kind").set_value(choice).run()
        app.button(key="place_star").click().run()
    return app


def result_copy(app: AppTest) -> str:
    return next(item.value for item in app.markdown if "constellation-result" in item.value)


def test_repeated_choices_reach_a_named_culmination() -> None:
    app = complete_path(launch_app(), ["Glow"] * 6)

    assert not app.exception
    assert app.caption[-1].value == "Stars placed: 6 / 6"
    assert "The Steadfast Lantern" in result_copy(app)
    assert app.button(key="reset_stars").label == "Try another sky"


def test_different_paths_produce_different_valid_results() -> None:
    glow_app = complete_path(launch_app(), ["Glow"] * 6)
    drift_app = complete_path(launch_app(), ["Drift"] * 6)

    assert "The Steadfast Lantern" in result_copy(glow_app)
    assert "The Patient Tide" in result_copy(drift_app)
    assert result_copy(glow_app) != result_copy(drift_app)


def test_archive_preserves_original_demonstration() -> None:
    app = navigate(launch_app(), "Archive")

    assert not app.exception
    archive_copy = " ".join(item.value for item in app.markdown)
    assert NEW_FOLLY in archive_copy
    assert RAIN_FOLLY in archive_copy


def test_random_selects_a_registered_folly() -> None:
    app = navigate(launch_app(), "Random")
    before = app.subheader[0].value

    app.button(key="random_folly").click().run()

    assert not app.exception
    assert app.subheader[0].value in {NEW_FOLLY, RAIN_FOLLY}
    assert app.subheader[0].value != before


def test_about_is_available() -> None:
    app = navigate(launch_app(), "About")

    assert not app.exception
    assert any(header.value == "About" for header in app.header)
    assert "no practical purpose" in " ".join(item.value for item in app.markdown)
