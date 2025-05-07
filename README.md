# fastapi_quizbot

Quizbot(feat. FastAPI)

## commands

### FastAPI

- run dev server

```bat
uv run fastapi dev src/main.py
```

### ngrok

```bat
ngrok http 8000 --region ap
```

### test

- set test environment

```bat
set APP_ENV=test
```

- run pytest

```bat
pytest
```

### docker

- build docker image with Dockerfile

```bat
docker build -t quizbot .
```
