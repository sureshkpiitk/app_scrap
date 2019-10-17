import tempfile
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from top_app.models import App, Video, ScreenShot


def scrape_all():
    res = requests.get('https://play.google.com/store/apps/collection/topselling_free')
    soup = BeautifulSoup(res.text, 'html.parser')
    a = soup.find_all('div', attrs={'class': 'ImZGtf mpg5gc'})
    top_apps = set(App.objects.filter(is_top=True))
    for k in a:
        parsed = urlparse(k.find('a').get('href'))
        if parsed:
            package_name = parse_qs(parsed.query)['id'][0]
            try:
                app = App.objects.get(package_name=package_name)
            except App.DoesNotExist:
                app = App.objects.create(package_name=package_name)
                app.get_remote_image(k.find('img').get('data-src'))
                app.developer = k.find('a', attrs={'class': 'mnKHRc'}).string
                app.name = k.find('div', attrs={'class': "WsMG1c nnK0zc"}).string
                print(k.find('img').get('data-src'),
                      k.find('div', attrs={'class': "WsMG1c nnK0zc"}).string,
                      k.find('div', attrs={'class': 'KoLSrc'}).string
                      )
            app.is_top = True
            app.save()
            if app in top_apps:
                top_apps.remove(app)

    for app in top_apps:
        app.is_top = False
        app.save()


def scrape_one(package_name):
    app = App.objects.get(package_name=package_name)
    res = requests.get(f'https://play.google.com/store/apps/details?id={package_name}')
    soup = BeautifulSoup(res.text, 'html.parser')

    tags = soup.find_all('button', attrs={'class': 'Q4vdJd'})

    for tag in tags:
        screen_shot = None
        if tag.find('img').get('data-src'):
            screen_shot = tag.find('img').get('data-src')
        elif tag.find('img').get('src'):
            screen_shot = tag.find('img').get('src')
        if screen_shot:
            try:
                ScreenShot.objects.get(app=app, url=screen_shot)
            except ScreenShot.DoesNotExist:
                ScreenShot.objects.create(app=app, url=screen_shot)

    # video
    video_tag = soup.find('div', attrs={'class': "MSLVtf Q4vdJd"})
    if video_tag:
        if video_tag.find('img').get('src') and video_tag.find('button').get('data-trailer-url'):
            try:
                Video.objects.get(app=app,
                                  url=video_tag.find('button').get('data-trailer-url'),
                                  thumbnail=video_tag.find('img').get('src')
                                  )
            except Video.DoesNotExist:
                Video.objects.create(app=app,
                                     url=video_tag.find('button').get('data-trailer-url'),
                                     thumbnail=video_tag.find('img').get('src')
                                     )
    return app
