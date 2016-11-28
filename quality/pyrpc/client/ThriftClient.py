#!/usr/bin/env python
# coding=utf-8

import functools
import time

from thrift.transport import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol

class ThriftClient(object):
    def __init__(self, modual, **kwargs):
        self.retry_times = kwargs.get("retry_times", 3)
        self.retry_interval = kwargs.get("retry_interval", 1)
        self.host = kwargs.get("host", 'localhost')
        self.port = kwargs.get("port", 4999)
        self.timeout = kwargs.get("timeout", 3)
        
        self.client_class = modual.Client

    def open(self):
        retried_times = 0
        start_ts = time.time()
        while True:
            try:
                return self._connect()
            except Exception, e:
                current_seconds = time.time() - start_ts
                retried_times += 1
                if current_seconds > self.timeout or retried_times > self.retry_times:
                    raise e

    def close(self):
        if not self.transport:
            return
        try:
            self.transport.close()
        except Exception, e:
            print e
        finally:
            self.transport = None


    def _connect(self):
        self.transport = TSocket(self.host, self.port)
        self.transport = TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol(self.transport)

        self.client = self.client_class(self.protocol)
        
        self.transport.open()


    def __getattr__(self, name):

        def wrapper(self, *args, **kwargs):
            
            func = getattr(self.client, name)

            while True:
                try:
                    self.open()
                    ret = func(args, kwargs)
                    return ret
                except:
                    if self.retry_interval:
                        time.sleep(float(self.retry_interval))
                finally:
                    self.close()

        return functools.partial(wrapper, self)
