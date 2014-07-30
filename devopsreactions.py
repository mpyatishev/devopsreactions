import asyncio
import aiohttp
import concurrent

from lxml.html import fromstring
from urllib.request import urlopen

loop = asyncio.get_event_loop()


def get_urls():
    content = urlopen('http://devopsreactions.tumblr.com/').read()
    html = fromstring(content)

    data = {}
    for e in html.find_class('item_content'):
        titles = e.find_class('post_title')
        if titles:
            name = titles[0].text_content()
            image = e.find('p').find('img')
            if image is not None:
                data[name] = image.attrib['src']

    return data


# 0.596u 0.496s 0:38.09 2.8%      0+0k 1128+50104io 11pf+0w
def load_images(data):
    for (name, url) in data.items():
        with open(name + '.gif', 'wb') as f:
            f.write(urlopen(url).read())


#
def load_images_asyncio(data):
    for (name, url) in data.items():
        response = yield from aiohttp.request('GET', url)
        img = yield from response.read()
        with open(name + '.gif', 'wb') as f:
            f.write(img)


def load_url(url):
    response = urlopen(url)
    return response.read()


# 0.632u 0.528s 0:24.14 4.7%      0+0k 0+50104io 0pf+0w
def load_images_threadpool(data):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(load_url, url): name
                         for (name, url) in data.items()}
        for future in concurrent.futures.as_completed(future_to_url):
            name = future_to_url[future]
            try:
                img = future.result()
            except Exception as e:
                print(e)
            else:
                with open(name + '.gif', 'wb') as f:
                    f.write(img)


# 0.616u 0.636s 0:27.95 4.4%      0+0k 472+50104io 3pf+0w
def load_images_processpool(data):
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(load_url, url): name
                         for (name, url) in data.items()}
        for future in concurrent.futures.as_completed(future_to_url):
            name = future_to_url[future]
            try:
                img = future.result()
            except Exception as e:
                print(e)
            else:
                with open(name + '.gif', 'wb') as f:
                    f.write(img)


if __name__ == '__main__':
    data = get_urls()
    # load_images(data)


    # loop.run_until_complete(load_images_asyncio(data))

    # load_images_threadpool(data)

    load_images_processpool(data)
