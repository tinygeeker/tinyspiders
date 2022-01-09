# encoding = utf-8
import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup


def header(referer):

    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }

    return headers


def request_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'gbk'
            return response.text
    except requests.RequestException:
        return None


def get_page_urls():
    urls = []
    for i in range(1, 3):
        baseurl = 'https://www.tutu555.net/a/cn/xiuren/list_6_{}.html'.format(i)
        html = request_page(baseurl)
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.find(class_='clearfix').find_all('li')
        for item in elements:
            url = item.find('a').get('href')
            title = item.find('a').find('span').string
            print('%s__@@__%s' % (title, url))
            urls.append('{}__@@__{}' . format(title, url))

    return urls


def download_Pic(title, image_list):
    # 新建文件夹
    os.mkdir(title)
    j = 1
    # 下载图片
    for item in image_list:
        filename = '%s/%s.jpg' % (title, str(j))
        print('downloading....%s : NO.%s' % (title, str(j)))
        with open(filename, 'wb') as f:
            img = requests.get(item).content
            f.write(img)
        j += 1

def download(url):
    # print('start')
    res = url.split('__@@__')
    # print(res[0], res[-1])
    html = request_page(res[-1])
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find(class_='page').find_all('a')[-2].string
    # print(total)
    title = res[0]
    print(title, total)
    image_list = []

    for i in range(int(total)):
        page = i + 1
        page_url = f'_{page}.html'.join(res[-1].split('.html')) if page > 1 else res[-1]
        html = request_page(page_url)
        soup = BeautifulSoup(html, 'lxml')
        img_url = soup.find(class_='content').find_all('img')
        for item in img_url:
            im_url = item.get('src')
            print(im_url)
            image_list.append(im_url)

    download_Pic(title, image_list)


def download_all_images(list_page_urls):
    # 获取每一个详情妹纸
    # works = len(list_page_urls)
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as exector:
        for url in list_page_urls:
            exector.submit(download, url)


if __name__ == '__main__':
    # 获取每一页的链接和名称
    # for i in range(1,4):
    #     print(i)
    # print('_3.html'.join('https://www.tutu555.net/a/cn/xiuren/2022/0101/41919.html'.split('.html')))
    list_page_urls = get_page_urls()
    # print(list_page_urls)
    download_all_images(list_page_urls)