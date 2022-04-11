from threading import Thread
from typing import Optional
# from book.composites.book_api import MessageBus
import click
import requests
from classic.messaging import Message, Publisher


def create_cli(publisher, MessageBusCons):
    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1)
    def get_books(tags):
        books_ids = []
        for tag in tags:
            r = requests.get(f'https://api.itbook.store/1.0/search/{tag}').json()
            page_count = (int(r['total']) // 10) + (1 if int(r['total']) % 10 != 0 else 0)
            page_count = page_count if page_count < 5 else 5
            for i in range(1, page_count + 1):
                book_page = requests.get(f'https://api.itbook.store/1.0/search/{tag}/{i}').json()
                for book in book_page['books']:
                    books_ids.append(book['isbn13'])
        for book_id in books_ids:
            book = requests.get(f'https://api.itbook.store/1.0/books/{book_id}').json()
            publisher.publish(Message('TestApiExchange', {'book': book}))

    @cli.command()
    def consumer():
        MessageBusCons.declare_scheme()
        MessageBusCons.consumer.run()
        # consumer = Thread(target=MessageBusCons.consumer.run, daemon=True)
        # consumer.start()

    return cli
# book_service get-books 'azure'
