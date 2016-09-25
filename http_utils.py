from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def get_html(url):
    try:
        html = urlopen(url).read()
    except HTTPError as e:
        if e.code == 400:
            print('ERROR: ' + 'BAD REQUEST: ' + url)
        if e.code == 401:
            print('ERROR: ' + 'UNAUTHORIZED: ' + url)
        if e.code == 403:
            print('ERROR: ' + 'FORBIDDEN: ' + url)
        if e.code == 404:
            print('ERROR: ' + 'NOT FOUND: ' + url)
        if e.code == 500:
            print('ERROR: ' + 'INTERNAL SERVER ERROR: ' + url)
    except URLError as e:
        print('ERROR: ' + 'INCORRECT URL: ' + url)