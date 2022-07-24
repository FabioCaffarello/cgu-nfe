FROM python:3.8

ENV  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_HOME="/home/poetry" \
  VENV_PATH="/home/bot .venv" \
  BOT_HOME="/home/bot" \
  SCRAPY_HOME="/home/bot/cgu_nfe"

ENV  PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN pip3 install poetry==1.2.0a2
WORKDIR $BOT_HOME

COPY ./cgu_nfe ./cgu_nfe
COPY ./.env .
COPY ./pyproject.toml .
COPY ./poetry.toml .

WORKDIR $SCRAPY_HOME

RUN poetry install

EXPOSE 8888

ENTRYPOINT ["poetry", "run", "scrapy", "crawl", "cgu_nfe"]
