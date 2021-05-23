# -*- coding:UTF-8 -*-
def get_page_nums(*,
                  q: str = '',
                  categories: str = '111',
                  purity: str = '100',
                  atleast: str = '2560x1600',
                  ratios: str = '16x10') -> int:
    # 默认的请求url
    url = 'https://wallhaven.cc/search'

    # 设置请求的参数字典
    request_params = {'q': q,
                      'categories': categories,  # categories:3个bit分别代表General Anime People
                      'purity': purity,  # purity:3个bit分别代表SFW Sketchy NSFW(图片健康度)
                      'atleast': atleast,  # atleast:最小分辨率
                      'ratios': ratios,  # ratios:宽高比
                      'sorting': 'random',  # sorting:排序依据  favorites relevance random date_added views toplist hot
                      'seed': seed(),  # random情况下的随机数种子
                      'order': 'desc',  # order:排序方式  desc-降序  asc-升序
                      'page': '2'}  # 默认是第2页的图

    # 发送get请求，获取当前page的info_urls
    import requests
    r = requests.request(method='get', url=url, headers=virtual_headers(),
                         params=request_params)
    while r.status_code != 200:
        print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
        from time import sleep
        from random import uniform
        sleep(uniform(3, 5))
        r = requests.request(method='get', url=url, headers=virtual_headers(),
                             params=request_params)
    print(r.url)
    # 提取信息
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(markup=r.text, features='html5lib')
    # 寻找符合条件的tag
    find_result_str = soup.find(name='h2').text
    pages_str_list = find_result_str.split(' / ')
    print(pages_str_list[1])
    return int(pages_str_list[1])


def get_one_page_info_urls(*,
                           page: str = 2,
                           q: str = '',
                           categories: str = '111',
                           purity: str = '100',
                           atleast: str = '2560x1600',
                           ratios: str = '16x10') -> list:
    # 默认的请求url
    url = 'https://wallhaven.cc/search'

    # 设置请求的参数字典
    request_params = {'q': q,
                      'categories': categories,  # categories:3个bit分别代表General Anime People
                      'purity': purity,  # purity:3个bit分别代表SFW Sketchy NSFW(图片健康度)
                      'atleast': atleast,  # atleast:最小分辨率
                      'ratios': ratios,  # ratios:宽高比
                      'sorting': 'random',  # sorting:排序依据  favorites relevance random date_added views toplist hot
                      'seed': seed(),  # random情况下的随机数种子
                      'order': 'desc',  # order:排序方式  desc-降序  asc-升序
                      'page': page}  # 默认是第一页的图

    # 发送get请求，获取当前page的info_urls
    import requests
    r = requests.request(method='get', url=url, headers=virtual_headers(),
                         params=request_params)
    while r.status_code != 200:
        print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
        from time import sleep
        from random import uniform
        sleep(uniform(3, 5))
        r = requests.request(method='get', url=url, headers=virtual_headers(),
                             params=request_params)

    # 提取信息
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(markup=r.text, features='html5lib')
    # 寻找符合条件的tag
    # <a  class="preview" href="https://wallhaven.cc/w/0je3dq" target="_blank" >
    find_all_result_tags = soup.find_all(name='a', attrs={'class': 'preview', 'target': '_blank'})
    # 把tag中的href提取出来放入列表one_page_info_urls
    one_page_info_urls = list()
    for tag in find_all_result_tags:
        one_page_info_urls.append(tag.get('href'))

    return one_page_info_urls


def get_src_url(info_url: str) -> str:
    import requests
    r = requests.request(method='get', url=info_url, headers=virtual_headers())
    while r.status_code != 200:
        print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
        from time import sleep
        from random import uniform
        sleep(uniform(1, 10))
        r = requests.request(method='get', url=info_url, headers=virtual_headers())

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(markup=r.text, features='html5lib')
    find_result_tag = soup.find(name='img', attrs={'id': 'wallpaper'})
    src_url = find_result_tag.get('src')
    return src_url


def download_picture(src_url: str, output_dir: str = './result/'):
    # 判断目标目录是否存在，如果不存在，则新建目录
    from pathlib import Path
    output_dir_path = Path(output_dir)
    if not output_dir_path.exists():
        output_dir_path.mkdir()
    # 根据src_url对保存的文件命名
    output_file_name_str = src_url
    output_file_name_str = output_file_name_str.replace(':', '_')
    output_file_name_str = output_file_name_str.replace('/', '_')
    output_file_name_str = output_file_name_str.replace('.', '_')
    output_file_name_str = output_file_name_str.replace('-', '_')

    # 如果文件存在，则执行完毕，否则下载
    output_file_path = Path(output_dir + output_file_name_str + '.jpg')
    if output_file_path.exists():
        print('文件{0}已存在！'.format(output_file_name_str))
    else:
        import requests
        r = requests.request(method='get', url=src_url, headers=virtual_headers())
        if r.status_code != 200:
            print('请求发送失败，返回码为{0}，正在重试...'.format(r.status_code))
            from time import sleep
            from random import uniform
            sleep(uniform(1, 10))
            r = requests.request(method='get', url=src_url, headers=virtual_headers())
        with open(output_dir + output_file_name_str + '.jpg', 'wb') as f:
            f.write(r.content)
        print('【{0}】下载完毕！'.format(output_dir + output_file_name_str + '.jpg'))


# 功能：生成随机种子
def seed() -> str:
    lower_letter = [chr(letter).lower() for letter in range(65, 91)]
    upper_letter = [chr(letter) for letter in range(65, 91)]
    zero_to_nine = [str(i) for i in range(0, 10)]

    from random import choices
    ret_seed = ''.join(choices(population=lower_letter + upper_letter + zero_to_nine, k=6))
    return ret_seed


# 设置虚拟头
def virtual_headers() -> dict:
    from fake_useragent import UserAgent
    ua = UserAgent(use_cache_server=False)
    vir_header = {
        "user-agent": ua.chrome,
        "connection": "close"}
    return vir_header
