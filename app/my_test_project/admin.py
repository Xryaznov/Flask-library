from flask_admin import Admin, expose, BaseView, AdminIndexView
from flask_admin.contrib.sqla import ModelView

admin = Admin()


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):

        return self.render('adminhome.html')


admin = Admin(index_view=MyHomeView())

from models import db, Book, User, Author

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Author, db.session))


