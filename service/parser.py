import re
from typing import List
from service.kiwi_parser import parser as ko_parser
from service.en_parser import english_parser as en_parser


def _split_ko_en(text: str) -> tuple[str, str]:
    ko_parts = re.findall(
        r"[\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uAC00-\uD7AF\uD7B0-\uD7FF\uFFA0-\uFFBF]+",
        text,
    )
    en_parts = re.findall(r"[a-zA-Z]+(?:[\'-][a-zA-Z]+)*", text)
    ko_text = " ".join(ko_parts)
    en_text = " ".join(en_parts)
    return ko_text, en_text


def _merge_result(ko_result, en_result):
    return {
        "nouns": ko_result["nouns"] + en_result["nouns"],
        "adverbs": ko_result["adverbs"] + en_result["adverbs"],
        "verbs": ko_result["verbs"] + en_result["verbs"],
        "adjectives": ko_result["adjectives"] + en_result["adjectives"],
    }


def mixed_parser(texts: List[str]):
    results = []
    for text in texts:
        ko_text, en_text = _split_ko_en(text)
        ko_result = (
            ko_parser([ko_text])
            if ko_text
            else dict(nouns=[], adverbs=[], verbs=[], adjectives=[])
        )
        en_result = (
            en_parser([en_text])
            if en_text
            else dict(nouns=[], adverbs=[], verbs=[], adjectives=[])
        )
        results.append(_merge_result(ko_result, en_result))
    return results
