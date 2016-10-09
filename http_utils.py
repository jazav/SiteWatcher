from urllib.request import urlopen

def get_html(url):
    try:
        html = urlopen(url).read()
        return html
    except Exception as e:
        raise Exception(type(e).__name__ + ': ' + e.reason + ': ' + url)
