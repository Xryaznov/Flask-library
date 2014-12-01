from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, PasswordField, SelectMultipleField
from my_test_project.models import User, Book

class SignupForm(Form):
    firstname = StringField("First name", [validators.DataRequired("Please enter your first name.")])
    lastname = StringField("Last name", [validators.DataRequired("Please enter your last name.")])
    email = StringField("Email", [validators.DataRequired("Please enter email."), validators.Email("Please enter email.")])
    password = PasswordField("Password", [validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken.")
            return False
        else:
            return True


class SigninForm(Form):
    email = StringField("Email", [validators.DataRequired("Please enter email."), validators.Email("Please enter email.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter password.")])
    submit = SubmitField("Sign in")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password.")
            return False


class AddbookForm(Form):
    title = StringField("Title", [validators.DataRequired("Please enter title.")])
    author = StringField("Author", [validators.DataRequired("Please enter author.")])
    submit = SubmitField("Add")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True