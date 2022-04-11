FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
#ENV PATH=$PATH:/usr/bin
COPY ./setup.cfg .
COPY ./setup.py .
RUN pip install --upgrade -e '.[dev]'
COPY . .

#RUN pip install click
#RUN pip install requests

COPY ./dist .
#COPY ./entrypoint_cons.sh .
#COPY ./entrypoint_service.sh .
#COPY ./book/adapters/cli.py .

#COPY ./book/composites ./
COPY . ./book
#RUN python cli.py 'ActionScript'
#RUN pip install *.tar.gz
COPY . .

COPY ./entrypoint_*.sh /usr/bin/

RUN chmod +x /usr/bin/entrypoint_*.sh
#CMD["python", "cli.py", "--tags='Mongo'", "--tags='ActionScript'"]

#CMD ["gunicorn","-b","0.0.0.0:1235", "book.composites.book_api:app", "--reload"]