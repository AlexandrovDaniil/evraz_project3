import time

import click
import requests
from classic.messaging import Message


def create_cli(publisher, MessageBusCons):
    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1)
    def get_books(tags):
        books_ids = []
        new_book_list = []
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
            new_book_list.append(book)
            publisher.publish(Message('TestApiExchange', {'book': book}))
        if new_book_list:
            get_top_3(new_book_list)

    def get_top_3(book_list: list):
        top_list = sorted(book_list, key=lambda x: (x['rating'], -int(x['year'])), reverse=True)[:3]
        for i in top_list:
            print(i['title'], i['rating'], i['year'])
        send_top_3(top_list)

    def send_top_3(top_list: list):
        ...

    @cli.command()
    def consumer():
        MessageBusCons.declare_scheme()
        MessageBusCons.consumer.run()

    return cli
# book_service get-books 'azure'
# book_service get-books 'actionscript'
