from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, TextAreaField, FileField, \
    IntegerField, DecimalField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()], render_kw={'class': 'form-control'})
    pwd = PasswordField('密码', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('登录', render_kw={'class': "btn btn-info btn-lg btn-block"})


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()], render_kw={'class': 'form-control'})
    pwd = PasswordField('密码', validators=[DataRequired()], render_kw={'class': 'form-control'})
    re_pwd = PasswordField('确认密码', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('注册', render_kw={'class': "btn btn-info btn-lg btn-block"})


class GoodForm(FlaskForm):
    ID = IntegerField('编号')
    image = StringField('图片链接')
    name = StringField('商品名', render_kw={'class': 'form-control'})
    price = DecimalField('售价', render_kw={'class': 'form-control'})
    number = IntegerField('库存', render_kw={'class': 'form-control'})
    submit = SubmitField('添加商品', render_kw={'class': 'col-2 btn btn-primary'})


class EmailForm(FlaskForm):
    email = StringField('邮箱地址', validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control', 'placeholder': "请输入邮箱地址"})
    submit = SubmitField("确认", render_kw={'class': "btn btn-info btn-block"})
