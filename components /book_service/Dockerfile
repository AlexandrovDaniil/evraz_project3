FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./setup.cfg .
COPY ./setup.py .
RUN pip install --upgrade -e '.[dev]'
COPY . .

COPY ./dist .

COPY . ./book
RUN pip install *.tar.gz
COPY . .

COPY ./entrypoint_*.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint_*.sh
