from flask import Flask
from flask_security import SQLAlchemyUserDatastore , Security

app = Flask(__name__)
app.config.from_pyfile("config.py")

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

admin.add_view(LessonView(Lesson , db.session))
admin.add_view(VipCardView(VipCard , db.session))
admin.add_view(CoachView(Coach , db.session))
admin.add_view(CustomerView(Customer , db.session))
admin.add_view(UserView(User , db.session))
admin.add_view(leaveView(Leave , db.session))
