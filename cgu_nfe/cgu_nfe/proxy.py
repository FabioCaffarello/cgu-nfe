import concurrent.futures
import redis
import requests
from bs4 import BeautifulSoup


class GetProxy:
    def __init__(self):
        self._url_free_proxy = "https://free-proxy-list.net"
        self._url_proxy_valid = "http://httpbin.org/ip"
        self.proxy_pool = []

    def _free_proxy_request(self):
        response = requests.get(self._url_free_proxy)
        return response

    def _on_processing_free_proxy_request(self):
        response = self._free_proxy_request()
        soup = BeautifulSoup(response.content, "html.parser")
        proxies = list()
        for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                proxies.append(f"http://{str(ip)}:{str(port)}")

            except IndexError:
                continue

        return proxies

    def _proxy_validation(self, proxy):
        try:
            response = requests.get(self._url_proxy_valid, proxies={"http": proxy, "https": proxy}, timeout=5)
            self.proxy_pool.append(proxy)
            self.to_redis(proxy)
        except:
            pass

    def get_proxy_pool(self):
        proxies = self._on_processing_free_proxy_request()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self._proxy_validation, proxies)

    def to_redis(self, proxy):
        cache = redis.Redis(
            host= 'localhost',
            port= '6379',
            db=0
        )

        return cache.zadd('proxy', {proxy: 0})


# if __name__ == "__main__":
#     proxy_client = GetProxy()
#     proxy_client.get_proxy_pool()
