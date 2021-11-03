# -*- coding:UTF-8 -*-

from crawler import FavoritesCrawler

if __name__ == '__main__':
    crawler_instance = FavoritesCrawler(
        '001', '100', '1920x1080', '16x9,16x10', '/Users/yaohui/Pictures/wallhaven/')
    crawler_instance.do_crawler()
