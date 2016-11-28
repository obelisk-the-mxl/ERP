#!/usr/bin/env python
# coding=utf-8

import os
import sys

_CUR_DIR = os.path.split(os.path.realpath(__file__))[0]
_PYRPC_DIR = os.path.join(_CUR_DIR, "..", "..", "..")

sys.path.append(_PYRPC_DIR)

from pyrpc.client import ThriftClient
from pyrpc.thrift_gen.inspect.InspectService import InspectService

class InspectServiceBase(object):
    def __init__(self, **kwargs):
        self.client = ThriftClient(InspectService, **kwargs)

    def __getattr__(self, name):
        return getattr(self.client, name)
