import re
import unicodedata

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from . import input, static


class GenerateUrlRequest(input.Input):
    def __init__(self):
        super().__init__()

    def generate_url_index_request(self, offset):
        url = "".join([
            static.HOST,
            static.PARAMS,
            str(offset),
            static.QUERY,
            self.filter_gte,
            static.FILTER,
            self.filter_lt,
            static.META,
        ])
        return url

    def generate_url_nfe_request(self, nfe_id):
        url = "".join([
            static.HOST,
            nfe_id,
            static.NFE_PARAMS,
        ])
        return url

    def generate_url_products_services_request(self, filter_id):
        url = "".join([
            static.HOST,
            static.PRODUCTS_SERVICES_PARAMS,
            filter_id,
            static.PRODUCTS_SERVICES_META
        ])
        return url

    def generate_url_events_request(self, filter_id):
        url = "".join([
            static.HOST,
            static.EVENTS_PARAMS,
            filter_id,
            static.EVENTS_META
        ])
        return url


def _get_soup(raw_data):
    try:
        soup = BeautifulSoup(raw_data)
        if not soup:
            return None
        return soup
    except Exception:
        return None


def parse_nfe_details_data(raw_data):
    soup_raw_data = _get_soup(raw_data)
    parsed_data = (
        soup_raw_data
        .find_all(
            "div",
            {
                "class": re.compile(
                    r"col-xs-12 col-sm-2|col-xs-12 col-sm-3|col-xs-12 col-sm-4|col-xs-12 col-sm-5|col-xs-12 col-sm-6|col-xs-12 col-sm-7"
                )
            }
        )
    )

    return parsed_data


def get_filter_id(raw_data):
    soup_raw_data = _get_soup(raw_data)
    parsed_data = (
        soup_raw_data
        .find_all(
            "script"
        )
    )
    for tag in parsed_data:
        if "idIdentificacao" in tag.text:
            idIdentificacao = re.search(r'idIdentificacao = "([0-9]*)";', tag.text).group(1)
    return idIdentificacao


def get_nfe_fields(parsed_data: ResultSet):
    fields = dict()
    destinatario_fields = dict()
    emitente_fields = dict()
    for tag in parsed_data:
        field_name = tag.find("strong").contents[0] if tag.find("span") else None
        field_data = tag.find("span").text if tag.find("span") else None
        if field_name:
            field_name = camel_case_format(field_name)
            if tag.find_parent("div", attrs={"id": "destinatario"}):
                destinatario_fields[field_name] = field_data if field_data else None
            elif tag.find_parent("div", attrs={"id": "emitente"}):
                emitente_fields[field_name] = field_data if field_data else None
            else:
                fields[field_name] = field_data if field_data else None
    fields["destinatario"] = destinatario_fields
    fields["emitente"] = emitente_fields

    return fields


def camel_case_format(text: str) -> str:

    text_normalized = normalize_text(str(text))
    text_cleaned = "".join(
        filter(
            lambda x: x.isalpha() or x.isdigit(),
            text_normalized
            .title()
            .replace(" ", "")
        )
    )
    text_formated = "".join([
        text_cleaned[0].lower(),
        text_cleaned[1:]
    ])

    return text_formated


def normalize_text(text: str) -> str:

    text_normalized = str(
        unicodedata
        .normalize("NFD", text)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    return text_normalized
