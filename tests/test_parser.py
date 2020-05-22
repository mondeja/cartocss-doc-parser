# -*- coding: utf-8 -*-

import types

import pytest

import cartocss_doc_parser

PARAMETRIC = [
    ("symbolizers", 10, False),
    ("values", 9, False),
    ("other_parameters", 3, False),
    ("torque_properties", 7, True),
    ("common_elements", 3, True),
    ("map_background_and_string_elements", 4, True),
    ("polygon", 10, True),
    ("line", 18, True),
    ("markers", 21, True),
    ("shield", 34, True),
    ("line_pattern", 8, True),
    ("polygon_pattern", 10, True),
    ("raster", 9, True),
    ("point", 7, True),
    ("text", 34, True),
    ("building", 3, True),
]


class TestParser:
    @classmethod
    def setup_class(cls):
        cls.carto_css_data_types = list(
            cartocss_doc_parser.cartocss_data_types())

    def assert_link(self, url, contains=["#"]):
        self.assert_string(url)
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

    def assert_section_props(self, _values, values=5, properties=False):
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

    def assert_parser(self, soup, parser_func, values=5, properties=False):
        self.assert_section_props(
            parser_func(soup), values=values, properties=properties)

    @pytest.mark.parametrize("parser,values,properties", PARAMETRIC)
    def test_parser(self, soup, parser, values, properties):
        self.assert_parser(
            soup,
            getattr(cartocss_doc_parser, "parse_%s" % parser),
            values=values,
            properties=properties)

    def test_cartocss_doc(self):
        docs = cartocss_doc_parser.cartocss_doc()
        for attrname, values, properties in PARAMETRIC:
            self.assert_section_props(
                docs[attrname], values=values, properties=properties)
