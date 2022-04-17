from typing import List, Optional

from evraz.classic.components import component
from user.application import dataclasses, interfaces


@component
class MailSender(interfaces.MailSender):

    def send(self, users: List[dataclasses.User], data: dict):
        if users:
            for user in users:
                print(f'Dear {user.name}, we have something to you!')
                print(f'Here is our new books compilation:')
                for tag in data:
                    print(f'For tag {tag}:')
                    for book in data[tag]:
                        print(
                            f'\t{book["title"]}, rating: {book["rating"]}, publish year: {book["year"]}'
                        )
