import wtforms
from wtforms.validators import Email, length, EqualTo, email, input_required, InputRequired
from models import UserModel,EmailCaptchaModel


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    # captcha = wtforms.StringField(validators=[length(min=6, max=6,message='验证码格式错误')])
    username = wtforms.StringField(validators=[length(min=3, max=20,message='用户名不符合规范')])
    password = wtforms.StringField(validators=[length(min=6, max=20,message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="两次密码不一致！")])

    # 自定义验证
    def validate_email(self, field):
        """1邮箱是否已经被注册！"""
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # # 2.验证码是否正确
    # def validate_captcha(self, field):
    #     captcha = field.data
    #     email = self.email.data
    #     captcha_model = EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
    #     if not captcha_model:
    #         raise wtforms.ValidationError(message="邮箱或验证码错误！")

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[length(min=6, max=20, message="密码格式错误！")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3,max=100,message="标题格式错误！")])
    content = wtforms.StringField(validators=[length(min=3,message="内容格式有误！")])


class CommentForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=2,message="内容格式有误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题的id!")])


class SetInfoForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    username = wtforms.StringField(validators=[length(min=3, max=20, message='用户名不符合规范')])
    password = wtforms.StringField(validators=[length(min=6, max=20, message="密码格式错误！")])