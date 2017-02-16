#!/usr/bin/env python
# coding=utf-8

from quality.pyrpc.service import InspectService
from quality.pyrpc.thrift_gen.inspect.constants import *



class InspectIface(object):
    
    INTERNAL_SERVER_ERR = 1
    ILLEGAL_PARAM = 2

    class ErrResponse(object):
        def __init__(self, errno=0, errmsg=""):
            self.errno = errno
            self.errmsg = errmsg

        def __rper__(self):
            l = ['%s=%r' % (key, value) for key, value in self.__dict__.iteritems()]
            return "%s(%s)" % (self.__class__.__name__, ','.join(l))

    def __init__(self):
        self.client = InspectService(host='192.168.2.81')

    def __get_err_response(self, errno, errmsg=""):
        return ErrResponse(errno, errmsg)

    def create_item(work_order_id, category, index):
        try:
            if not work_order_id or not category or not index:
                return self.__get_err_response(self.ILLEGAL_PARAM)
            if not self.client:
                return self.__get_err_response(self.INTERNAL_SERVER_ERR)
            req = CreateBaseItemReq(work_order_id=work_order_id, cate=category, index=index)
            resp = self.client.create_item(req)
        except Exception, e:
            return self.__get_err_response(self.INTERNAL_SERVER_ERR, str(e))
        return resp

    def update_item(itemid, status, userId, checkDate, extra):
        try:
            if not itemid:
                return self.__get_err_response(self.ILLEGAL_PARAM)
            if not self.client:
                return self.__get_err_response(self.INTERNAL_SERVER_ERR)
            req = UpdateItemReq(itemid=itemid, status=status, usrId=userId, checkDate=checkDate, extra=extra)
            resp = self.client.updateItem(req)
        except Exception, e:
            return self.__get_err_response(self.INTERNAL_SERVER_ERR, str(e))
        return resp
    
    def get_inspect_report(work_order_id, category):
        try:
            if not work_order_id or not category:
                return self.__get_err_response(self.ILLEGAL_PARAM)
            if not self.client:
                return self.__get_err_response(self.INTERNAL_SERVER_ERR)
            req = GetInspectReportReq(work_order_id=work_order_id, categories=[category])
            resp = self.client.get_inspect_report(req)
        except Exception, e:
            return self.__get_err_response(self.INTERNAL_SERVER_ERR, str(e))
        return resp

    def mget_item_by_ids(item_ids):
        try:
            if not item_ids:
                return self.__get_err_response(self.ILLEGAL_PARAM)
            if not self.client:
                return self.__get_err_response(self.INTERNAL_SERVER_ERR)
            req = MgetByIdsReq(item_ids=item_ids)
            resp = self.client.mget_by_ids(req)
        except Exception, e:
            return self.__get_err_response(self.INTERNAL_SERVER_ERR, str(e))
        return resp

    def mget_item_by_workorder(work_order_id, categories):
        try:
            if not work_order_id or not categories:
                return self.__get_err_response(self.ILLEGAL_PARAM)
            if not self.client:
                return self.__get_err_response(self.INTERNAL_SERVER_ERR)
            req = MgetItemByWorkOrderReq(req)
            resp = self.client.mget_by_workorder(req)
        except Exception, e:
            return self.__get_err_response(self.INTERNAL_SERVER_ERR, str(e))
        return resp
