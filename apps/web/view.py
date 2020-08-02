from flask import url_for , redirect , render_template
from flask_admin import helpers as admin_helpers
from flask_security import login_required , login_user , logout_user

from apps import admin
from . import web


@web.context_processor
def web_context_processor():
    return dict(
        admin_base_template=admin.base_template ,
        admin_view=admin.index_view ,
        get_url=url_for ,
        h=admin_helpers
    )


@web.route("/")
def init():
    return redirect(url_for('web.index'))


@web.route("/admin")
def index():
    return render_template('admin/mybase.html')


from apps.web.forms import *
from apps.model import User
from apps import db , user_datastore


@web.route('/login' , methods=['POST' , 'GET'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        print(form.username.data)
        if user is not None:
            if form.password.data == user.password:
                login_user(user)
                return redirect('/admin')

        return render_template('login/login.html' , form=form , m="用户名或密码错误")

    return render_template('login/login.html' , form=form , m="")


@web.route('/logout')
@login_required
def logout():
    logout_user()


@web.route('/register' , methods=['POST' , 'GET'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        re_password = form.re_password.data

        if password == re_password:
            role = user_datastore.find_role("user")
            user = user_datastore.create_user(name=username , email=email , password=password)
            user_datastore.add_role_to_user(user , role)
            db.session.commit()
            return redirect('/login')
        return render_template('login/register.html' , form=form , m="两次输入密码不一致")
    return render_template('login/register.html' , form=form , m="")
