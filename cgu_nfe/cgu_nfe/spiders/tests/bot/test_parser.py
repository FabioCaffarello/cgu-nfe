import os
from ... import parser


def reference_html(file_name):
    _path_debug = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            f"response_files/{file_name}"
        )
    )

    with open(_path_debug, "rb") as file:
        raw_file = file.read()
    return raw_file


def test_shoul_parse_soup():
    reference = reference_html("_on_processing_nfe_request.html")
    soup = parser.parse_nfe_details_data(reference)
    fields = parser.get_nfe_fields(soup)
    print(fields)
    assert 2 == 2


def test_shoul_get_filter_id():
    reference = reference_html("_on_processing_nfe_request.html")
    filter_id = parser.get_filter_id(reference)
    print(filter_id)
    assert 2 == 3
