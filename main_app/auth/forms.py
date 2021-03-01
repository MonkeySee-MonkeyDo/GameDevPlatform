from main_app.form_fields import *

class LoginForm(Form):
    def __init__(self, title, legend):
        super().__init__(title, legend, "Log In",
            TextField("Username", "username", required=True),
            PasswordField("Password", "password", required=True)
        )

class SignUpForm(Form):
    def __init__(self, title, legend):
        roles = [["not set", "Select One..."], ["developer", "Developer"], ["artist", "Artist"], ["combination", "Both"]]
        super().__init__(title, legend, "Sign Up",
            UsernameField("Username", "username", required=True),
            PasswordField("Password", "password", required=True),
            EmailField("Email", "email", required=True),
            SelectField("Role", "role", roles, required=True)
        )