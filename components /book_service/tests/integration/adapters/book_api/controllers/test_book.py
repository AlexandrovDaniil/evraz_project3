import json
from datetime import datetime


def test__on_get_show_info(client, books_service):
    expected = {
        "book id": 9781491954461,
        "tag": "mongo",
        "title": "MongoDB: The Definitive Guide, 3rd Edition",
        "subtitle": "Powerful and Scalable Data Storage",
        "authors": "Shannon Bradshaw, Kristina Chodorow",
        "pages": 514,
        "price": 29.0,
        "publisher": "O'Reilly Media",
        "description": "Manage your data with a system",
        "published year": 2019,
        "booking time": None,
    }
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_get('/api/books/show_info', headers=header, params={'book_id': 9781491954461})

    assert result.status_code == 200
    assert result.json == expected


def test__on_get_show_all(client, books_service):
    expected = [{
        "book id": 9781491954461,
        "tag": "mongo",
        "title": "MongoDB: The Definitive Guide, 3rd Edition",
        "subtitle": "Powerful and Scalable Data Storage",
        "authors": "Shannon Bradshaw, Kristina Chodorow",
        "pages": 514,
        "price": 29.0,
        "publisher": "O'Reilly Media",
        "description": "Manage your data with a system",
        "published year": 2019,
        "booking time": None,
    }]
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_get('/api/books/show_all', headers=header)

    assert result.status_code == 200
    assert result.json == expected


def test__on_get_filter(client, books_service):
    expected = [{
        "book id": 9781491954461,
        "tag": "mongo",
        "title": "MongoDB: The Definitive Guide, 3rd Edition",
        "subtitle": "Powerful and Scalable Data Storage",
        "authors": "Shannon Bradshaw, Kristina Chodorow",
        "pages": 514,
        "price": 29.0,
        "publisher": "O'Reilly Media",
        "description": "Manage your data with a system",
        "published year": 2019,
        "booking time": None,
    }]
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_get('/api/books/filter', headers=header, params={'keyword': 'MongoDB'})

    assert result.status_code == 200
    assert result.json == expected


def test__on_post_take_book(client, books_service):
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_post('/api/books/take_book', headers=header, body=json.dumps({'book_id': 9781491954461}))
    assert result.status_code == 200


def test__on_post_return_book(client, books_service):
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_post('/api/books/return_book', headers=header, body=json.dumps({'book_id': 9781491954461}))
    assert result.status_code == 200


def test__on_get_show_history(client, books_service):
    expected = [{
        'book id': 9781491954463,
        'user id': 1,
        'action': 'take book',
        'booking time': datetime(2022, 4, 15, 20, 20, 20).strftime('%Y-%m-%d %H:%M:%S'),
        'id': 1
    }]
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}

    result = client.simulate_get('/api/books/show_history', headers=header)

    assert result.status_code == 200
    assert result.json == expected


def test__on_post_buy_book(client, books_service):
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}

    result = client.simulate_post('/api/books/buy_book', headers=header, body=json.dumps({'book_id': 9781491954461}))
    assert result.status_code == 200


def test__on_get_active_book(client, books_service):
    expected = {
        "book id": 9781491954461,
        "tag": "mongo",
        "title": "MongoDB: The Definitive Guide, 3rd Edition",
        "subtitle": "Powerful and Scalable Data Storage",
        "authors": "Shannon Bradshaw, Kristina Chodorow",
        "pages": 514,
        "price": 29.0,
        "publisher": "O'Reilly Media",
        "description": "Manage your data with a system",
        "published year": 2019,
        "booking time": None,
    }
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_get('/api/books/active_book', headers=header)

    assert result.status_code == 200
    assert result.json == expected
