from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from CrawlM3u8Data.spiders.main import MainSpider

if __name__ == "__main__":
    url = input("采集网址: ")
    save_mp4_path = input("保存目录: ")

    # 创建爬虫进程
    process = CrawlerProcess(get_project_settings())  # 加载项目的 Scrapy 配置

    # 通过传递参数启动爬虫
    process.crawl(MainSpider, url=url, save_mp4_path=save_mp4_path)

    # 开始运行爬虫
    process.start()
