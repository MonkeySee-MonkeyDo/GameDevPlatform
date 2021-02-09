from main_app.form_fields import *

class Form:
    def __init__(self, title="Form", legend="Legend", submit="Submit", *fields):
        self.fields = fields
        self.title = title
        self.legend = legend
        self.submit = submit
    
    def render(self):
        output = ""
        for field in self.fields:
            output += field.render()
        output += f"""
        <input type="submit" value="{self.submit}">
        """
        return output
    
    def set_values(self, value_dict):
        for field in self.fields:
            if not (isinstance(field, InputField) and field.input_type == "password"):
                if field.name in value_dict:
                    val = value_dict[field.name]
                if isinstance(val, list):
                    val = val[0]
                field.value = val

class UserForm(Form):
    def __init__(self, title, legend):
        super().__init__(title, legend, "Submit",
            InputField("Username", "username", "text", True),
            InputField("Password", "password", "password", True),
            InputField("Email", "email", "email", True)
        )

class DeleteUserForm(Form):
    def __init__(self):
        super().__init__(
            "Delete User",
            "Please confirm your password:", 
            "DELETE", 
            InputField("Password", "password", "password", True)
        )

class ProfileForm(Form):
    def __init__(self, title, legend):
        sexes = [["not set", "Select One..."], ["male", "Male"], ["female", "Female"], ["prefer not to say", "Prefer Not To Say"]]
        roles = [["not set", "Select One..."], ["developer", "Developer"], ["artist", "Artist"], ["combination", "Both"]]
        super().__init__(title, legend, "Submit",
            InputField("First Name", "first_name", "text", True),
            InputField("Last Name", "last_name", "text", True),
            InputField("Email", "email", "email", True, True),
            InputField("Phone Number", "phone_number", "tel"),
            InputField("Date of Birth", "dob", "date"),
            SelectField("Sex", "sex", sexes),
            SelectField("Role", "role", roles),
            InputField("Link", "link", "url"),
            FileUploadField("Profile Picture", "profile_picture", ["image/*"])
        )

class PostForm(Form):
    def __init__(self, title, legend, users):
        super().__init__(title, legend, "Submit",
            InputField("Title", "title", "text", True),
            TextAreaField("Body", "body", 4, 50, True)
        )

class ReplyForm(Form):
    def __init__(self, title, legend, users):
        super().__init__(title, legend, "Submit",
            TextAreaField("Body", "body", 4, 50, True)
        )

class LoginForm(Form):
    def __init__(self, title, legend):
        super().__init__(title, legend, "Log In",
            InputField("Username", "username", "text", True),
            InputField("Password", "password", "password", True)
        )