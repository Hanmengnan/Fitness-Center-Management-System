from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from flask import redirect, url_for, render_template, request


class MyBaseModelView(ModelView):
    column_display_pk = True
    can_set_page_size = True
    can_view_details = True

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

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('web.login', next=request.url))


class CustomerView(MyBaseModelView):
    column_searchable_list = ("name", "adress", "sid", "phoneNumber")
    page_size = 10


class CoachView(MyBaseModelView):
    column_auto_select_related = True
    column_searchable_list = ("name", "nation", "political", "education", "phoneNumber", "job",
                              "school")

    page_size = 10


class LessonView(MyBaseModelView):
    column_auto_select_related = True

    column_searchable_list = (
        "lessonName", "lessonData", "room", "coach")

    page_size = 10
