FROM python:3.9.2

RUN pip install poetry

WORKDIR /code

COPY pyproject.toml /code/

RUN poetry install
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY intent_detector_service/ /code/intent_detector_service

RUN poetry run python -m spacy download es_core_news_lg
RUN poetry run python -m spacy download en_core_web_lg

CMD ["poetry", "run", "uvicorn", "intent_detector_service.app:app", "--host", "0.0.0.0", "--port", "80"]