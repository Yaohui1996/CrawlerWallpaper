# CrawlerWallpaper
## 用途及用法
用于爬取[https://wallhaven.cc/](https://wallhaven.cc/)的壁纸

修改`kwargs_get_page_nums`的`value`即可更改筛选规则

```python
kwargs_get_page_nums = {'q': '',                # 图片的关键词。默认为空
                        'categories': '111',    # 图片分类。3个bit分别对应 General Anime People
                        'purity': '100',        # 图片纯洁度。3个bit分别对应 SFW Sketchy NSFW
                        'atleast': '2560x1600', # 图片最小分辨率。 
                        'ratios': '16x10'}      # 图片宽高比。
```

## 环境要求
- python = 3.9.4
- requests = 2.25.1
- beautifulsoup4 = 4.9.3
- html5lib = 1.1
- fake-useragent = 0.1.11