from main_app.form_fields import *

class LoginForm(Form):
    def __init__(self, title, legend):
        super().__init__(title, legend, "Log In",
            InputField("Username", "username", "text", True),
            InputField("Password", "password", "password", True)
        )

class UserForm(Form):
    def __init__(self, title, legend):
        super().__init__(title, legend, "Submit",
            InputField("Username", "username", "text", True),
            InputField("Password", "password", "password", True),
            InputField("Email", "email", "email", True)
        )