# -*- coding: utf-8 -*-
"""4KVM 在线影视 TVBox 配置源
对接 https://4kvm.alonglfb.com 真实 API
运行: pip install flask requests && python tvbox_4kvm.py [端口]
"""
import sys
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE = "https://4kvm.alonglfb.com"
UA = "Mozilla/5.0"

CLASSES = [
    (20, "电影·纪录片"), (21, "电影·短片"), (22, "电影·动画片"),
    (23, "电视剧·国产"), (24, "电视剧·港台"), (30, "电视剧·泰剧"),
    (45, "电视剧·短剧"),
    (31, "综艺·大陆"), (32, "综艺·港台"), (33, "综艺·日韩"),
    (34, "综艺·欧美"),
    (35, "动漫·国产"), (36, "动漫·欧美"), (37, "动漫·日本"),
    (41, "体育·足球"),
]


def api_get(path):
    try:
        r = requests.get(BASE + path, headers={"User-Agent": UA}, timeout=10)
        return r.json()
    except Exception:
        return None


@app.route('/vod/class')
def vod_class():
    return jsonify([
        {"type_id": str(t), "type_name": n} for t, n in CLASSES
    ])


@app.route('/vod/list')
def vod_list():
    tid = request.args.get("type", "20")
    pg = int(request.args.get("pg", 1))
    d = api_get(f"/api/vod?type_id={tid}&pg={pg}")
    if not d:
        return jsonify({"page": pg, "pagecount": 1, "total": 0, "list": []})
    return jsonify({
        "page": d.get("page", pg),
        "pagecount": d.get("pagecount", 1),
        "total": d.get("total", 0),
        "list": [
            {
                "vod_id": v.get("id"),
                "vod_name": v.get("name"),
                "vod_pic": v.get("pic"),
                "vod_remarks": v.get("remarks", ""),
            }
            for v in d.get("list", [])
        ],
    })


@app.route('/vod/detail')
def vod_detail():
    vid = request.args.get("id", "")
    d = api_get(f"/api/vod?id={vid}")
    if not d or not d.get("list"):
        return jsonify({"vod_id": vid, "vod_name": "未找到"})
    v = d["list"][0]
    sources = v.get("sources", [])
    play_from = []
    play_url = []
    for s in sources:
        play_from.append(s.get("sourceName", "线路"))
        eps = s.get("episodes", [])
        play_url.append("#".join(
            f'{e.get("name", "")}${e.get("url", "")}' for e in eps
        ))
    return jsonify({
        "vod_id": vid,
        "vod_name": v.get("name"),
        "vod_pic": v.get("pic"),
        "type_name": v.get("type_name"),
        "vod_year": v.get("year"),
        "vod_area": v.get("area"),
        "vod_remarks": v.get("remarks"),
        "vod_actor": v.get("actor"),
        "vod_director": v.get("director"),
        "vod_content": v.get("content"),
        "vod_play_from": "$$$".join(play_from),
        "vod_play_url": "$$$".join(play_url),
    })


@app.route('/vod/search')
def vod_search():
    wd = request.args.get("wd", "")
    d = api_get(f"/api/vod/suggest?q={wd}&limit=20")
    if not d:
        return jsonify({"list": []})
    return jsonify({
        "list": [
            {
                "vod_id": v.get("id"),
                "vod_name": v.get("name"),
                "vod_pic": v.get("pic"),
                "vod_remarks": v.get("remarks", ""),
            }
            for v in d.get("list", [])
        ],
    })


@app.route('/')
def index():
    return jsonify({"name": "4KVM影视源", "base": BASE,
                    "endpoints": {"分类": "/vod/class",
                                  "列表": "/vod/list?type=23&pg=1",
                                  "详情": "/vod/detail?id=ikun_57075",
                                  "搜索": "/vod/search?wd=庆余年"}})


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
