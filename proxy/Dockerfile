FROM python:3.8

ENV  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_HOME="/home/poetry" \
  VENV_PATH="/home/proxy .venv"

ENV  PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN pip3 install poetry==1.2.0a2
WORKDIR /home/proxy

COPY . /home/proxy
RUN poetry install --without dev

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "proxy"]
