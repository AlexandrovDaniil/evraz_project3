from evraz.classic.components import component
from evraz.classic.http_auth import authenticate, authenticator_needed
from user.application import services

from .auth import generate_token
from .join_points import join_point


@authenticator_needed
@component
class Users:
    users: services.Users

    @join_point
    @authenticate
    def on_get_show_info(self, request, response):
        request.params['user_id'] = request.context.client.user_id
        user = self.users.get_info(**request.params)
        response.media = {
            'user id': user.id,
            'user name': user.name,
            'user login': user.login
        }

    @join_point
    def on_post_add_user(self, request, response):
        user = self.users.add_user(**request.media)
        token = generate_token(user)
        response.media = token

    @join_point
    def on_post_user_login(self, request, response):
        user = self.users.login_user(**request.media)
        token = generate_token(user)
        response.media = token

    @join_point
    @authenticate
    def on_get_show_all(self, request, response):
        users = self.users.get_all()
        response.media = [
            {
                'id': user.id,
                'name': user.name,
                'login': user.login
            } for user in users
        ]
