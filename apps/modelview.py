from flask import redirect , url_for , render_template , request
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from apps.model import Authority

from apps import user_datastore
from apps.web import loginForm


class MyBaseModelView(ModelView):
    column_display_pk = True
    can_edit = True
    can_export = True
    can_delete = True
    can_create = True
    can_view_details = True
    edit_modal = True
    create_modal = True
    details_modal = True
    column_auto_select_related = True
    can_set_page_size = True
    page_size = 10

    def inaccessible_callback(self , name , **kwargs):
        form = loginForm()
        return render_template('login/login.html' , form=form , m="您没有权限，请重新登陆后尝试")


class AdminView(ModelView):
    column_display_pk = True
    can_set_page_size = True
    can_view_details = True
    page_size = 10
    details_modal = True
    edit_modal = True
    create_modal = True

    def is_accessible(self):
        from apps import user_datastore
        admin = user_datastore.find_role("admin")
        if not current_user.is_anonymous:
            if current_user.has_role(admin):
                self.create_modal = True
                self.can_edit = True
                self.can_export = True
                self.can_delete = True
        else:
            return False
        return current_user.is_authenticated


class CustomerView(MyBaseModelView):
    column_searchable_list = ("name" , "adress" , "sid" , "phoneNumber")

    def is_accessible(self):
        role = current_user.roles[0].name
        if not current_user.is_anonymous:
            userAuthority = Authority.query.filter_by(roleName=role).first()
            if userAuthority.customerDetail == False:
                self.can_view_details = False
            else:
                self.can_view_details = True
            if userAuthority.customerManage == False:
                self.can_create = False
                self.can_edit = False
                self.can_export = False
                self.can_delete = False
            else:
                self.can_create = True
                self.can_edit = True
                self.can_export = True
                self.can_delete = True
            return True
        else:
            return current_user.is_authenticated


class CoachView(MyBaseModelView):
    column_searchable_list = ("name" , "phoneNumber" , "job")

    def is_accessible(self):
        role = current_user.roles[0].name
        if not current_user.is_anonymous:
            userAuthority = Authority.query.filter_by(roleName=role).first()
            if userAuthority.coachDetail == False:
                self.can_view_details = False
            else:
                self.can_view_details = True
            if userAuthority.coachManage == False:
                self.can_create = False
                self.can_edit = False
                self.can_export = False
                self.can_delete = False
            else:
                self.can_create = True
                self.can_edit = True
                self.can_export = True
                self.can_delete = True
            return True
        else:
            return current_user.is_authenticated


class LessonView(MyBaseModelView):
    column_searchable_list = ("lessonName" , "room")

    def is_accessible(self):
        role = current_user.roles[0].name
        if not current_user.is_anonymous:
            userAuthority = Authority.query.filter_by(roleName=role).first()

            if userAuthority.lessonDetail == False:
                self.can_view_details = False
            else:
                self.can_view_details = True
            if userAuthority.lessonManage == False:
                self.can_create = False
                self.can_edit = False
                self.can_export = False
                self.can_delete = False
            else:
                self.can_create = True
                self.can_edit = True
                self.can_export = True
                self.can_delete = True
            return True
        else:
            return current_user.is_authenticated


class UserView(MyBaseModelView):
    column_searchable_list = ("id" , "name" , "email")
    column_list = ("id" , "name" , "email" , "customerID")

    def is_accessible(self):
        role = current_user.roles[0].name
        if not current_user.is_anonymous:
            userAuthority = Authority.query.filter_by(roleName=role).first()
            if userAuthority.userAdd == False:
                self.can_create = False
            else:
                self.can_create = True

            if userAuthority.userDelete == False:
                self.can_delete = False
            else:
                self.can_delete = True

            if userAuthority.userEdit == False:
                self.can_edit = False
            else:
                self.can_edit = True
            return True
        else:
            return current_user.is_authenticated


class VipCardView(MyBaseModelView):
    column_searchable_list = (
        "name" , "price" , "discount")

    def is_accessible(self):
        role = current_user.roles[0].name
        if not current_user.is_anonymous:
            userAuthority = Authority.query.filter_by(roleName=role).first()
            print(userAuthority.cardDetail)
            print(self.can_create)
            if userAuthority.cardDetail == False:
                self.can_view_details = False
            else:
                self.can_view_details = True
            if userAuthority.cardManage == False:
                self.can_create = False
                self.can_edit = False
                self.can_export = False
                self.can_delete = False
            else:
                self.can_create = True
                self.can_edit = True
                self.can_export = True
                self.can_delete = True
            return True
        else:
            return current_user.is_authenticated


class leaveView(AdminView):
    can_create = False
    column_list = ("id" , "customerid" , "starttime" , "endtime")

    def is_accessible(self):
        role = current_user.roles[0].name
        if not current_user.is_anonymous:
            userAuthority = Authority.query.filter_by(roleName=role).first()
            if userAuthority.leaveManage == False:
                self.can_edit = False
                self.can_export = False
                self.can_delete = False
            else:
                self.can_edit = True
                self.can_export = True
                self.can_delete = True
            return True
        else:
            return current_user.is_authenticated
