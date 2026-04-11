import threading
from typing import List, ClassVar, Optional
from kiwipiepy import Kiwi


NOUN_TAGS = {"NNG", "NNP", "NNB", "NR", "NP"}
ADV_TAGS = {"MAG", "MAJ"}
VERB_TAGS = {"VV", "VX", "VCP", "VCN"}
ADJ_TAGS = {"VA"}


class KiwiInstance:
    _instance: ClassVar[Optional["KiwiInstance"]] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    kiwi: Kiwi

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance.kiwi = Kiwi()
                    cls._instance = instance
        return cls._instance


def parser(texts: List[str]):
    kiwi: Kiwi = KiwiInstance().kiwi
    parsed = kiwi.analyze(texts)

    result = dict(nouns=[], adverbs=[], verbs=[], adjectives=[])

    for data in parsed:
        # data[0][0]은 가장 확률이 높은 분석 결과(tokens)입니다.
        tokens = data[0][0]
        i = 0
        while i < len(tokens):
            word = tokens[i]

            # 1. [명사 + 동사/형용사] 결합 처리
            # 예: '철(NNG) + 들(VV) + 다', '애(NNG) + 들(VV) + 다'
            if word.tag in NOUN_TAGS and i + 1 < len(tokens):
                next_word = tokens[i + 1]
                if next_word.tag in VERB_TAGS or next_word.tag in ADJ_TAGS:
                    # 두 단어를 합치고 '다'를 붙여 기본형 생성
                    combined_form = word.form + next_word.form + "다"

                    if next_word.tag in VERB_TAGS:
                        result["verbs"].append(combined_form)
                    else:
                        result["adjectives"].append(combined_form)

                    i += 2  # 두 개를 합쳤으므로 인덱스 2칸 이동
                    continue

            # 2. 개별 단어 처리 (결합되지 않은 경우)
            if word.tag in NOUN_TAGS:
                result["nouns"].append(word.form)
            elif word.tag in ADV_TAGS:
                result["adverbs"].append(word.form)
            elif word.tag in VERB_TAGS:
                base = getattr(word, "lemma", None) or (word.form + "다")
                result["verbs"].append(base)
            elif word.tag in ADJ_TAGS:
                base = getattr(word, "lemma", None) or (word.form + "다")
                result["adjectives"].append(base)

            i += 1

    return result
