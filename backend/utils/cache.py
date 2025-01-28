# -*- coding: utf-8 -*-
# @Time    : 17-11-19 下午5:07
# @Author  : Pei Le
# @Email   : le.pei@easytransfer.cn
# @File    : redis_cache.py
# @Software: PyCharm
"""
redis 通用方法 简单版
"""
import redis
import pickle
import os

from django.conf import settings


class RedisConnection(object):

    def __init__(self, host=None, password=None, port=None, prefix='universal:', timeout=60, **kwargs):
        """
        初始化
        :param host: ip
        :param password: 密码
        :param port: 端口
        :param prefix: 缓存前缀
        :param timeout: 过期时间
        """
        try:
            self.timeout = timeout
            self.prefix = prefix
            pool = redis.ConnectionPool(host=host, password=password, port=port)
            self.redis = redis.Redis(connection_pool=pool)
        except Exception as e:
            self.redis = None
            raise ConnectionError('redis连接错误')

    def get_redis(self):
        return self.redis


redis_conn = RedisConnection(host=settings.REDIS_HOST, password=settings.REDIS_PASSWORD, port=settings.REDIS_PORT,
                             timeout=settings.REDIS_TIMEOUT)

class RedisHelper(object):
    def __init__(self, prefix='', timeout=60, **kwargs):
        """
        初始化
        :param host: ip
        :param password: 密码
        :param port: 端口
        :param prefix: 缓存前缀
        :param timeout: 过期时间
        """
        self.redis = redis_conn.get_redis()
        self.timeout = timeout
        self.prefix = prefix

    def set(self, key=None, value=None, timeout=None, **kwargs):
        """
        设置缓存 不安全  存在就更新，不存在就设置
        :param key: key
        :param value: 值
        :param timeout: 过期时间 秒
        :return: bool
        """
        timeout = timeout if timeout is not None else self.timeout
        if key is not None and value is not None and type(key) == str:
            name = self.prefix + key
            if self.get(key) is not None:
                nx, xx = False, True
            else:
                nx, xx = True, False
            return self.redis.set(name=name, value=pickle.dumps(value), ex=timeout, nx=nx, xx=xx)
        return False
    
    def record_new_set_data(self, key):
        record_need_sync_redis_key = 'need_sync_redis_key_list'
        exist_need_sync_key_list = self.lrange(record_need_sync_redis_key, 0, -1)
        if key.encode('utf-8') not in exist_need_sync_key_list:
            self.redis.lpush(record_need_sync_redis_key, key)


    def set_safe(self, key=None, value=None, timeout=None, update=False, **kwargs):
        """
        设置缓存 安全 更新必须将update 设置为True 否则无法更新  添加 update为False
        :param key: key
        :param value: 值
        :param timeout: 过期时间
        :param update: 是否更新
        :return: bool
        """
        timeout = timeout if timeout and timeout > 0 else self.timeout
        nx = not update
        xx = update
        if key is not None and value is not None and type(key) == str:
            name = self.prefix + key
            value = pickle.dumps(value)
            return self.redis.set(name=name, value=value, ex=timeout, nx=nx, xx=xx)
        return False

    def get(self, key=None, **kwargs):
        """
        获得缓存key值
        :param key:key
        :return: object 没有为None
        """
        if key is not None and type(key) == str:
            name = self.prefix + key
            result = self.redis.get(name)
            return pickle.loads(result) if result is not None else None
        return None

    def delete(self, key=None, *argv, **kwargs):
        """
        删除缓存key
        :param key: key
        :return: bool
        """
        if key is not None and type(key) == str:
            name = self.prefix + key

            if not kwargs.get('is_partial'):
                return True if self.redis.delete(name) == 1 else False

            # 模糊搜索后判断删除
            partial_key_list = self.redis.keys(f'*{name}*')
            if not partial_key_list:
                return False
            return True if self.redis.delete(*partial_key_list) >= 1 else False
        return False


    def get_timeout(self, key=None, **kwargs):
        """
        获得key过期时间
        :param key:
        :return: 过期或者没有返回0
        """
        if key is not None:
            name = self.prefix + key
            timeout = self.redis.ttl(name)
            return timeout if timeout is not None and timeout > 0 else 0
        return 0

    def refresh_timeout(self, key=None, timeout=None, **kwargs):
        """
        刷新过期时间
        :param key: key
        :param timeout: 过期时间
        :return: bool
        """
        timeout = timeout if timeout and timeout > 0 else self.timeout
        if key is not None:
            name = self.prefix + key
            return self.redis.expire(name=name, time=timeout)
        return False

    def lpush(self, key, value):
        """
        list类型push
        :param key:
        :param value: list, tuple
        :return:
        """
        self.redis.lpush(key, value)
    
    def rpop(self, key):
        """
        把队列最右端的值弹出
        """
        return self.redis.rpop(key)
        

    def rpoplpush(self, old_key, new_key):
        """将链表old_key的尾部元素取出放到链表new_key的头部,并返回该元素"""
        return self.redis.rpoplpush(old_key, new_key)

    def lrange(self, key, start, end):
        return self.redis.lrange(key, start, end)

    def set_no_time(self, key=None, value=None, **kwargs):
        """
        设置永久缓存
        :param key: key
        :param value: 值
        :param timeout: 过期时间 秒
        :return: bool
        """
        if key is not None and value is not None and type(key) == str:
            name = self.prefix + key
            return self.redis.set(name=name, value=pickle.dumps(value))
        return False


cache = RedisHelper()