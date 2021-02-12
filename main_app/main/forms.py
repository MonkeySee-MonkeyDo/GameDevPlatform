from main_app.form_fields import *

class EditUserForm(Form):
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