# -*- coding: utf-8 -*-

import types

from cartocss_doc_parser import (
    cartocss_data_types,
    parse_symbolizers,
    parse_values,
    parse_other_parameters,
    parse_torque_properties,
    parse_common_elements,
    parse_map_background_and_string_elements,
    parse_polygon,
    parse_line,
    parse_markers,
    parse_shield,
    parse_line_pattern,
    parse_polygon_pattern,
    parse_raster,
    parse_point,
    parse_text,
    parse_building,
)

class TestParser:
    def setup_class(cls):
        cls.carto_css_data_types = list(cartocss_data_types())

    def assert_link(self, url, contains=["#"]):
        assert isinstance(url, str)
        assert len(url) > 0
        for _string in contains:
            assert _string in url

    def assert_string(self, value):
        assert isinstance(value, str)
        assert len(value) > 0

    def assert_id(self, value):
        self.assert_string(value)
        assert "#" not in value

    def assert_type(self, value):
        self.assert_string(value)
        assert value in self.carto_css_data_types

    def assert_description(self, value):
        self.assert_string(value)

    def assert_default(self, value):
        self.assert_string(value)

    def assert_variants(self, value):
        assert isinstance(value, list)
        assert len(value) > 1
        for item in value:
            self.assert_string(item)

    def assert_table_links_after_h(self,
                                   soup,
                                   parser_func,
                                   values=5,
                                   properties=False):
        _values = parser_func(soup)
        assert isinstance(_values, types.GeneratorType)
        print()

        _values = list(_values)
        assert len(_values) == values

        for _value in _values:
            assert "link" in _value
            self.assert_link(_value["link"])

            assert "name" in _value
            self.assert_string(_value["name"])

            assert "id" in _value
            self.assert_id(_value["id"])
            print("#" + _value["id"])

            if properties:
                assert "type" in _value
                self.assert_type(_value["type"])

                assert "description" in _value
                self.assert_description(_value["description"])

                assert "default" in _value
                self.assert_default(_value["default"])

                if _value["type"] == "keyword":
                    assert "variants" in _value
                    self.assert_variants(_value["variants"])
        print()

    def test_symbolizers_markup(self, soup):
        self.assert_table_links_after_h(soup, parse_symbolizers, values=10)

    def test_values_markup(self, soup):
        self.assert_table_links_after_h(soup, parse_values, values=9)

    def test_other_parameters_markup(self, soup):
        self.assert_table_links_after_h(soup, parse_other_parameters, values=3)

    def test_torque_properties_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_torque_properties, values=7, properties=True)

    def test_common_elements_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_common_elements, values=3, properties=True)

    def test_map_background_and_string_elements_markup(self, soup):
        self.assert_table_links_after_h(
            soup,
            parse_map_background_and_string_elements,
            values=4,
            properties=True)

    def test_polygon_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_polygon, values=10, properties=True)

    def test_line_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_line, values=18, properties=True)

    def test_markers_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_markers, values=21, properties=True)

    def test_shield_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_shield, values=34, properties=True)

    def test_line_pattern_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_line_pattern, values=8, properties=True)

    def test_polygon_pattern_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_polygon_pattern, values=10, properties=True)

    def test_raster_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_raster, values=9, properties=True)

    def test_point_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_point, values=7, properties=True)

    def test_text_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_text, values=34, properties=True)

    def test_building_markup(self, soup):
        self.assert_table_links_after_h(
            soup, parse_building, values=3, properties=True)
