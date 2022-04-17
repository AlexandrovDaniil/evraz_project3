import click


def create_cli(MessageBus):

    @click.group()
    def cli():
        pass

    @cli.command()
    def consumer():
        MessageBus.declare_scheme()
        MessageBus.consumer.run()

    return cli
