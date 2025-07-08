import requests
import re
import hashlib


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
    'Connection': 'close',
}

def solve_waf_challenge(response_text):
    """
    解析并解决WAF挑战
    """
    try:
        # 提取key和prefix
        k_match = re.search(r"var k='([^']+)'", response_text)
        sv_match = re.search(r"var sv='([^']+)'", response_text)
        
        if not k_match or not sv_match:
            print("无法找到k或sv参数")
            return None
        
        k = k_match.group(1)
        sv = sv_match.group(1)
        
        
        # 暴力破解找到满足条件的i值
        for i in range(10000000):  # 设置一个合理的上限
            test_string = k + str(i)
            hash_result = hashlib.sha1(test_string.encode()).hexdigest()
            
            if hash_result.startswith(sv):
                cookie_value = f"{k}_{i}"
                return cookie_value
            
            # 每100万次输出进度
            if i % 1000000 == 0 and i > 0:
                print(f"计算进度: {i}")
        
        print("在限制范围内未找到解答")
        return None
        
    except Exception as e:
        print(f"解析WAF挑战失败: {e}")
        return None

def get_built_ver():
    try:
        url = 'https://www.kkrb.net/getMenu'
        
        # 第一次请求，获取WAF挑战
        response = session.post(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 检查是否返回了JavaScript挑战
        if '<script>' in response.text and 'sha1' in response.text:
            print("检测到WAF挑战，正在解决...")
            
            # 解决挑战
            cookie_value = solve_waf_challenge(response.text)
            if not cookie_value:
                print("WAF挑战解决失败")
                return None
            
            # 设置WAF cookie
            session.cookies.set('waf_cookie13', cookie_value)
            
            # 重新请求
            response = session.post(url, headers=headers, timeout=10)
            response.raise_for_status()
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            if 'built_ver' in data:
                return data['built_ver']
            else:
                print(f"响应中缺少built_ver: {data}")
                return None
        except:
            print(f"非JSON响应: {response.text[:200]}...")
            return None
            
    except Exception as e:
        print("get_built_ver 出错:", e)
        return None

async def get_ovd_data():
    try:
        built_ver = get_built_ver()
        if not built_ver:
            raise Exception("无法获取 built_ver")

        url = 'https://www.kkrb.net/getOVData'
        response = session.post(url, data={'version': built_ver}, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
        
    except Exception as e:
        print("get_ovd_data 出错:", e)
        return None