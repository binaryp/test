import subprocess
from operate import *
# import call_run
import os

url = input("输入需采集的网址：")
cookies = input("输入cookies：")
save_mp4_path_home = input("保存目录: ")

# 网址信息提取
url_params = url.replace("https://", "").split('/')
app_id, course_id = [url_params[0].split(".")[0], url_params[5]]

# 返回索引中需要的数据
datas_params = index(app_id, course_id)

for param in datas_params:
    save_mp4_path = os.path.join(save_mp4_path_home, param['title'])
    os.mkdir(save_mp4_path)
    m3u8_url = m3u8_path(cookies, param)
    # call_run.star_run_craw(m3u8_url, save_mp4_path)

    result = subprocess.run(
        ["python", "call_run.py", m3u8_url, save_mp4_path],
        capture_output=True,  # 捕获子进程输出
        text=True,
        encoding="utf-8",
        errors="replace"  # 或 "ignore"
    )

    # 打印爬虫日志（可选）
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error occurred for {m3u8_url}: {result.stderr}")
        break  # 如果某个任务失败，停止后续任务

    print(f"Finished crawl for: {m3u8_url}")
