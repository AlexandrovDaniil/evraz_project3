import click

from evraz.classic.messaging import Message


def create_cli(publisher, MessageBusCons):
    ''' book_service get-tags azure
        book_service get-tags actionscript azure
        book_service get-tags mongo azure ios 1:08/0:10
        команды для добавления книг
    '''

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1)
    def get_tags(tags):
        publisher.publish(Message('ApiExchange', {'tags': tags}))

    @cli.command()
    def consumer():
        MessageBusCons.declare_scheme()
        MessageBusCons.consumer.run()

    return cli
