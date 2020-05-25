# -*- coding: utf-8 -*-

import os
import sys

import pytest

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(TEST_DIR))

TEST_MARKUP_FILEPATH = os.path.join(TEST_DIR, "markup.html")

sys.path.append(ROOT)

from cartocss_doc_parser import (  # noqa: E402
    get_cartocss_doc_html,
    get_cartocss_doc_soup,
)


def before_start():
    if not os.path.exists(TEST_MARKUP_FILEPATH):
        with open(TEST_MARKUP_FILEPATH, "w", encoding="utf-8") as f:
            f.write(get_cartocss_doc_html())


@pytest.fixture(autouse=True, scope="session")
def setup():
    before_start()
    yield


@pytest.fixture
def soup():
    yield get_cartocss_doc_soup(url=TEST_MARKUP_FILEPATH)


@pytest.fixture
def html():
    yield get_cartocss_doc_html(url=TEST_MARKUP_FILEPATH)
