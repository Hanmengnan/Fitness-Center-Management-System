from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from flask_security import current_user , roles_required

from flask import redirect , url_for , render_template , request


class MyBaseModelView(ModelView):
    column_display_pk = True
    can_set_page_size = True
    can_view_details = True
    page_size = 10

    def is_accessible(self):
        from apps import user_datastore
        admin = user_datastore.find_role("admin")
        if current_user.has_role(admin):
            self.edit_modal = True
            self.create_modal = True
            self.details_modal = True
            self.can_edit = True
            self.can_export = True
            self.can_delete = True
        else:
            self.edit_modal = False
            self.create_modal = False
            self.details_modal = False
            self.can_edit = False
            self.can_export = False
            self.can_delete = False
        return current_user.is_authenticated

    def inaccessible_callback(self , name , **kwargs):
        return redirect(url_for('web.login' , next=request.url))


class AdminView(ModelView):
    column_display_pk = True
    can_set_page_size = True
    can_view_details = True
    page_size = 10

    def is_accessible(self):
        from apps import user_datastore
        admin = user_datastore.find_role("admin")
        if current_user.has_role(admin):
            if current_user.has_role(admin):
                self.edit_modal = True
                self.create_modal = True
                self.details_modal = True
                self.can_edit = True
                self.can_export = True
                self.can_delete = True
        else:
            return False
        return current_user.is_authenticated

    def inaccessible_callback(self , name , **kwargs):
        from apps.web import loginForm
        form = loginForm()
        return render_template('login/login.html' , form=form , m="您没有权限，请重新登陆后尝试")


class CustomerView(AdminView):
    column_auto_select_related = True
    column_searchable_list = ("name" , "adress" , "sid" , "phoneNumber")


class CoachView(MyBaseModelView):
    column_auto_select_related = True
    column_searchable_list = ("name" , "nation" , "political" , "education" , "phoneNumber" , "job" ,
                              "school")


class LessonView(MyBaseModelView):
    column_auto_select_related = True

    column_searchable_list = (
        "lessonName" , "lessonData" , "room" , "coach")


class UserView(AdminView):
    column_auto_select_related = True

    column_searchable_list = (
        "id" , "name" , "email")
    column_list = ("id" , "name" , "email")


class VipCardView(MyBaseModelView):
    column_auto_select_related = True
    column_searchable_list = (
        "name" , "price" , "discount")