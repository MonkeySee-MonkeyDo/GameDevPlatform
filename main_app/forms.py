class Field:
    def __init__(self, title, name, required=False, disabled=False):
        self.title = title
        self.name = name
        self.value = None
        self.required = required
        self.disabled = disabled
    
    def render(self):
        pass

class InputField(Field):
    def __init__(self, title, name, input_type, required=False, disabled=False):
        self.input_type = input_type
        super().__init__(title, name, required, disabled)
    
    def render(self):
        return f"""
        <label>
            {self.title}{"*" if self.required else ""}:
            <input type="{self.input_type}" name="{self.name}"{'value="' + self.value + '"' if self.value else ""}{" required" if self.required else ""}{" disabled" if self.disabled else ""}>
        </label>
        """

class SelectField(Field):
    def __init__(self, title, name, options, required=False, disabled=False):
        self.options = options
        super().__init__(title, name, required, disabled)
    
    def render(self):
        start = f"""
        <label>
            {self.title}{"*" if self.required else ""}:
            <select name="{self.name}"{" required" if self.required else ""}{" disabled" if self.disabled else ""}>"""
        middle = ""
        for option in self.options:
            middle += f"""
                <option value="{option[0]}"{" selected" if self.value == option[0] else ""}>{option[1]}</option>"""
        end = f"""
            </select>
        </label>
        """
        return start + middle + end

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
            val = value_dict[field.name]
            if isinstance(val, list):
                val = val[0]
            field.value = val

sexes = [["not set", "Select One..."], ["male", "Male"], ["female", "Female"], ["prefer not to say", "Prefer Not To Say"]]
roles = [["not set", "Select One..."], ["developer", "Developer"], ["artist", "Artist"], ["combination", "Both"]]

class UserForm(Form):
    def __init__(self):
        self.fields = [
            InputField("Username", "username", "text", True),
            InputField("Password", "password", "password", True),
            InputField("Email", "email", "email", True)
        ]

class ProfileForm(Form):
    def __init__(self):
        self.fields = [
            InputField("First Name", "first_name", "text", True),
            InputField("Last Name", "last_name", "text", True),
            InputField("Email", "email", "email", True, True),
            InputField("Phone Number", "phone_number", "tel"),
            InputField("Date of Birth", "dob", "date"),
            SelectField("Sex", "sex", sexes),
            SelectField("Role", "role", roles),
            InputField("Link", "link", "url")
        ]