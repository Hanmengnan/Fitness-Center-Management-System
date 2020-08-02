from wtforms import fields , validators
from flask_wtf import FlaskForm


class loginForm(FlaskForm):
    username = fields.StringField(label=u'用户名' , validators=[validators.required()])
    password = fields.PasswordField(label=u'密码' , validators=[validators.required()])

    submit = fields.SubmitField(u'OK')


class registerForm(FlaskForm):
    username = fields.StringField(label=u'用户名' , validators=[validators.required()])
    email = fields.StringField(label=u'电子邮箱' , validators=[validators.required()])
    password = fields.PasswordField(label=u'密码' , validators=[validators.required()])
    re_password = fields.PasswordField(label=u'密码' , validators=[validators.required()])

    register = fields.SubmitField(u'OK')
