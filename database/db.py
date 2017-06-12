# _*_ coding: utf-8 _*_

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '******'
DB_DB   = 'raz'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                   (DB_USER, DB_PASS, DB_HOST, DB_DB),
                 encoding='utf-8', echo=False,
                   pool_size=100, pool_recycle=10)
