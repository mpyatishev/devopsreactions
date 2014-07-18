import asyncio

from lxml.html import fromstring
from urllib import request


def get_urls():
    content = request.urlopen('http://devopsreactions.tumblr.com/').read()
    html = fromstring(content)

    data = {}
    for e in html.find_class('item_content'):
        titles = e.find_class('post_title')
        if titles:
            name = titles[0].text_content()
            image = e.find('p').find('img')
            if image:
                data[name] = image.attrib['src']

    return data


if __name__ == '__main__':
    load_images(get_urls())
