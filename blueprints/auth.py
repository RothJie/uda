import random
import string
import asyncio
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, g
from blueprints.forms import RegisterForm, LoginForm, SetInfoForm
from decorators import login_required
from models import EmailCaptchaModel, UserModel
from exts import mail, db, Profile
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/login", methods=['GET', 'POST'])  # /auth/login
def login():
    if request.method == "GET":
        print("Before redirect, url4512:", url_for("auth.login"))  # 打印生成的 URL
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("没有找到该用户的邮箱！请重新登录或移步到注册页面！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # 让浏览器记住网站的cookie,flask中的session是经过加密存储在cookie中的
                session["id"] = user.id  # 在config中设置盐SECRET_KEY。这里设置好以后就是全局都可以使用，但要注意名称一致
                return redirect('/')  # 跳转到首页
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# @bp.route("/register",methods=["GET","POST"])
# def register():
#     if request.method == "GET":
#         return render_template("register.html")
#     else:
#         form = RegisterForm(request.form)
#         if form.validate():
#             email = form.email.data
#             username = form.username.data
#             password = form.password.data
#             user = UserModel(email=email,name=username,password=generate_password_hash(password))
#             db.session.add(user)  # 保存数据
#             db.session.commit()
#             return jsonify({"code":200, "message":None, "data":{"email":email}})
#         else:
#             print(form.errors)
#             return redirect(url_for('register'))


@bp.route("/register", methods=["GET", "POST"])  # 优化之后的
def register():
    try:
        if request.method == "GET":
            return render_template("register.html")
        else:
            form = RegisterForm(request.form)
            if form.validate():
                email = form.data.get("email")
                username = form.data.get("username")
                password = form.data.get("password")
                user = UserModel(email=email, name=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                return jsonify({"code": 200, "data": {"email": email}})
            else:
                print(form.errors)
                return render_template("register.html")  # 显示错误信息

    except Exception as e:
        print(f'Exception occurred: {str(e)}')
        return render_template("register.html")


@bp.route("/captcha/email")  # /captcha/email?email=2847832624@qq.com
def get_email_captcha():
    email = request.args.get("email")  # 通过请求获取用户的邮箱
    captcha = "".join([random.choice(string.digits) for _ in range(6)])  # 通过列表推导式实现一个6位数的验证码
    message = Message(subject="知了传课邮箱验证码", sender="3110711143@qq.com", recipients=[email],
                      body=f"您的验证码是：{captcha}")
    mail.send(message)
    # 用数据库存储验证码
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "请求成功！", "data": None})


@bp.route("/set_info", methods=["GET", "POST"])
@login_required
def set_info():
    if request.method == "GET":
        return render_template("user_info_set.html")
    else:
        form = SetInfoForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(id=g.user.id).first()
            user.email = email
            user.name = username
            user.password = generate_password_hash(password)
            db.session.commit()
            session.clear()
        return redirect(url_for("auth.login"))


@bp.route("/register/submit_avatar", methods=["POST"])
def submit_avatar():
    email = request.form.get("email")
    imageFile = request.files.get("imageFile")
    if imageFile:
        image_filename = secure_filename(imageFile.filename)
        user = UserModel.query.filter_by(email=email).first()
        user.avatar_url = "images/{}".format(image_filename)
        db.session.commit()
        image_path = Profile.get_images_path()
        full_path = image_path.joinpath(image_filename)
        imageFile.save(full_path)
    return redirect(url_for("auth.login"))

@bp.route("/upload_user_avatar", methods=["POST"])
@login_required
def upload_user_avatar():
    imageFile = request.files.get("imageFile")
    if imageFile:
        image_filename = secure_filename(imageFile.filename)
        image_path = Profile.get_images_path()
        full_path = image_path.joinpath(image_filename)
        imageFile.save(full_path)
        user = UserModel.query.filter_by(id=g.user.id).first()
        user.avatar_url = "images/{}".format(image_filename)
        db.session.commit()
        session.clear()
    # return redirect(url_for("auth.login"))
