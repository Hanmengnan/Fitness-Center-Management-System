from wtforms import fields , validators
from flask_wtf import FlaskForm


class loginForm(FlaskForm):
    username = fields.StringField(label=u'用户名' , validators=[validators.required()])
    password = fields.PasswordField(label=u'密码' , validators=[validators.required()])
    submit = fields.SubmitField(u'OK')


class registerForm(FlaskForm):
    username = fields.StringField(label=u'用户名' , validators=[validators.required()])
    customerid = fields.StringField(label=u'会员账号' , validators=[validators.required()])
    email = fields.StringField(label=u'电子邮箱' , validators=[validators.required()])
    password = fields.PasswordField(label=u'密码' , validators=[validators.required()])
    re_password = fields.PasswordField(label=u'密码' , validators=[validators.required()])
    register = fields.SubmitField(u'OK')


class profileForm(FlaskForm):
    cardid = fields.IntegerField(label=u'卡号')
    userid = fields.IntegerField(label=u'会员号')
    submit1 = fields.SubmitField(u'OK')

    day = fields.SelectField('请假时间' ,
                             choices=[(1 , '1') , (2 , '2') , (3 , '3') , (4 , '5') , (5 , '15') , (6 , '30')])
    submit2 = fields.SubmitField(u'OK')

    cardid3 = fields.IntegerField(label=u'卡号')
    submit3 = fields.SubmitField(u'OK')

    lessonid = fields.IntegerField(label=u'卡号')
    submit4 = fields.SubmitField(u'OK')


class authorityForm(FlaskForm):
    roleName = fields.StringField(label=u'会员号')
    query = fields.SubmitField(u'query')
    modify = fields.SubmitField(u'modify')
    c1 = fields.BooleanField("c1")
    c2 = fields.BooleanField("c2")
    c3 = fields.BooleanField("c3")
    c4 = fields.BooleanField("c4")
    c5 = fields.BooleanField("c5")
    c6 = fields.BooleanField("c6")
    c7 = fields.BooleanField("c7")
    c8 = fields.BooleanField("c8")
    c9 = fields.BooleanField("c9")
    c10 = fields.BooleanField("c10")
    c11 = fields.BooleanField("c11")
    c12 = fields.BooleanField("c12")

