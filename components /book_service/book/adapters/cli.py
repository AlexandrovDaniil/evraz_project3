import click
from classic.messaging import Message


def create_cli(publisher, MessageBusCons):
    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1)
    def get_books(tags):
        publisher.publish(Message('ApiExchange', {'tags': tags}))

    @cli.command()
    def consumer():
        MessageBusCons.declare_scheme()
        MessageBusCons.consumer.run()

    return cli
# book_service get-books azure
# book_service get-books actionscript azure
# book_service get-books mongo azure ios 1:08/0:10
