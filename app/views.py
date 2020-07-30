from flask_admin import expose
from flask_admin.contrib.sqla import ModelView


class CustomerView(ModelView):
    page_size = 10

    @expose('/')
    def index(self):
        return self.render('admin/cutomer.html')
