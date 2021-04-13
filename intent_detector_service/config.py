import os
from typing import Final

ALLOW_ORIGINS: Final[str] = os.environ.get("ALLOW_ORIGINS", ".*")
SPACY_MODEL: Final[str] = os.environ.get("SPACY_MODEL", "es_core_news_lg")
