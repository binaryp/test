import scrapy
from ..items import Crawlm3U8DataItem
from urllib.parse import urljoin


class MainSpider(scrapy.Spider):
    name = "main"

    def __init__(self, url, save_mp4_path, *args, **kwargs):
        """
        初始化数据
        :param url: 采集的 url
        :param save_mp4_path: 采集后存放的 url
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

        # 收集信息
        self.url = url
        self.save_mp4_path = save_mp4_path

        # 自定义固定参数
        self.home_url = self.url.split('playlist_eof')[0]

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        for i in response.text.split('\n'):
            if '#' not in i and i:
                yield Crawlm3U8DataItem(url=urljoin(self.home_url, i))
