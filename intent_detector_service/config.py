import os
from typing import Final, Literal

ALLOW_ORIGINS: Final[str] = os.environ.get("ALLOW_ORIGINS", ".*")
ENGLISH_SPACY_MODEL: Final[str] = os.environ.get("SPACY_MODEL", "en_core_web_lg")
SPANISH_SPACY_MODEL: Final[str] = os.environ.get("SPACY_MODEL", "es_core_news_lg")

ALLOWED_LANGUAGES: Final[list[str]] = ["english", "spanish"]
ALLOWED_LANGUAGE_TYPES = Literal["english", "spanish"]  # alias type
