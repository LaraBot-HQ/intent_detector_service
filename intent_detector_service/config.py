import os
from typing import Final, Literal, Optional

ALLOW_ORIGINS: Final[str] = os.environ.get("ALLOW_ORIGINS", ".*")
ENGLISH_SPACY_MODEL: Final[str] = os.environ.get("SPACY_MODEL", "en_core_web_lg")
SPANISH_SPACY_MODEL: Final[str] = os.environ.get("SPACY_MODEL", "es_core_news_lg")

ALLOWED_LANGUAGES: Final[list[str]] = ["english", "spanish"]
ALLOWED_LANGUAGE_TYPES = Literal["english", "spanish"]  # alias type


# luis.ai config

AUTHORING_KEY = os.environ.get("AUTHORING_KEY")
AUTHORING_ENDPOINT = os.environ.get("AUTHORING_ENDPOINT", "https://westus.api.cognitive.microsoft.com")

LUIS_LANGUAGE_APPS: dict[ALLOWED_LANGUAGE_TYPES, Optional[str]] = {
    "english": os.environ.get("EN_PREDICTION_KEY"),
    "spanish": os.environ.get("ES_PREDICTION_KEY")
}
