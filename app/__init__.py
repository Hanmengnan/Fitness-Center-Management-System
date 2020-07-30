from flask_admin import Admin

from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("config.py")

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)

admin = Admin(app , name="健身中心管理系统" ,
              template_mode="bootstrap3" , base_template="admin/mybase.html")

from flask_security import Security , SQLAlchemyUserDatastore , UserMixin , RoleMixin , login_required , current_user
from app.model import *

user_datastore = SQLAlchemyUserDatastore(db , User , Role)
security = Security(app , user_datastore)



from app.views import *
from app import route

admin.add_view(ModelView(Customer , db.session))
admin.add_view(ModelView(Coach , db.session))
admin.add_view(ModelView(Lesson , db.session))
