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

## Docker

### 로컬 빌드 및 실행

```bash
docker build -t memo-moa-kh-fastapi .
docker run -p 8000:8000 memo-moa-kh-fastapi
```

### docker-compose

```bash
docker compose up -d
```

### Portainer 배포

**방법 1 — Stack (권장)**

1. Portainer → **Stacks** → **Add stack**
2. **Repository** 탭 선택 후 GitHub 레포 URL 입력 (또는 `docker-compose.yml` 내용을 Web editor에 직접 붙여넣기)
3. **Deploy the stack** 클릭

**방법 2 — 이미지 빌드 후 배포**

```bash
# 로컬 또는 CI에서 이미지 빌드 후 레지스트리에 push
docker build -t <registry>/memo-moa-kh-fastapi:latest .
docker push <registry>/memo-moa-kh-fastapi:latest
```

이후 Portainer → **Containers** → **Add container** 에서 이미지 지정, 포트 `8000:8000` 매핑 후 배포합니다.

## 기술 스택

- **FastAPI** - 웹 프레임워크
- **Kiwi (kiwipiepy)** - 한국어 형태소 분석
- **spaCy (en_core_web_sm)** - 영어 형태소 분석
- **uvicorn** - ASGI 서버
