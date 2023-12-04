import pymysql
from .celery import app as celery_app

pymysql.install_as_MySQLdb()  # initialize Mysql
__all__ = ("celery_app",)  # initialize celery
