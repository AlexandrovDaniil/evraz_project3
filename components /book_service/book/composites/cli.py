from book.adapters.cli import create_cli
from book.composites.book_api import MessageBus
from book.composites.book_api import MessageBusCons

cli = create_cli(MessageBus.publisher, MessageBusCons)
