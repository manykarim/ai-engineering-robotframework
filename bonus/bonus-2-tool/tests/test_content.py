from pathlib import Path

import pytest

from robotframework_github_reporter import content

ACTIONS = {
    "GITHUB_ACTIONS": "true",
    "GITHUB_SERVER_URL": "https://github.com",
    "GITHUB_REPOSITORY": "octo-org/app",
    "GITHUB_RUN_ID": "42",
}


def test_title():
    assert content.title("Suite.Sub Suite.Test Name") == "Failing test: Suite.Sub Suite.Test Name"


def test_run_url_in_github_actions():
    assert content.run_url(ACTIONS) == "https://github.com/octo-org/app/actions/runs/42"


def test_run_url_outside_github_actions():
    assert content.run_url({}) is None
    assert content.run_url({**ACTIONS, "GITHUB_ACTIONS": "false"}) is None


@pytest.mark.parametrize("name", ["GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"])
def test_run_url_needs_every_variable(name):
    missing = {key: value for key, value in ACTIONS.items() if key != name}
    assert content.run_url(missing) is None
    assert content.run_url({**ACTIONS, name: ""}) is None


def test_location_relative_to_cwd(tmp_path):
    source = tmp_path / "atest" / "demo.robot"
    assert content.location(source, 12, cwd=tmp_path) == "atest/demo.robot:12"
    assert content.location(str(source), 12, cwd=tmp_path) == "atest/demo.robot:12"


def test_location_outside_cwd_is_unchanged(tmp_path):
    source = tmp_path / "elsewhere" / "demo.robot"
    cwd = tmp_path / "project"
    assert content.location(source, 3, cwd=cwd) == f"{source}:3"


def test_location_without_source_or_line(tmp_path):
    assert content.location(None, 12, cwd=tmp_path) == "unknown:12"
    assert content.location(None, None, cwd=tmp_path) == "unknown"
    assert content.location(tmp_path / "demo.robot", None, cwd=tmp_path) == "demo.robot"


def test_location_defaults_to_current_directory():
    assert content.location(Path.cwd() / "atest" / "demo.robot", 12) == "atest/demo.robot:12"


def test_body(tmp_path):
    text = content.body("Expected 200 but got 500", tmp_path / "atest/demo.robot", 12, None, cwd=tmp_path)
    assert text == (
        "**Failure message**\n"
        "\n"
        "```text\n"
        "Expected 200 but got 500\n"
        "```\n"
        "\n"
        "**Source:** `atest/demo.robot:12`\n"
    )


def test_body_with_run_url(tmp_path):
    url = "https://github.com/octo-org/app/actions/runs/42"
    text = content.body("Boom", tmp_path / "demo.robot", 1, url, cwd=tmp_path)
    assert text.endswith(f"**Source:** `demo.robot:1`\n**Run:** {url}\n")


def test_body_without_run_url_has_no_run_line(tmp_path):
    assert "**Run:**" not in content.body("Boom", tmp_path / "demo.robot", 1, None, cwd=tmp_path)


def test_multi_line_message_with_backticks_stays_in_one_fence(tmp_path):
    message = "First line\n```\nnot a fence\n````\n**still the message**"
    text = content.body(message, tmp_path / "demo.robot", 1, None, cwd=tmp_path)
    # The longest run in the message is four backticks, so the fence has five.
    assert text.split("`````") == [
        "**Failure message**\n\n",
        f"text\n{message}\n",
        "\n\n**Source:** `demo.robot:1`\n",
    ]


def test_comment_starts_with_failed_again(tmp_path):
    source = tmp_path / "demo.robot"
    text = content.comment("Boom", source, 1, None, cwd=tmp_path)
    assert text == "Failed again.\n\n" + content.body("Boom", source, 1, None, cwd=tmp_path)
