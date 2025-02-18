# -*- coding: utf-8 -*-
# @Time    : 17-11-19 下午5:07
# @Author  : Pei Le
# @Email   : le.pei@easytransfer.cn
# @File    : redis_cache.py
# @Software: PyCharm
"""
redis 通用方法 简单版
"""
import json
import redis.asyncio as sync_redis
import redis  # 使用同步版的redis
from django.conf import settings


class SyncRedisHelper:
    def __init__(self, host='localhost', port=6379, password=None, db=0, prefix='', timeout=60):
        """
        初始化 Redis 连接池
        :param host: Redis 主机
        :param port: Redis 端口
        :param db: Redis 数据库索引
        :param prefix: 缓存前缀
        :param timeout: 默认过期时间（秒）
        """
        self.prefix = prefix
        self.timeout = timeout

        # 创建 Redis 连接池
        self.redis = sync_redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True,
        )
        if self.redis.ping():
            print('连接redis成功')
        else:
            print('连接redis失败')

    async def set(self, key, value, timeout=None):
        """
        设置 Redis 键值，支持自动刷新值和过期时间
        :param key: 键
        :param value: 值
        :param timeout: 过期时间，秒
        :return: 操作结果
        """
        timeout = timeout if timeout else self.timeout
        name = self.prefix + key
        # 设置键值对，支持自动刷新的过期时间
        if await self.get(key) is not None:
            nx, xx = False, True
        else:
            nx, xx = True, False
        result = await self.redis.set(name, self.serializer_value(value=value), ex=timeout, nx=nx, xx=xx)
        return result

    async def get(self, key):
        """
        获取 Redis 键值
        :param key: 键
        :return: 值
        """
        name = self.prefix + key
        result = await self.redis.get(name)
        if result:
            return json.loads(result)  # 反序列化
        return None

    async def get_timeout(self, key):
        """
        获取 Redis 键的过期时间
        :param key: 键
        :return: 过期时间（秒）
        """
        name = self.prefix + key
        timeout = await self.redis.ttl(name)
        return timeout if timeout > 0 else 0

    async def refresh_timeout(self, key, timeout=None):
        """
        刷新 Redis 键的过期时间
        :param key: 键
        :param timeout: 新的过期时间，秒
        :return: 操作结果
        """
        timeout = timeout if timeout else self.timeout
        name = self.prefix + key
        return await self.redis.expire(name, timeout)

    @staticmethod
    def should_pickle(value):
        if isinstance(value, (int, float, str, bool, type(None))):
            return False
        return True
    
    def serializer_value(self, value):
        if self.should_pickle(value):
            return json.dumps(value)
        return value
    



# 使用示例




class RedisHelper:
    def __init__(self, host='localhost', port=6379, password=None, db=0, prefix='', timeout=60):
        """
        初始化 Redis 连接池
        :param host: Redis 主机
        :param port: Redis 端口
        :param db: Redis 数据库索引
        :param prefix: 缓存前缀
        :param timeout: 默认过期时间（秒）
        """
        self.prefix = prefix
        self.timeout = timeout

        # 创建 Redis 连接池
        self.redis = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True,
        )
        if self.redis.ping():
            print('连接redis成功')
        else:
            print('连接redis失败')

    def set(self, key, value, timeout=None):
        """
        设置 Redis 键值，支持自动刷新值和过期时间
        :param key: 键
        :param value: 值
        :param timeout: 过期时间，秒
        :return: 操作结果
        """
        timeout = timeout if timeout else self.timeout
        name = self.prefix + key
        # 设置键值对，支持自动刷新的过期时间
        if self.get(key) is not None:
            nx, xx = False, True
        else:
            nx, xx = True, False
        result = self.redis.set(name, self.serializer_value(value=value), ex=timeout, nx=nx, xx=xx)
        return result

    def get(self, key):
        """
        获取 Redis 键值
        :param key: 键
        :return: 值
        """
        name = self.prefix + key
        result = self.redis.get(name)
        if result:
            return json.loads(result)  # 反序列化
        return None

    def get_timeout(self, key):
        """
        获取 Redis 键的过期时间
        :param key: 键
        :return: 过期时间（秒）
        """
        name = self.prefix + key
        timeout = self.redis.ttl(name)
        return timeout if timeout > 0 else 0

    def refresh_timeout(self, key, timeout=None):
        """
        刷新 Redis 键的过期时间
        :param key: 键
        :param timeout: 新的过期时间，秒
        :return: 操作结果
        """
        timeout = timeout if timeout else self.timeout
        name = self.prefix + key
        return self.redis.expire(name, timeout)

    @staticmethod
    def should_pickle(value):
        if isinstance(value, (int, float, str, bool, type(None))):
            return False
        return True
    
    def serializer_value(self, value):
        if self.should_pickle(value):
            return json.dumps(value)
        return value


# 使用示例
# sync_cache = SyncRedisHelper(host=settings.REDIS_HOST, password=settings.REDIS_PASSWORD, port=settings.REDIS_PORT, db=0)
cache = RedisHelper(host=settings.REDIS_HOST, password=settings.REDIS_PASSWORD, port=settings.REDIS_PORT, db=0)


