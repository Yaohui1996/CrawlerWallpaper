# -*- coding:UTF-8 -*-
from crawler import get_page_nums
from crawler import get_one_page_info_urls
from crawler import get_src_url
from crawler import download_picture

if __name__ == '__main__':
    # 获取页面数目
    kwargs_get_page_nums = {'q': '',
                            'categories': '111',
                            'purity': '100',
                            'atleast': '2560x1600',
                            'ratios': '16x10'}
    page_nums = get_page_nums(**kwargs_get_page_nums)
    print('检索到【{0}】页图片，每页【24】张。'.format(page_nums))

    # 请输入下载的图片页数
    download_page_nums = int(input('请输入下载的图片页数：'))
    min_nums = min(page_nums, download_page_nums)
    print('即将开始下载【{0}】页，【{1}】张图片...'.format(min_nums, 24 * min_nums))

    # 解析info_urls
    info_urls = list()
    for i in range(0, min_nums):
        kwargs_get_one_page_info_urls = kwargs_get_page_nums.copy()
        kwargs_get_one_page_info_urls['page'] = str(i + 1)
        info_urls.extend(get_one_page_info_urls(**kwargs_get_one_page_info_urls))
        print('已解析{0}张图片的主页地址！'.format(len(info_urls)))

    # 解析src_urls并下载
    info_urls.reverse()
    while info_urls:
        info_url = info_urls.pop()
        print('正在解析【{0}】...'.format(info_url))
        src_url = get_src_url(info_url)
        print('解析完毕！正在下载...')
        if not (src_url is None):
            download_picture(src_url)
        print('还剩【{0}】张图片待下载！'.format(len(info_urls)))

    print('全部图片下载完毕！')
