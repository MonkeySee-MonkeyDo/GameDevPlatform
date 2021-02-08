from main_app.form_fields import *

class Form:
    def __init__(self, *fields):
        self.fields = fields
    
    def render(self):
        output = ""
        for field in self.fields:
            output += field.render()
        return output
    
    def set_values(self, value_dict):
        for field in self.fields:
            if field.name in value_dict:
                val = value_dict[field.name]
            if isinstance(val, list):
                val = val[0]
            field.value = val

class UserForm(Form):
    def __init__(self):
        self.fields = [
            InputField("Username", "username", "text", True),
            InputField("Password", "password", "password", True),
            InputField("Email", "email", "email", True)
        ]

class ProfileForm(Form):
    def __init__(self):
        sexes = [["not set", "Select One..."], ["male", "Male"], ["female", "Female"], ["prefer not to say", "Prefer Not To Say"]]
        roles = [["not set", "Select One..."], ["developer", "Developer"], ["artist", "Artist"], ["combination", "Both"]]
        self.fields = [
            InputField("First Name", "first_name", "text", True),
            InputField("Last Name", "last_name", "text", True),
            InputField("Email", "email", "email", True, True),
            InputField("Phone Number", "phone_number", "tel"),
            InputField("Date of Birth", "dob", "date"),
            SelectField("Sex", "sex", sexes),
            SelectField("Role", "role", roles),
            InputField("Link", "link", "url"),
            FileUploadField("Profile Picture", "profile_picture", ["image/*"])
        ]

class PostForm(Form):
    def __init__(self, users):
        users_select = []
        for user in users:
            users_select.append([str(user["_id"]), user["username"]])
        self.fields = [
            SelectField("Poster", "user_id", users_select),
            InputField("Title", "title", "text", True),
            TextAreaField("Body", "body", 4, 50, True)
        ]

class ReplyForm(Form):
    def __init__(self, users):
        users_select = []
        for user in users:
            users_select.append([str(user["_id"]), user["username"]])
        self.fields = [
            SelectField("Poster", "user_id", users_select),
            TextAreaField("Body", "body", 4, 50, True)
        ]