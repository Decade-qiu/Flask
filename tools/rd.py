# -*- coding: utf-8 -*-
import redis  # 连接驱动
from config import redis_configs

# 连接池
pool = redis.ConnectionPool(**redis_configs)

# 连接对象
rd = redis.Redis(connection_pool=pool)
