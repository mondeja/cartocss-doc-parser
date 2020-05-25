# -*- coding: utf-8 -*-

import os
import hashlib


def test_doc_content_md5(html):
    hash_md5 = hashlib.md5(html.encode("utf-8"))
    assert hash_md5.hexdigest() == "5d27e2a724aa8e6708e8d00c89f4d107"


def test_doc_content_diff(html):
    markup_lines = html.splitlines()

    with open(os.path.join("tests", "expected-markup.html")) as f:
        expected_markup_lines = f.read().splitlines()

    line_iterator = enumerate(zip(markup_lines, expected_markup_lines))
    for i, (line, expected_line) in line_iterator:
        msg_schema = "Difference in line number %d.\nEXPECTED: %s\nFOUND: %s"
        assert expected_line == line, msg_schema % (i+1, expected_line, line)
