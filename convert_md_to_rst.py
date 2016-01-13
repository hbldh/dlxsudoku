#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`register`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-01-13

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import pandoc

pandoc.core.PANDOC_PATH = "/usr/bin/pandoc"
doc = pandoc.Document()
doc.markdown = open('README.md') .read()
with open('README.rst', 'w') as f:
    f.write(doc.rst)



