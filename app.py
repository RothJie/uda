from flask import Flask,session,g

import config
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)  #绑定配置文件

db.init_app(app) #配置文件绑定app
migrate = Migrate(app, db)
"""
# ORM模型映射成表的三步zhou/  ,  ,
# 1.python -m flask db init         这步只需要执行一次 首先cd 当前目录
# 2.python -m flask db migrate      识别ORM模型的改变，生成迁移脚本
# 3.python -m flask db upgrade      运行迁移脚本，同步到数据库中
"""

@app.before_request
def my_before_request():
        user_id = session.get('id')
        if user_id:
                user = UserModel.query.get(user_id)
                setattr(g, 'user', user)
        else:
                setattr(g, 'user', None)

@app.context_processor
def my_context_processor():
        return {"user":g.user}
        # return dict(user=g.user)
app.register_blueprint(qa_bp)   # 绑定蓝图
app.register_blueprint(auth_bp) # # 绑定蓝图

mail.init_app(app)

if __name__ == '__main__':
        app.run(
                debug = True,
                host='0.0.0.0',
                port=5000
                )  # 不显示参数设置是因为pychrm识别成了Flask项目运行，而不是python项目，看运行时的图标即可。解决办法：新建一个python运行方案