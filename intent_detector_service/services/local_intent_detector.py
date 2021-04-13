import spacy

from intent_detector_service.config import SPACY_MODEL

nlp = spacy.load(SPACY_MODEL)