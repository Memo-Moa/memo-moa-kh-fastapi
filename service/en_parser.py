import threading
from typing import List, ClassVar, Optional
import spacy


NOUN_POS = {"NOUN", "PROPN", "PRON"}
ADV_POS = {"ADV"}
AUX_POS = {"AUX"}
VERB_POS = {"VERB"}
ADJ_POS = {"ADJ"}


class SpacyInstance:
    _instance: ClassVar[Optional["SpacyInstance"]] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    nlp: spacy.Language

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance.nlp = spacy.load("en_core_web_sm")
                    cls._instance = instance
        return cls._instance


def english_parser(texts: List[str]):
    nlp = SpacyInstance().nlp
    result = dict(nouns=[], adverbs=[], verbs=[], adjectives=[])

    for doc in nlp.pipe(texts):
        for token in doc:
            if token.is_punct or token.is_space:
                continue
            if token.pos_ == "PRON":
                result["nouns"].append(token.lemma_)
                continue
            if token.pos_ in VERB_POS or token.pos_ in AUX_POS:
                result["verbs"].append(token.lemma_)
                continue
            if token.is_stop:
                continue
            if token.pos_ in NOUN_POS:
                result["nouns"].append(token.lemma_)
            elif token.pos_ in ADV_POS:
                result["adverbs"].append(token.lemma_)
            elif token.pos_ in ADJ_POS:
                result["adjectives"].append(token.lemma_)

    return result
