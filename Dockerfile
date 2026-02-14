FROM ghcr.io/astral-sh/uv:python3.14-alpine

WORKDIR /server
COPY ./main.py /server/
COPY ./pyproject.toml /server/
COPY ./uv.lock /server/

RUN uv sync

ENTRYPOINT ["uv", "run", "./main.py"]