# -*- coding: utf-8 -*-
import mysql.connector  # 导入数据库连接驱动
from sqlalchemy import create_engine  # 导入创建引擎
from sqlalchemy.orm import sessionmaker  # 创建会话工具
from config import DB_URI  # 导入连接配置


# 创建会话，操作数据表要通过会话操作
class ORM:
    @classmethod
    def db(cls):
        link = DB_URI
        # 创建连接引擎，encoding编码，echo是[True]否[False]输出日志
        engine = create_engine(
            link,
            echo=False,
            pool_size=100,
            pool_recycle=10,
            connect_args={'charset': "utf8"}
        )
        # 创建用于操作数据表的会话
        Session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )
        # autocommit，自动提交，True[开启]，False[关闭]，采用手动的方式，自己写事务处理的逻辑
        # autoflush，自动刷新权限，True[开启]
        return Session()
