
SECRET_KEY = "hukhnnjnks"

SERVER_NAME = "127.0.0.1:5000"

# 数据库配置信息
HOST = '127.0.0.1'
PORT =  3306
USER = 'root'
PASSWORD = 'abc123'
DATABASE = 'zhiliaohz'

DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PROT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "3110711143"
MAIL_PASSWORD = "qwpuaemhzffddccc"
MAIL_DEBUG = True
