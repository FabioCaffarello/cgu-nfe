FROM python:3.8

ENV  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_HOME="/home/poetry" \
  VENV_PATH="/home/proxy .venv" \
  BOT_HOME="/home/bot"

ENV  PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN pip3 install poetry==1.2.0a2
WORKDIR $BOT_HOME

COPY ./cgu_nfe/cgu_nfe ./cgu_nfe
COPY ./cgu_nfe/scrapy.cfg .
COPY ./.env .
COPY ./pyproject.toml .
COPY ./poetry.toml .
COPY ./cgu_nfe/tests ./tests
COPY ./cgu_nfe/schemas ./schemas
RUN poetry install --without dev

EXPOSE 8888

ENTRYPOINT ["poetry", "run", "scrapy", "crawl", "cgu_nfe"]
