#!/usr/bin/env python
# coding=utf-8

import redis
import json

def singleton(cls, *args, **kwargs):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

@singleton
class RedisClient(object):

    __redis_server = redis.StrictRedis(host='192.168.2.80', port=6379, db=0)

    def get(self, key):
        return self.__redis_server.get(key)

    def set(self, key, value):
        return self.__redis_server.set(key, value)

    def rpush(self, key, value):
        return __redis_server.rpush(key, value)

    def mrpush(self, key, values):
        with self.__redis_server.pipeline(False) as pipe:
            for v in value:
                self.__redis_server.rpush(key, v)
        ret = pipe.execute()
        return ret

    def lrange(self, key, l, r):
        return self.__redis_server.lrange(key, l, r)

    def llen(self, key):
        return self.__redis_server.llen(key)

    def lrm(self, key, value):
        return self.__redis_server.lrem(key, 0, value)

@singleton
class InspectingTaskPool(object):

    __prefix = "inspect"

    def __make_key(self, key):
        return "%s&%s" % (self.__prefix, key)
    
    def __init__(self):
        self.__client = RedisClient()

    def __getShare(self, category):
        k = "share&%s" % category
        key = self.__make_key(k)
        v = self.__client.get(key)
        return v.split(',')

    def __setShare(self, category, ids):
        k = "share&%s" % category
        key = self.__make_key(k)
        v = ','.join(ids)
        self.__client.set(key, v)

    def pushToPool(self, category, datas):
        k = "task&%s" % category
        key = self.__make_key(k)
        return self.__client.rpush(key, datas)

    def __getFromList(self, dtas, cnt):
        match_ids = []
        match_data = []
        match_count = 0
        for data in datas:
            data_dict = json.loads(data)
            id = data_dict.get("id")
            if id not in share_ids:
                match_ids.append(id)
                match_data.append(data_dict)
                match_count += 1
            if match_count >= cnt:
                break

        return match_data, match_ids
        
    def getFromPool(self, category, count=10):
        key = "task&%s" % category
        key = self.__make_key(key)
        pool_data = self.__client.lrange(key, 0, count * 10)
        share_ids = self.__getShare(category)
        
        match_data, match_ids = self.__getFromList(pool_data, count)

        more_lens = count - len(match_ids)
        if more_lens:
            llen = self.__cleint.llen(key)
            all_data = self.__client.lrange(key, 0, llen)
            more_data, more_ids = self.__getFromList(all_data, more_lens)

        self.__setShare(category, match_ids + more_ids)
        
        return match_data + more_data        

    def processTask(self, category, data):
        task_key = "task&%s" % category
        task_key = self.__make_key(task_key)
        self.__client.lrem(task_key, data)
        self.__removeShare(category, data)

    def __removeShare(self, category, data):
        share_key = "share&%s" % category
        share_key = self.__make_key(share_key)
        ids = self.__client.get(share_key)
        ids = ids.split(",")
        id = json.loads(data).get("id")
        ids.remove(id)
        self.__client.set(",".join(ids))

    def giveTask(self, category, data):
        self.__removeShare(category, data)


@singleton
class MaterielTaskPool(InspectingTaskPool):

    __prefix = "materiel"

@singleton
class ProcessingTaskPool(InspectingTaskPool):

    __prefix = "processing"

@singleton
class FeedingTaskPool(InspectingTaskPool):

    __prefix = "feeding"

@singleton
class BarrelTaskPool(InspectingTaskPool):

    __prefix = "barrel"

@singleton
class AssembleTaskPool(InspectingTaskPool):

    __prefix = "assemble"

@singleton
class PressureTaskPool(InspectingTaskPool):

    __prefix = "pressure"

@singleton
class FacadeTaskPool(InspectingTaskPool):

    __prefix = "facade"
