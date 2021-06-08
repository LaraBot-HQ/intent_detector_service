from operator import itemgetter
from typing import TypedDict, Final

import spacy
from spacy import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from intent_detector_service.config import SPANISH_SPACY_MODEL, ENGLISH_SPACY_MODEL, ALLOWED_LANGUAGE_TYPES
from intent_detector_service.services.base_intent_detector import (
    IntentEngineDetector, IntentDictionary, SimilarityObject, ExtractedEntityDict
)
from intent_detector_service.type_models.request.intent_detection import ActionObject, PatternMatcherObject

en_nlp: Language = spacy.load(ENGLISH_SPACY_MODEL)
es_nlp: Language = spacy.load(SPANISH_SPACY_MODEL)

for nlp in [en_nlp, es_nlp]:
    nlp.Defaults.stop_words.add("larabot")
    nlp.Defaults.stop_words.add("LARABOT")


class SpacyLanguageDictInstances(TypedDict):
    english: Language
    spanish: Language


LANGUAGE_DICT_INSTANCE: Final[SpacyLanguageDictInstances] = {
    "english": en_nlp,
    "spanish": es_nlp,
}


class LocalEngineDetector(IntentEngineDetector):
    """
    This is the intent detector for local working using spacy and NLTK
    """

    nlp: Language
    NAME = "local"

    def __init__(self, lang: ALLOWED_LANGUAGE_TYPES):
        self.LANG = lang
        super().__init__(lang)

        self.nlp = LANGUAGE_DICT_INSTANCE[self.LANG]

    def process_text(self, text: str) -> str:
        doc = self.nlp(text.strip().lower())
        result = []
        for token in doc:
            if token.text in self.nlp.Defaults.stop_words:
                continue
            if token.is_punct:
                continue
            if token.lemma_ == '-PRON-':
                continue
            result.append(token.lemma_)

        return " ".join(result)

    def detect_intention(
        self, user_message: str, actions: list[ActionObject]
    ) -> IntentDictionary:
        user_message = self.process_text(user_message)
        similarity_list: list[SimilarityObject] = []
        message_doc = self.nlp(user_message)

        for i, action_object in enumerate(actions):
            action = action_object.action
            sentence_1 = self.nlp(self.process_text(action))
            similarity_object = SimilarityObject(action_object, action, sentence_1.similarity(message_doc), i)
            similarity_list.append(similarity_object)

        sorted_list = sorted(similarity_list, key=itemgetter(2), reverse=True)

        intent = sorted_list[0]

        # Named entity recognition (NER)
        entities = self.extract_entities(message_doc, intent.action_object.matchers)

        return {
            "intent_id": intent.action_object.intent_id,
            "action": intent.action,
            "entities": entities,
            "similarity": intent.similarity,
            "message": user_message
        }

    def __extract_auto_entities_recognizer(self, message_doc: Doc) -> list[ExtractedEntityDict]:
        return [{"type": e.label_, "value": e.text} for e in message_doc.ents]

    def __extract_with_match_pattern(
            self, message_doc: Doc, pattern_matchers: list[PatternMatcherObject]
    ) -> list[ExtractedEntityDict]:
        matcher = Matcher(nlp.vocab)
        # Add match ID "HelloWorld" with no callback and one pattern
        for pattern_matcher in pattern_matchers:
            matcher.add(pattern_matcher.id, pattern_matcher.patterns)

        matches = matcher(message_doc)
        extracted_entities: list[ExtractedEntityDict] = []
        for match_id, start, end in matches:
            # string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = message_doc[start:end]  # The matched span
            extracted_entities.append({
                "type": match_id, "value": span.text
            })

        return extracted_entities

    def extract_entities(
        self, message_doc: Doc, pattern_matchers: list[PatternMatcherObject] = None, *_, **__
    ) -> list[ExtractedEntityDict]:
        if pattern_matchers:
            return self.__extract_with_match_pattern(message_doc, pattern_matchers)
        else:
            return self.__extract_auto_entities_recognizer(message_doc)
