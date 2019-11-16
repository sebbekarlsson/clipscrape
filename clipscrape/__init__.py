import requests
from bs4 import BeautifulSoup
import json


class Clipart(object):

    def __init__(self):
        self.base_url = 'https://etc.usf.edu/clipart/'
        self.session = requests.Session()

    def scrape(self, url=None):
        url = url or self.base_url

        document = BeautifulSoup(self.session.get(url).text, 'html.parser')

        return [
            self.scrape(u) if 'galleries' in u else
            self.handle_image(
                self.scrape_image_page(document.title.string, u)
            )
            for u in [
                a.get('href') for a in document.select('.span3.compendious a')
            ]
        ]

    def scrape_image_page(self, gallery_title, url):
        return (
            gallery_title,
            BeautifulSoup(self.session.get(url).text, 'html.parser')
            .select_one('img').get('src')
        )

    def handle_image(self, image):
        title, src = image

        print(json.dumps({
            'gallery': title,
            'image': src
        }, indent=4, sort_keys=True))
