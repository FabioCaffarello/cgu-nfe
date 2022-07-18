from . import server_status

class BaseError(Exception):
    """Base Error"""
    pass

class CrawlingError(BaseError):
    """A crawling error happened"""

    def __init__(self, status_code, status_detail=""):
        self.status_code = status_code
        self.status_detail = status_detail


class GatewayTimeoutError(CrawlingError):
    """Connectivity between the proxy and the website (not necessarily proxy problem)"""

    def __init__(self, status_detail="Gateway Timeout"):
        super().__init__(server_status.GATEWAY_TIMEOUT, status_detail)
