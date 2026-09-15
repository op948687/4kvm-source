# -*- coding: utf-8 -*-
# 4kvm 影视 Python 爬虫源（赵喵/FongMi 格式）
import sys
from base.spider import Spider

sys.path.append('..')


class Spider(Spider):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-S9080 Build/V417IR; wv) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
                      'Chrome/101.0.4951.61 Safari/537.36',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    host = ''

    CLASSES = [
        (20, '电影·纪录片'), (21, '电影·短片'), (22, '电影·动画片'),
        (23, '电视剧·国产'), (24, '电视剧·港台'), (30, '电视剧·泰剧'),
        (45, '电视剧·短剧'),
        (31, '综艺·大陆'), (32, '综艺·港台'), (33, '综艺·日韩'),
        (34, '综艺·欧美'),
        (35, '动漫·国产'), (36, '动漫·欧美'), (37, '动漫·日本'),
        (41, '体育·足球'),
    ]

    def init(self, extend=''):
        ext = extend.strip()
        if ext.startswith('http'):
            self.host = ext.rstrip('/')
        else:
            self.host = 'https://4kvm.alonglfb.com'
        return self.host

    def homeContent(self, filter):
        return {'class': [
            {'type_id': str(t), 'type_name': n} for t, n in self.CLASSES
        ]}

    def homeVideoContent(self):
        try:
            r = self.fetch(f'{self.host}/api/vod', headers=self.headers,
                           verify=False).json()
        except Exception:
            return {'list': []}
        return {'list': [
            {'vod_id': v.get('id'), 'vod_name': v.get('name'),
             'vod_pic': v.get('pic'), 'vod_remarks': v.get('remarks', '')}
            for v in r.get('list', [])
        ]}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            r = self.fetch(f'{self.host}/api/vod?type_id={tid}&pg={pg}',
                           headers=self.headers, verify=False).json()
        except Exception:
            return {'list': []}
        return {
            'page': r.get('page', 1),
            'pagecount': r.get('pagecount', 1),
            'limit': '20',
            'total': r.get('total', 0),
            'list': [
                {'vod_id': v.get('id'), 'vod_name': v.get('name'),
                 'vod_pic': v.get('pic'), 'vod_remarks': v.get('remarks', '')}
                for v in r.get('list', [])
            ],
        }

    def detailContent(self, ids):
        try:
            r = self.fetch(f'{self.host}/api/vod?id={ids[0]}',
                           headers=self.headers, verify=False).json()
            v = r['list'][0]
        except Exception:
            return {'list': []}

        play_from, play_url = [], []
        for s in v.get('sources', []):
            play_from.append(s.get('sourceName', '线路'))
            play_url.append('#'.join(
                f"{e.get('name', '')}${e.get('url', '')}"
                for e in s.get('episodes', [])
            ))

        return {'list': [{
            'vod_id': v.get('id'),
            'vod_name': v.get('name'),
            'vod_pic': v.get('pic'),
            'type_name': v.get('type_name'),
            'vod_year': v.get('year'),
            'vod_area': v.get('area'),
            'vod_remarks': v.get('remarks'),
            'vod_actor': v.get('actor'),
            'vod_director': v.get('director'),
            'vod_content': v.get('content'),
            'vod_play_from': '$$$'.join(play_from),
            'vod_play_url': '$$$'.join(play_url),
        }]}

    def searchContent(self, key, quick, pg='1'):
        try:
            r = self.fetch(f'{self.host}/api/vod/suggest?q={key}&limit=20',
                           headers=self.headers, verify=False).json()
        except Exception:
            return {'list': []}
        return {'list': [
            {'vod_id': v.get('id'), 'vod_name': v.get('name'),
             'vod_pic': v.get('pic'), 'vod_remarks': v.get('remarks', '')}
            for v in r.get('list', [])
        ]}

    def playerContent(self, flag, id, vipFlags):
        return {
            'jx': 0,
            'parse': 0,
            'url': id,
            'header': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) '
                              'AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1'
            },
        }

    def getName(self):
        return '4kvm'

    def isVideoFormat(self, url):
        return url.endswith(('.m3u8', '.mp4', '.flv', '.mkv'))

    def manualVideoCheck(self):
        return False

    def destroy(self):
        pass

    def localProxy(self, param):
        return {}
