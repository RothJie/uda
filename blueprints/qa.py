import base64
import json

from flask import Blueprint, request, render_template, g, redirect, url_for, jsonify

from exts import db
from models import QuestionModel, CommentModel,UserQuestionStatusModel,StatusTotalViewModel
from .forms import QuestionForm, CommentForm
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")  # 首页采用根路径

@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    status_total = StatusTotalViewModel.query.all()
    return render_template('index.html',questions=questions,status_total=status_total)

@bp.route("/qa/public",methods=['GET', 'POST'])
@login_required # 使用闭包（自定义装饰器），解决代码冗余问题。
def public_question():
    # 如果没有登录则不能发表问答，直接跳转到首页；但是只适用于问答这一个界面，如果存在多个类似界面，不登录不能访问，
    # 则使用闭包（自定义装饰器），解决代码冗余问题。
    # if not g.user:
    #     return redirect('/')
    if request.method == 'GET':
        return render_template('pub_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/") #重定向，跳转到首页或详情页
        else:
            print(form.errors)
            return redirect(url_for('qa.public_question'))

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    if g.user:
        status_data = UserQuestionStatusModel.query.filter_by(question_id=qa_id,user_id=g.user.id).first()
        return render_template("detail.html",question=question,status_data=status_data)
    return render_template("detail.html",question=question)

@bp.route("/comment/public",methods=['GET', 'POST'])
@login_required  # 需要先登录才能进行评论，未登录和上面一样，直接跳转到登录页面，在装饰器中完成
def public_comment():
    form = CommentForm(request.form)  # 需要一个验证表单
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        comment = CommentModel(content=content,question_id=question_id,author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('qa.qa_detail',qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('qa.qa_detail',qa_id=request.form.get("question_id")))


@bp.route("/search",methods=['GET', 'POST'])
def search():
    """
    3种方式可以获取用户输入的关键字
    01./search?q=马斯克
    02./search/<q>
    03.post,request.form
    :return:
    """
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    status_total = StatusTotalViewModel.query.all()
    return render_template('index.html', questions=questions,status_total=status_total)

@bp.route("/qa/status_data",methods=['POST'])
def status_data():
    status = request.data   # b'{"user_id":"1","question_id":"3","isLiked":0,"isCommented":0,"isCollected":0}'
    status_data = json.loads(status.decode("utf-8"))
    u_i = status_data["user_id"]
    q_i = status_data["question_id"]
    user_status = UserQuestionStatusModel.query.filter_by(user_id=u_i, question_id=q_i).first()
    key3 = list(status_data.keys())[2]
    if user_status:
        # 这里不能直接使用user_status.key3 = status_data[key3] 原因是key3是字符串而不是字段
        if key3 == "isLiked":
            user_status.isLiked = status_data["isLiked"]
        elif key3 == "isCommented":
            user_status.isCommented = status_data["isCommented"]
        else:
            user_status.isCollected = status_data["isCollected"]
    else:
        user_status = UserQuestionStatusModel(isLiked=0,isCommented=0,isCollected=0,question_id=q_i,user_id=u_i)
        if key3 == "isLiked":
            user_status.isLiked = status_data["isLiked"]
        elif key3 == "isCommented":
            user_status.isCommented = status_data["isCommented"]
        else:
            user_status.isCollected = status_data["isCollected"]
        db.session.add(user_status)

    db.session.commit()
    return jsonify({"code":200,"message":None  ,"data":None})




