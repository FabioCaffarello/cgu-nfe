import random

import redis


class GetProxy:
    def _redis_connect(self):
        redis_client = redis.Redis(
            host='redis',
            port='6379',
            db=0
        )

        return redis_client

    def _get_proxy_array(self):
        redis_client = self._redis_connect()
        proxy_array = redis_client.zrange('proxy', 0, -1)
        proxy_array = [proxy.decode('utf-8') for proxy in proxy_array]

        return proxy_array

    def get_proxy(self, blacklist=[]):
        proxy_array = self._get_proxy_array()
        proxy_array_filterd = list(filter(lambda proxy: proxy not in blacklist, proxy_array))
        proxy = random.choice(proxy_array_filterd)
        return proxy
