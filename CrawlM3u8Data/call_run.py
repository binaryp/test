import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from CrawlM3u8Data.spiders.main import MainSpider

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python crawl_runner.py <url> <save_mp4_path>")
        sys.exit(1)

    url = sys.argv[1]
    save_mp4_path = sys.argv[2]

    # 创建爬虫进程
    process = CrawlerProcess(get_project_settings())  # 加载项目的 Scrapy 配置

    # 通过传递参数启动爬虫
    process.crawl(MainSpider, url=url, save_mp4_path=save_mp4_path)

    # 开始运行爬虫
    process.start()
