import asyncio
import json
import os

import requests
import scrapy
from cgu_nfe.items import CguNfeItem, CguNfeLoader

from cgu_nfe import config, errors, proxy

from . import parser, static


class CguNfeSpider(scrapy.Spider):
    config.LoggingConfig()
    name = 'cgu_nfe'

    def start_requests(self):
        self.products_services = None
        self.events_data = None
        self._queue = asyncio.Queue()
        self.url_request = parser.GenerateUrlRequest()
        self.proxy_blacklist = list()
        self._proxy_client = proxy.GetProxy()
        self._data = list()
        self._id_bag = list()
        self._offset = 0
        self._current_errors_attemps = 0
        return self._first_request()

    def _first_request(self):
        self._proxy = self._proxy_client.get_proxy(self.proxy_blacklist)
        self.logger.info(f"FIRST REQUEST WITH PROXY: {self._proxy}")
        url = self.url_request.generate_url_index_request(self._offset)
        yield scrapy.Request(
            url,
            callback=self._on_processing_first_request,
            errback=self._on_error,
            meta={
                "proxy": self._proxy
            },
            dont_filter=True
        )

    def _on_processing_first_request(self, response):
        _response = response.json()
        self.debug_response("_on_processing_first_request.json", json.dumps(_response, indent=4).encode("utf-8"))
        array_data = _response.get('data', None)

        if array_data is None or array_data == []:
            _has_next = False

        if self._offset < _has_next:
            self._offset += 1
            for _data in array_data:
                nfe_id = _data.get('chaveNotaFiscal', None)
                if nfe_id not in self._id_bag:
                    self._queue.put_nowait(1)
                self._id_bag.append(nfe_id)
                cb_kwargs = {
                    "nfe_id": nfe_id
                }
                yield scrapy.Request(
                    self.url_request.generate_url_nfe_request(nfe_id),
                    callback=self._on_processing_nfe_request,
                    cb_kwargs=cb_kwargs,
                    errback=self._on_error,
                    meta={
                        "proxy": self._proxy
                    }
                )
            yield response.follow(
                self.url_request.generate_url_index_request(self._offset),
                callback=self._on_processing_first_request,
                errback=self._on_error,
                meta={
                    "proxy": self._proxy
                }
            )
        else:
            self.logger.info("NO MORE PAGES")
            if self._queue.empty():
                self.logger.info("Queue End's....")

    def _on_processing_nfe_request(self, response, nfe_id):
        items = CguNfeLoader(CguNfeItem())
        self.debug_response("_on_processing_nfe_request.html", response.body)
        filter_id = parser.get_filter_id(response.body)
        self._request_products_services(filter_id)
        self._request_events(filter_id)
        raw_data = parser.parse_nfe_details_data(response.body)
        nfe_data = parser.get_nfe_fields(raw_data)
        nfe_data["produtosServicos"] = self.products_services_data
        nfe_data["eventos"] = self.events_data
        self._queue.get_nowait()
        items.add_fields(nfe_data)
        yield items.load_item()

    def _request_products_services(self, filter_id):
        try:
            r = (
                requests
                .get(
                    self.url_request.generate_url_products_services_request(filter_id),
                    proxies={
                        "http": self._proxy,
                        "https": self._proxy
                    },
                    timeout=5
                )
            )
            self.products_services_data = r.json().get('data', None)
        except:
            pass

    def _request_events(self, filter_id):
        try:
            r = (
                requests
                .get(
                    self.url_request.generate_url_events_request(filter_id),
                    proxies={
                        "http": self._proxy,
                        "https": self._proxy
                    },
                    timeout=5
                )
            )
            self.events_data = r.json().get('data', None)
        except:
            pass

    def debug_response(self, file_name, content):
        _path_debug = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                static.PATH_DEBUG,
                file_name
            )
        )

        with open(_path_debug, "wb") as file:
                file.write(content)

    def _on_error(self, failure):
        self.logger.warning(f"error[{failure}] on request")
        self.logger.warning("Blacklisting used proxy")
        self.proxy_blacklist.append(self._proxy)
        if self._current_errors_attemps <= static.MAX_PROXY_ATTEMPTS:
            self.logger.warning("Trying Again")
            self._current_errors_attemps += 1
            if not self._queue.empty():
                self._queue.get_nowait()
            return self._first_request()

        raise errors.GatewayTimeoutError()
