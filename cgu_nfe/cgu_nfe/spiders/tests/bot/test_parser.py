import json
import os
import logging

from ... import parser

logger = logging.getLogger(__name__)


def _get_reference_file_path(file_name):
    path_debug = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            f"reference_files/{file_name}"
        )
    )
    return path_debug


def reference_html(file_name):
    _path_debug = _get_reference_file_path(file_name)

    with open(_path_debug, "rb") as file:
        raw_file = file.read()
    return raw_file


def reference_json(file_name):
    _path_debug = _get_reference_file_path(file_name)

    with open(_path_debug, "rb") as file:
        raw_file = json.loads(file)
    return raw_file


def test_shoul_parse_soup():
    reference = reference_html("_on_processing_nfe_request.html")
    soup = parser.parse_nfe_details_data(reference)
    fields = parser.get_nfe_fields(soup)
    logger.info(fields)
    assert 2 == 3


def test_shoul_get_filter_id():
    expected_id = "111001370"
    reference = reference_html("_on_processing_nfe_request.html")
    filter_id = parser.get_filter_id(reference)
    assert expected_id == filter_id
