# -*- coding: utf-8 -*-

import os
import hashlib


def test_doc_content_md5(html):
    hash_md5 = hashlib.md5(html.encode("utf-8"))
    assert hash_md5.hexdigest() == "60b7b01ab44061426aef0c695a689b33"


def test_doc_content_diff(html):
    markup_lines = html.splitlines()

    with open(os.path.join("tests", "expected-markup.html")) as f:
        expected_markup_lines = f.read().splitlines()

    line_iterator = enumerate(zip(markup_lines, expected_markup_lines))
    for i, (line, expected_line) in line_iterator:
        msg_schema = "Difference in line number %d.\nEXPECTED: %s\nFOUND: %s"

        _line, _el = (line.strip(" ").strip("\t"),
                      expected_line.strip(" ").strip("\t"))
        assert _line == _el, msg_schema % (i+1, expected_line, line)
