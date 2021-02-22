from settings.base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = True

ALLOWED_HOSTS = ["*"]

# 务必修改以下值，确保运行时系统安全:
SECRET_KEY = "w$46bks+b3-7f(13#i%v@jwejrnxc$^^#@#@^t@fofizy1^mo9r8(-939243423300"

# 如果仅使用数据库中的账号，以下 LDAP 配置可忽略
# 替换这里的配置为正确的域服务器配置，同时可能需要修改 base.py 中的 LDAP 服务器相关配置:
LDAP_AUTH_URL = "ldap://xxxxx:389"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "your_admin_credentials"

INSTALLED_APPS += (
    # other apps for production site
)

# 钉钉群的 WEB_HOOK， 用于发送钉钉消息
DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxxxx"


sentry_sdk.init(
    dsn="http://3b3982614bb24441aeeb6b0af0886dc1@172.25.17.134:9000/2",
    integrations=[DjangoIntegration()],
    # 采样率，生产环境访问量过大时建议调小，不用每一个URL都记录性能
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.25.17.134:6380/1",
        "TIMEOUT": 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "",
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds    连接超时时间
            "SOCKET_TIME": 5,     # r/w timeout in seconds    每次读写数据超时时间
        }
    }
}

CELERY_BROKER_URL = 'redis://172.25.17.134:6380/0'
CELERY_RESULT_BACKEND = 'redis://172.25.17.134:6380/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")