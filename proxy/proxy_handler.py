import requests
import re
# from random import choice
from slitherlib.proxy.retriever import Retriever
# from urllib.parse import urlparse
import urllib.request as urllib_request

ip_addresses = []
used_ip = []


def _get_proxy():
    s = requests.Session()
    ip_addresses = Retriever(thread_count=10).thread_ips
    for i in ip_addresses:
        ip = ip_addresses.pop()
        if ip in used_ip:
            next
        try:
            r = s.get('https://httpbin.org/ip', proxies={'https' : ip, 'http' : ip})
            if re.search(f"{ip.split(sep=':')[0]}", r.text):
                return ip
        except requests.exceptions.ProxyError:
            print('Proxy Timed Out. Removing and Retrying')
        except Exception as e:
            print(e)

def _return_proxyHandler():
    print("CREATE proxyHandler")
    # ip = _get_proxy()
    ip = '165.227.39.167:8080'
    used_ip.append(ip)
    print(f"\nUSING IP: {ip}")
    return urllib_request.ProxyHandler(proxies={'https' : f"https://{ip}", 'http' : f"http://{ip}"})

# _return_proxyHandler()

# urllib_request.ProxyHandler(proxies={'https' : ip, 'http' : ip})
# proxy = "127.0.0.1:8888"
# parsed_url = urlparse(proxy)
# print(parsed_url)
# print(parsed_url.netloc)
# print(parsed_url.scheme)
# if parsed_url.netloc and parsed_url.scheme:
#     proxy_address = '{0!s}://{1!s}'.format(parsed_url.scheme, parsed_url.netloc)
#     print(proxy_address)


