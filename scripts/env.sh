#!/bin/bash

export EN_SPACY_MODEL='en_core_web_lg'
export ES_SPACY_MODEL='es_core_news_lg'
export AUTHORING_KEY='87a8292ac07c4e708842c839414b3be2'
export AUTHORING_ENDPOINT='https://westus.api.cognitive.microsoft.com'
export EN_PREDICTION_KEY='a8051846-301c-4324-a3c6-fd48837c71cd'
export ES_PREDICTION_KEY='775cfa5d-12ef-4a3d-82a6-78755bbbe06b'

exec "$@"