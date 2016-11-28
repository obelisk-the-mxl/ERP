#!/usr/bin/env python
# coding=utf-8

import os
import sys

_CUR_DIR = os.path.split(os.path.realpath(__file__))[0]
_PYRPC_DIR = os.path.join(_CUR_DIR, "..", "..")

sys.path.append(_PYRPC_DIR)

from pyrpc.thrift_gen.inspect.ttypes import *
from pyrpc.thrift_gem.inspect.constants import *
from pyrpc.service.inspect import InspectServiceBase

class InspectService(InspectServiceBase):
    def __init__(self, **kwargs):
        super(InspectServiceBase, self).__init__(**kwargs)
