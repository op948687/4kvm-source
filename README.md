# 4KVM 影视源 (GitHub 托管)

> 聚合影视源，对接 `https://4kvm.alonglfb.com` 真实接口。
> 仅供个人学习爬虫 / 影视聚合技术使用。

## 源简介
- 数据源：4KVM 聚合接口（`/api/vod`、`/api/vod/suggest`）
- 播放链接：直接 m3u8（iKun 线路），无需二次解析
- 分类：电影·纪录片 / 电视剧·国产·港台·泰剧·短剧 / 综艺·动漫 / 体育·足球

## 文件
| 文件 | 说明 |
|---|---|
| `4kvm.py` | Python 爬虫源（FongMi / 影视TV，`base.spider.Spider` 格式） |
| `csp_4kvm.py` | 同 4kvm.py 的副本 |
| `tvbox_4kvm.py` | Flask 自建后端（标准 JSON 订阅接口） |
| `.gitignore` | 忽略缓存 |

## 使用

### 方式一：影视TV / FongMi（py 爬虫）
支持 Python 爬虫的播放器可直接加载 `4kvm.py`。

**加载地址（任选）：**
- 快取(CDN，访问最快)：`https://h.uguu.se/gxTqJBXo.py`
- jsDelivr：`https://cdn.jsdelivr.net/gh/op948687/4kvm-source@main/4kvm.py`
- GitHub raw：`https://raw.githubusercontent.com/op948687/4kvm-source/main/4kvm.py`

> 注意：uguu.se 为临时文件站，文件会过期清理，适合临时加速；长期请用 jsDelivr / GitHub 地址。

### 方式二：自建后端（JSON 接口）
```bash
pip install flask requests
python tvbox_4kvm.py 5000
```

## 仓库
- https://github.com/op948687/4kvm-source
