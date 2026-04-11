# mecab-server

한국어(Kiwi) 및 영어(spacy) 형태소 분석 API 서버

## 실행

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## API

### `POST /`

문장 목록을 받아 품사별로 분류된 형태소 분석 결과를 반환합니다.

**요청 본문** (JSON array of strings):

```json
["나는 밥을 먹는다", "I love programming"]
```

**응답** (JSON array):

```json
[
  {
    "nouns": ["밥"],
    "adverbs": [],
    "verbs": ["먹다"],
    "adjectives": []
  },
  {
    "nouns": ["programming"],
    "adverbs": [],
    "verbs": ["love"],
    "adjectives": []
  }
]
```

한국어와 영어가 혼합된 문장도 자동으로 분리하여 각각 분석 후 병합합니다.

## Rate Limiting

- UUID 기반: `x-user-id` 헤더당 윈도우 내 1회 요청
- IP 기반: IP당 윈도우 내 10회 요청
- 윈도우: 60초
- 제한 초과 시 `429 Too Many Requests` 응답, `Retry-After` 헤더 포함

## 기술 스택

- **FastAPI** - 웹 프레임워크
- **Kiwi (kiwipiepy)** - 한국어 형태소 분석
- **spaCy (en_core_web_sm)** - 영어 형태소 분석
- **uvicorn** - ASGI 서버