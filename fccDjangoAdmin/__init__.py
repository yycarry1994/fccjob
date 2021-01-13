import pymysql  # 导入第三方模块，用来操作mysql数据库

pymysql.version_info = (1, 4, 13, "final", 0)

pymysql.install_as_MySQLdb()
