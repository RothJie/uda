from datetime import datetime

from boltons.iterutils import unique

from exts import db

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False,unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    avatar_url = db.Column(db.String(255), nullable=True)  # 用于存储头像访问地址，允许为空

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(25), nullable=False)
    captcha = db.Column(db.String(20), nullable=False)

class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    #外键
    author_id = db.Column(db.Integer,db.ForeignKey("user.id")) # 作者id与用户id一致，即创建问题的作者id关联用户id
    # 关系  backref 反向引用
    # 当UserModel创建一个对象时，也就是有一个author时，可以通过反向引用的方式拿到该作者所有的提过的问题questions
    author = db.relationship(UserModel,backref="questions")  # 搭建一个用户表user即UserModel与question表的桥梁

class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))  # 对哪一个问题进行评论
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))  # 被评论的问题有谁发布的

    # 关系
    # 当QuestionModel创建一个对象时，也就是有一个question时，可以通过反向引用的方式拿到问题所有的评论comments
    question = db.relationship(QuestionModel,backref=db.backref('comments',order_by = create_time.desc()))
    # 当UserModel创建一个对象时，也就是有一个author时，可以通过反向引用的方式拿到该作者所有的评论comments
    author = db.relationship(UserModel,backref="comments")

class UserQuestionStatusModel(db.Model):
    __tablename__ = 'user_question_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isLiked = db.Column(db.Integer,nullable=False)
    isCommented = db.Column(db.Integer,nullable=False)
    isCollected = db.Column(db.Integer,nullable=False)
    # 外键
    question_id = db.Column(db.Integer,db.ForeignKey("question.id")) # 点赞评论收藏的状态关于哪一个问题的
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 点赞评论收藏的状态由谁操作的
    # 关系
    # 当UserQuestionStatusModel创建一个对象时，也就是有一个status时，可以通过反向引用的方式拿到问题所有的关于点赞评论收藏的状态
    question = db.relationship(QuestionModel, backref=db.backref('user_question_statuses'))
    # 当UserQuestionStatusModel创建一个对象时，也就是有一个status时，可以通过反向引用的方式拿到该作者所有对所有问题的状态
    author = db.relationship(UserModel, backref="user_question_statuses")

class StatusTotalViewModel(db.Model):
    __tablename__ = 'status_total_view'   # 这里映射的是状态总数视图
    question_id = db.Column(db.Integer,primary_key=True)
    like_t = db.Column(db.Integer,nullable=False)
    comment_t = db.Column(db.Integer,nullable=False)
    collect_t = db.Column(db.Integer,nullable=False)
    __mapper_args__ = {'eager_defaults':True}
"""
# ORM模型映射成表的三步zhou/  ,  ,
# 1.python -m flask db init         这步只需要执行一次 首先cd 当前目录 用来生成迁移文件
# 2.python -m flask db migrate      识别ORM模型的改变，生成迁移脚本
# 3.python -m flask db upgrade      运行迁移脚本，同步到数据库中
"""