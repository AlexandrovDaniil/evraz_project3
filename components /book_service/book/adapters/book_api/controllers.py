from book.application import services
from classic.components import component
from classic.http_auth import authenticate, authenticator_needed
from .join_points import join_point


@authenticator_needed
@component
class Books:
    books: services.Books

    @join_point
    @authenticate
    def on_get_show_info(self, request, response):
        book = self.books.get_info(**request.params)
        response.media = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published year': book.published_year,
        }

    @join_point
    @authenticate
    def on_post_add_book(self, request, response):
        self.books.add_book(**request.media)
        response.media = {'status': 'book added'}

    @join_point
    @authenticate
    def on_get_show_all(self, request, response):
        books = self.books.get_all()
        response.media = [{
            'book id': book.id,
            'author': book.author,
            'published year': book.published_year,
            'title': book.title
        } for book in books]

    @join_point
    @authenticate
    def on_get_delete_book(self, request, response):
        self.books.delete_book(**request.params)
        response.media = {'status': 'book deleted'}

    @join_point
    @authenticate
    def on_post_take_book(self, request, response):
        request.media['user_id'] = request.context.client.user_id
        self.books.take_book(**request.media)
        response.media = {'status': 'ok'}

    @join_point
    @authenticate
    def on_post_return_book(self, request, response):
        request.media['user_id'] = request.context.client.user_id
        self.books.return_book(**request.media)
        response.media = {'status': 'ok'}
