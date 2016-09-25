from urllib.request import urlopen

def get_html(url_str):
    html = urlopen(url_str).read().decode('utf-8')
    print(html)