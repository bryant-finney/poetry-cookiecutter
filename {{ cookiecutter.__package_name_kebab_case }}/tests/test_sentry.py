"""Test Sentry configuration."""
from __future__ import annotations

# stdlib
from unittest.mock import MagicMock

# third party
import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture

from {{ cookiecutter.__package_name_snake_case }}.sentry import configure_sentry

@pytest.fixture
def mocked_sentry_init(mocker: MockerFixture) -> MagicMock:
    """Patch the :func:`sentry_sdk.init()` with a :class:`MagicMock`."""
    mocked: MagicMock = mocker.patch("{{ cookiecutter.__package_name_snake_case }}.sentry.sentry_sdk.init")
    return mocked


@pytest.fixture
def monkeypatched_env(monkeypatch: MonkeyPatch, worker_id: str) -> dict[str, str]:
    """Match the environment variables to define ``SENTRY_DSN`` and ``ENVIRONMENT``."""
    env = {
        "SENTRY_DSN": f"{worker_id}:monkeypatched_env",
        "ENVIRONMENT": f"{worker_id}:monkeypatched_env",
    }
    monkeypatch.setenv("SENTRY_DSN", env["SENTRY_DSN"])
    monkeypatch.setenv("ENVIRONMENT", env["ENVIRONMENT"])

    return env


def test_configure_sentry(mocked_sentry_init: MagicMock, monkeypatched_env: dict[str, str]) -> None:
    """Test that Sentry can be configured."""
    configure_sentry()
    assert mocked_sentry_init.call_count == 1

    assert "traces_sample_rate" in mocked_sentry_init.call_args.kwargs
    assert "release" in mocked_sentry_init.call_args.kwargs
    assert mocked_sentry_init.call_args.kwargs["dsn"] == monkeypatched_env["SENTRY_DSN"]
    assert mocked_sentry_init.call_args.kwargs["environment"] == monkeypatched_env["ENVIRONMENT"]
