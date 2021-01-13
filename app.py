import os
import time
from helps import get_one_page, parse_one_page, write_to_file

def crawl(offset):
    url = os.getenv('URL') + '?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    # 如果已存在结果文件，清空
    with open(os.getenv('RESULT_FILE'), 'w') as f:
        f.truncate()

    # 爬取
    for i in range(10):
        print(f'Crawling Top {i*10+1} to {(i+1)*10}.....')
        crawl(i * 10)

        # 防止反爬虫
        time.sleep(1)

    print("Results has been written to " + os.getenv('RESULT_FILE'))