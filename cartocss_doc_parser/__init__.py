# -*- coding: utf-8 -*-

import os
import re

from bs4 import BeautifulSoup
import requests

__version__ = '0.0.1'
__version_info__ = tuple([int(i) for i in __version__.split('.')])
__title__ = 'cartocss_doc_parser'
__author__ = 'Álvaro Mondéjar Rubio'
__description__ = 'CartoCSS documentation parser.'

CARTOCSS_DOC_URL = 'https://carto.com/developers/styling/cartocss/'

DEFAULT_USER_AGENT = '%s v%s' % (__title__, __version__)

PROP_DETAILS_ATTR_MAP = {
    "Description": "description",
    "Sample CartoCSS Code": "sample",
    "Default Value": "default",
}

UNDOCUMENTED_VALUES = ["keyword", "unsigned", "tags"]

def get_cartocss_doc_html(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    if os.path.isfile(url):
        with open(url, encoding="utf-8") as f:
            markup = f.read()
        return markup
    return requests.get(url, headers={'User-Agent': user_agent}).text


def get_cartocss_doc_soup(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    markup = get_cartocss_doc_html(url=url, user_agent=user_agent)
    return BeautifulSoup(markup, 'lxml')


def _parse_table_links_after_h(soup,
                               h_id,
                               url=CARTOCSS_DOC_URL,
                               properties=False):
    h = soup.find(id=h_id)
    table = h.find_next()
    while table.name != "table":
        table = table.find_next()
    for td in table.find_all("td"):
        a = td.find("a", recursive=False)
        if a is None:
            break
        _id = a['href'].strip("#")
        prop = {
            "name": str(a.string),
            "link": url + a['href'],
            "id": _id,
        }
        if properties:
            prop_h = soup.find(id=_id)
            data_type_container = prop_h.find_next()

            # Error in property title:
            # https://carto.com/developers/styling/cartocss/#point-comp-op-keyword
            if prop_h.string is not None and "`" in prop_h.string:
                prop["type"] = prop_h.string.split("`")[-1]
            else:
                prop["type"] = data_type_container.string
            if data_type_container.name == "table":
                prop_table = data_type_container
            else:
                prop_table = data_type_container.find_next()
            while prop_table.name != "table":
                prop_table = prop_table.find_next()

            _details_attr_map = PROP_DETAILS_ATTR_MAP
            if prop["type"] == "keyword":
                _details_attr_map["Available Values"] = "variants"
            prop_details = {}
            _current_prop_detail = None
            for prop_td in prop_table.find_all("td"):
                if _current_prop_detail is None:
                    _current_prop_detail = PROP_DETAILS_ATTR_MAP.get(
                        prop_td.string, None)
                else:
                    if _current_prop_detail == "default":
                        code_container = prop_td.find("code")

                        if code_container is None:
                            default = re.search(
                                r'^([^.,]+)', prop_td.get_text().lower()
                            ).group(1)
                            if " (" in default:
                                default = default.split(" (")[0]
                        else:
                            default = code_container.string.lower()
                        prop_details[_current_prop_detail] = default
                    elif _current_prop_detail == "variants":

                        code_containers = prop_td.find_all("code")
                        if len(code_containers) > 0:
                            prop_details[_current_prop_detail] = []

                            # Unconsistency in Available Values code:
                            # https://carto.com/developers/styling/cartocss/#
                            # -torque-aggregation-function-keyword
                            if len(code_containers) == 1:
                                variants = code_containers[0].string.split(",")
                                for variant in variants:
                                    prop_details[_current_prop_detail].append(
                                        variant.strip(" "))
                            else:
                                for code_container in code_containers:
                                    prop_details[_current_prop_detail].append(
                                        code_container.string)
                    else:
                        prop_details[_current_prop_detail] = prop_td.get_text()
                    _current_prop_detail = None
            prop.update(prop_details)
        yield prop

def cartocss_data_types(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    soup = get_cartocss_doc_soup(url=url, user_agent=user_agent)
    for value in _parse_table_links_after_h(soup, "cartocss-values", url=url):
        data_type = value["name"].lower()
        yield data_type
        if data_type[-1] == "s":
            yield data_type[:-1]
    for value in UNDOCUMENTED_VALUES:
        yield value

def parse_symbolizers(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "cartocss-symbolizer", url=url)

def parse_values(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "cartocss-values", url=url)

def parse_other_parameters(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(
        soup, "other-cartocss-parameters", url=url)

def parse_torque_properties(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(
        soup, "cartocss---torque-maps", url=url, properties=True)

def parse_common_elements(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(
        soup, "common-elements", url=url, properties=True)

def parse_map_background_and_string_elements(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(
        soup, "map-background-and-string-elements", url=url, properties=True)

def parse_polygon(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "polygon", url=url, properties=True)

def parse_line(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "line", url=url, properties=True)

def parse_markers(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "markers", url=url, properties=True)

def parse_shield(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "shield", url=url, properties=True)

def parse_line_pattern(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(
        soup, "line-pattern", url=url, properties=True)

def parse_polygon_pattern(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(
        soup, "polygon-pattern", url=url, properties=True)

def parse_raster(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "raster", url=url, properties=True)

def parse_point(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "point", url=url, properties=True)

def parse_text(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(soup, "text", url=url, properties=True)

def parse_building(soup, url=CARTOCSS_DOC_URL):
    return _parse_table_links_after_h(
        soup, "building", url=url, properties=True)

def cartocss_doc(url=CARTOCSS_DOC_URL, user_agent=DEFAULT_USER_AGENT):
    soup = get_cartocss_doc_soup(url=url, user_agent=user_agent)
    return {
        "symbolizers": parse_symbolizers(soup, url=url),
        "values": parse_values(soup, url=url),
        "other_parameters": parse_other_parameters(soup, url=url),
        "torque_properties": parse_torque_properties(soup, url=url),
        "common_elements": parse_common_elements(soup, url=url),
        "map_background_and_string_elements": \
            parse_map_background_and_string_elements(soup, url=url),
        "polygon": parse_polygon(soup, url=url),
        "line": parse_line(soup, url=url),
        "markers": parse_markers(soup, url=url),
        "shield": parse_shield(soup, url=url),
        "line_pattern": parse_line_pattern(soup, url=url),
        "polygon_pattern": parse_polygon_pattern(soup, url=url),
        "raster": parse_raster(soup, url=url),
        "point": parse_point(soup, url=url),
        "text": parse_text(soup, url=url),
        "building": parse_building(soup, url=url),
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(cartocss_doc())
