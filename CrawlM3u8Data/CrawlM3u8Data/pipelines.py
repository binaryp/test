import scrapy
import os
import subprocess
import shutil
from scrapy.pipelines.files import FilesPipeline


class Crawlm3U8DataPipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.home_path = None
        self.ts_path = None

    def open_spider(self, spider):
        super().open_spider(spider)
        self.home_path = spider.settings.get('FILES_STORE')
        self.ts_path = os.path.join(self.home_path, 'ts')

    def get_media_requests(self, item, info):
        ts_name = item['url'].split("?")[0].split("/")[-1]
        return scrapy.Request(
            url=item['url'],
            meta={'file_name': ts_name}
        )

    def file_path(self, request, response=None, info=None, *, item=None):
        return os.path.join(self.ts_path, request.meta['file_name'])

    def close_spider(self, spider):
        """
        按照文件序号排序，合并成一个mp4文件，途中会创建一个临时的 file_list.txt 文件
        :param spider:
        :return:
        """
        # 获取所有的TS文件，并按文件名中的序号排序
        ts_files = [f for f in os.listdir(self.ts_path) if f.endswith('.ts')]
        ts_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

        # 创建一个文件用于ffmpeg的输入
        temp_ts_path_info = os.path.join(self.home_path, 'temp_ts_info.txt')
        with open(temp_ts_path_info, 'w', encoding='utf-8') as file_list:
            for ts_file in ts_files:
                file_list.write(f"file '{os.path.join(self.ts_path, ts_file)}'\n")

        # 调用ffmpeg合成MP4
        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_ts_path_info, '-c', 'copy', os.path.join(spider.save_mp4_path, os.path.basename(spider.save_mp4_path) + '.mp4')])

        # 清理垃圾文件
        shutil.rmtree(self.home_path)
