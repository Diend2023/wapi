import requests


session = requests.Session()
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'cache-control': 'no-cache',
    'content-length': '0',
    'dnt': '1',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.kkrb725.com/?viewpage=view%2Foverview',
    'sec-ch-ua': '""Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
}

def _warmup_connection(url):
    """预热连接，消耗掉第一次失败请求"""
    try:
        session.post(url, headers=headers, timeout=1)
    except:
        pass  # 忽略预热请求的错误

def get_built_ver():
    try:
        url = 'https://www.kkrb725.com/getMenu'
        _warmup_connection(url)  # 预热连接，消耗掉第一次失败请求
        response = session.post(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['built_ver']
    except Exception as e:
        print("get_built_ver 出错:", e)
        return None

def get_ovd_data():
    try:
        built_ver = get_built_ver()
        if not built_ver:
            raise Exception("无法获取 built_ver")
        url = 'https://www.kkrb725.com/getOVData'
        response = session.post(url, data={'version': built_ver}, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print("get_ovd_data 出错:", e)
        return None