
from backend.app.config import settings


def test_settings_load():
    assert settings.groq_api_key is not None
    assert settings.github_token is not None
