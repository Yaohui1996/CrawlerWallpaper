# -*- coding:UTF-8 -*-

import requests
from fake_useragent import UserAgent
from time import sleep
from random import uniform
from bs4 import BeautifulSoup
from pathlib import Path

class FavoritesCrawler:
    # constructor
    def __init__(self, categories: str, purity: str, atleast: str, ratios: str, save_dir: str) -> None:
        """[构造函数]

        Args:
            categories (str): [3个bit分别代表General Anime People]
            purity (str): [3个bit分别代表SFW Sketchy NSFW(图片健康度)]
            atleast (str): [最小分辨率]
            ratios (str): [宽高比]
            save_dir (str): [下载路径]]
        """
        self.__url = 'https://wallhaven.cc/search'
        self.__categories: str = categories
        self.__purity: str = purity
        self.__atleast: str = atleast
        self.__ratios: str = ratios
        self.__sorting: str = 'favorites'
        self.__order: str = 'desc'
        self.__save_dir: str = save_dir

    # private成员函数
    def __virtual_headers(self) -> dict:
        """[设置虚拟头]

        Returns:
            dict: [虚拟头参数字典]
        """
        # ua = UserAgent(use_cache_server=False)
        ua = UserAgent(verify_ssl=False)
        vir_header = {
            "user-agent": ua.chrome,
            "connection": "close"}
        return vir_header

    def __get_page_nums(self) -> int:
        """[获取页面的数目]

        Returns:
            int: [总共的页面数目(一页24张图)]
        """
        # 默认的请求url
        url = self.__url
        # 设置请求的参数字典
        request_params = {
            'categories': self.__categories,
            'purity': self.__purity,
            'atleast': self.__atleast,
            'ratios': self.__ratios,
            'sorting': self.__sorting,
            'order': self.__order,
            'page': '2'  # 默认是第2页的图
        }

        # 发送get请求，获取当前page的info_urls
        r = requests.request(method='get', url=url, headers=self.__virtual_headers(),
                             params=request_params)
        print('发送请求的url为: {0}'.format(r.url))
        while r.status_code != 200:
            print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
            sleep(uniform(3, 5))
            r = requests.request(method='get', url=url, headers=self.__virtual_headers(),
                                 params=request_params)
        # 提取信息
        soup = BeautifulSoup(markup=r.text, features='html5lib')
        # 寻找符合条件的tag
        find_result_str = soup.find(name='h2').text
        pages_str_list = find_result_str.split(' / ')
        print(pages_str_list[1])
        return int(pages_str_list[1])

    def __get_one_page_info_urls(self, page: str) -> list:
        """[获取24张图片的主页url]

        Args:
            page (str): [第page页]

        Returns:
            list: [第page页的24张图的主页url]
        """
        # 默认的请求url
        url = self.__url
        # 设置请求的参数字典
        request_params = {
            'categories': self.__categories,
            'purity': self.__purity,
            'atleast': self.__atleast,
            'ratios': self.__ratios,
            'sorting': self.__sorting,
            'order': self.__order,
            'page': page
        }

        # 发送get请求，获取当前page的info_urls
        r = requests.request(method='get', url=url, headers=self.__virtual_headers(),
                             params=request_params)
        print('发送请求的url为: {0}'.format(r.url))
        while r.status_code != 200:
            print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
            sleep(uniform(3, 5))
            r = requests.request(method='get', url=url, headers=self.__virtual_headers(),
                                 params=request_params)
        # 提取信息
        soup = BeautifulSoup(markup=r.text, features='html5lib')
        # 寻找符合条件的tag
        # <a  class="preview" href="https://wallhaven.cc/w/0je3dq" target="_blank" >
        find_all_result_tags = soup.find_all(
            name='a', attrs={'class': 'preview', 'target': '_blank'})
        # 把tag中的href提取出来放入列表one_page_info_urls
        one_page_info_urls = list()
        for tag in find_all_result_tags:
            one_page_info_urls.append(tag.get('href'))
        return one_page_info_urls

    # 判断url是否被下载过
    def __exist_url(self, url: str) -> bool:
        # 读取本地缓存文件
        cache_data = []
        cache_dir = self.__save_dir + 'exist-pictures-info.cache'
        if(Path(cache_dir).exists()):
            with open(cache_dir, 'r', encoding='utf-8') as f:
                cache_data = f.read().splitlines()
        else:
            with open(cache_dir, 'x', encoding='utf-8') as f:
                pass
        # 如果存在则返回True, 否则加入本地并返回False
        if url in cache_data:
            print('url=【{0}】已经存在.'.format(url))
            return True
        else:
            with open(cache_dir, 'a+', encoding='utf-8') as f:
                f.write(url+'\n')
            return False

    def __get_src_url(self, info_url: str) -> str:
        """[获取具体某张图片的文件地址]

        Args:
            info_url (str): [具体某张图的主页url]

        Returns:
            str: [图片的源文件所在地址]
        """
        r = requests.request(method='get', url=info_url,
                             headers=self.__virtual_headers())
        print('发送请求的url为: {0}'.format(r.url))
        while r.status_code != 200:
            print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
            sleep(uniform(1, 10))
            r = requests.request(method='get', url=info_url,
                                 headers=self.__virtual_headers())
        soup = BeautifulSoup(markup=r.text, features='html5lib')
        find_result_tag = soup.find(name='img', attrs={'id': 'wallpaper'})
        src_url = find_result_tag.get('src')
        return src_url

    def __download_picture(self, src_url: str):
        """[下载图片到本地]

        Args:
            src_url (str): [具体的图片的源文件所在地址]
        """
        output_dir = self.__save_dir
        # 判断目标目录是否存在，如果不存在，则新建目录
        output_dir_path = Path(output_dir)
        if not output_dir_path.exists():
            output_dir_path.mkdir()
        # 根据src_url对保存的文件命名
        output_file_name_str = src_url
        output_file_name_str = output_file_name_str.replace(':', '.')
        output_file_name_str = output_file_name_str.replace('/', '.')

        # 如果文件存在，则执行完毕，否则下载
        output_file_path = Path(output_dir + output_file_name_str)
        if output_file_path.exists():
            print('文件{0}已存在！'.format(output_file_name_str))
        else:
            r = requests.request(method='get', url=src_url,
                                 headers=self.__virtual_headers())
            if r.status_code != 200:
                print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
                sleep(uniform(1, 10))
                r = requests.request(method='get', url=src_url,
                                     headers=self.__virtual_headers())
            with open(output_dir + output_file_name_str, 'wb') as f:
                f.write(r.content)
            print('【{0}】下载完毕！'.format(output_dir + output_file_name_str))

    # public成员函数
    def do_crawler(self) -> None:
        """[执行爬虫程序]
        """
        # 获取页面数目
        page_nums = self.__get_page_nums()
        print('检索到【{0}】页图片, 每页【24】张. '.format(page_nums))
        # 请输入本次下载需要的图片数目
        input_nums = int(input('请输入下载的图片数目(会自动向上取整至24的倍数): '))
        if((page_nums - 1) * 24 < input_nums):
            print('图片总数小于输入的数目, 将下载全部图片!')
            download_nums = (page_nums - 1) * 24
        else:
            print('即将开始下载【{0}】张图片'.format(input_nums))
            download_nums = input_nums

        # 解析info_urls
        info_urls = []
        cur_page = 1
        while(len(info_urls) < download_nums):
            sleep(uniform(1, 2))
            cur_page_urls = self.__get_one_page_info_urls(str(cur_page))
            # 删除下载过的url
            i = 0
            while(i < len(cur_page_urls)):
                if(self.__exist_url(cur_page_urls[i])):
                    del cur_page_urls[i]
                    continue
                else:
                    i = i + 1
            cur_page = cur_page + 1
            info_urls.extend(cur_page_urls)
            print('当前待下载的图片数目为: {0}'.format(len(info_urls)))

        # 解析src_urls并下载
        info_urls.reverse()
        while info_urls:
            info_url = info_urls.pop()
            print('正在解析【{0}】...'.format(info_url))
            sleep(uniform(2, 3))
            src_url = self.__get_src_url(info_url)
            print('解析完毕！正在下载...')
            if not (src_url is None):
                self.__download_picture(src_url)
            print('还剩【{0}】张图片待下载！'.format(len(info_urls)))
        print('全部图片下载完毕！')
