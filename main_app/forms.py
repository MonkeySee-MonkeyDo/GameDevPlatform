class InputField:
    def __init__(self, title, name, input_type, required=False):
        self.title = title
        self.name = name
        self.input_type = input_type
        self.value = None
        self.required = required
    
    def render(self):
        return f"""
        <label>
            {self.title}{"*" if self.required else ""}:
            <input type="{self.input_type}" name="{self.name}"{'value="' + self.value + '"' if self.value else ""}{" required" if self.required else ""}>
        </label>
        """

class SelectField:
    def __init__(self, title, name, options, selected=None, required=False):
        self.title = title
        self.name = name
        self.options = options
        self.selected = selected
        self.required = required
    
    def render(self):
        start = f"""
        <label>
            {self.title}{"*" if self.required else ""}:
            <select name="{self.name}"{" required" if self.required else ""}>"""
        middle = ""
        for option in self.options:
            middle += f"""
                <option value="{option[0]}"{" selected" if self.selected == option[0] else ""}>{option[1]}</option>"""
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
            if isinstance(field, InputField):
                field.value = val
            elif isinstance(field, SelectField):
                field.selected = val

sexes = [["not set", "Select One..."], ["male", "Male"], ["female", "Female"], ["prefer not to say", "Prefer Not To Say"]]
roles = [["not set", "Select One..."], ["developer", "Developer"], ["artist", "Artist"], ["combination", "Both"]]

class UserForm(Form):
    def __init__(self):
        self.fields = [
            InputField("Username", "username", "text", True),
            InputField("Password", "password", "password", True),
            InputField("Email", "email", "email", True),
            InputField("Phone Number", "phone_number", "tel"),
            InputField("First Name", "first_name", "text", True),
            InputField("Last Name", "last_name", "text", True),
            InputField("Date of Birth", "dob", "date"),
            SelectField("Sex", "sex", sexes),
            SelectField("Role", "role", roles),
            InputField("Link", "links", "url")
        ]

