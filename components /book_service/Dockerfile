FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./setup.cfg .
COPY ./setup.py .
RUN pip install --upgrade -e '.[dev]'


COPY . .

CMD ["gunicorn","-b","0.0.0.0:1235", "book.composites.book_api:app", "--reload"]