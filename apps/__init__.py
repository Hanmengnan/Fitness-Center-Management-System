from flask import Flask
from flask_security import SQLAlchemyUserDatastore , Security

app = Flask(__name__)
app.config.from_pyfile("config.py")

from flask_babelex import Babel

babel = Babel(app)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)

from flask_admin import Admin

admin = Admin(app , name="健身中心管理系统" ,
              template_mode="bootstrap3" , base_template="admin/mybase.html")

from apps.model import *

user_datastore = SQLAlchemyUserDatastore(db , User , Role)
security = Security(app , user_datastore)

from apps.web import web

app.register_blueprint(web)

from apps.modelview import *

admin.add_view(LessonView(Lesson , db.session , name="课程管理"))
admin.add_view(VipCardView(VipCard , db.session , name="会员卡管理"))
admin.add_view(CoachView(Coach , db.session , name="教练管理"))
admin.add_view(CustomerView(Customer , db.session , name="顾客管理"))
admin.add_view(UserView(User , db.session , name="用户管理"))
admin.add_view(leaveView(Leave , db.session , name="请假管理"))
