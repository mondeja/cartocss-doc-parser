# -*- coding: utf-8 -*-

import hashlib


def test_doc_content_md5(html):
    hash_md5 = hashlib.md5(html.encode("utf-8"))
    assert hash_md5.hexdigest() == "5d27e2a724aa8e6708e8d00c89f4d107"
