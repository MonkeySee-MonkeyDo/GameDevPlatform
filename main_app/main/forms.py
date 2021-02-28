from main_app.form_fields import *

class EditUserForm(Form):
    def __init__(self, title, legend):
        super().__init__(title, legend, "Submit",
            UsernameField("Username", "username", required=True),
            PasswordField("Password", "password", required=True),
            EmailField("Email", "email", required=True)
        )

class DeleteUserForm(Form):
    def __init__(self):
        super().__init__(
            "Delete User",
            "Please confirm your password:", 
            "DELETE", 
            PasswordField("Password", "password", required=True)
        )

class ProfileForm(Form):
    def __init__(self, title, legend):
        sexes = [["not set", "Select One..."], ["male", "Male"], ["female", "Female"], ["prefer not to say", "Prefer Not To Say"]]
        roles = [["not set", "Select One..."], ["developer", "Developer"], ["artist", "Artist"], ["combination", "Both"]]
        super().__init__(title, legend, "Submit",
            TextField("First Name", "first_name", required=True),
            TextField("Last Name", "last_name", required=True),
            EmailField("Email", "email", required=True, disabled=True),
            TelField("Phone Number", "phone_number"),
            DateField("Date of Birth", "dob"),
            SelectField("Sex", "sex", sexes),
            SelectField("Role", "role", roles),
            URLField("Link", "link"),
            FileUploadField("Profile Picture", "profile_picture", ["image/*"])
        )

class ProjectForm(Form):
    def __init__(self, title, legend):
        super().__init__(title, legend, "Submit",
        TextField("Project Name", "title", required=True),
        TextAreaField("Description", "description", 4, 50),
        URLField("Link", "link"))