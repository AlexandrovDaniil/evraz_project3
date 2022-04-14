from user.adapters.cli import create_cli
from user.composites.user_api import MessageBus


cli = create_cli(MessageBus)
