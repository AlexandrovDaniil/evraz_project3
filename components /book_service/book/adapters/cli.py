import click
import requests


@click.command()
@click.option('--tags', help='tags for books', multiple=True)
def get_books_isbn13(tags):
    res = []
    for tag in tags:
        r = requests.get(f'https://api.itbook.store/1.0/search/{tag}')
        if int(r.json()['total']) < 50:
            page_count = (int(r.json()['total']) // 10) + 1
            for i in range(1, page_count + 1):
                r = requests.get(f'https://api.itbook.store/1.0/search/{tag}/{i}')
                for j in r.json()['books']:
                    res.append(j['title'])
        else:
            page_count = 5
            for i in range(1, page_count + 1):
                r = requests.get(f'https://api.itbook.store/1.0/search/{tag}/{i}')
                for j in r.json()['books']:
                    res.append(j['title'])

    for i, j in enumerate(res):
        print(i, j)


if __name__ == '__main__':
    get_books_isbn13()
