import json


def test__on_get_show_info(client, users_service):
    expected = {
        'user id': 1,
        'user name': 'Vasya',
        'user login': 'test_login1',
    }
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_get('/api/users/show_info', headers=header)

    assert result.status_code == 200
    assert result.json == expected


def test__on_post_add_user(client, users_service):
    user_data = {
        'login': 'test_login1',
        'password': 'test_pass1',
        'name': 'Vasya'
    }
    expected = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
               'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'

    result = client.simulate_post('/api/users/add_user', body=json.dumps(user_data))

    assert result.status_code == 200
    assert result.json == expected


def test__on_post_user_login(client, users_service):
    user_data = {
        'login': 'test_login1',
        'password': 'test_pass1',
    }
    expected = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
               'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'

    result = client.simulate_post('/api/users/user_login', body=json.dumps(user_data))

    assert result.status_code == 200
    assert result.json == expected


def test__on_get_show_all(client, users_service):
    expected = [{'id': 1,
                 'login': 'test_login1',
                 'name': 'Vasya'}]
    header = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIjoidGVzdF9sb2dpbjEiLCJuYW1lIj' \
                         'oiVmFzeWEiLCJncm91cCI6IlVzZXIifQ.YykXhJt6OHOUVPNBq08H6wx9sSHlYtdzptp76nGLMu4'}
    result = client.simulate_get('/api/users/show_all', headers=header)

    assert result.status_code == 200
    assert result.json == expected
