from __future__ import absolute_import, unicode_literals

import pymysql  # 导入第三方模块，用来操作mysql数据库

pymysql.version_info = (1, 4, 13, "final", 0)

pymysql.install_as_MySQLdb()

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)