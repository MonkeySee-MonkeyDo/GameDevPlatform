class Field:
    def __init__(self, title, name, required=False, disabled=False):
        self.title = title
        self.name = name
        self.value = None
        self.required = required
        self.disabled = disabled
    
    def render(self):
        pass

class FileUploadField(Field):
    def __init__(self, title, name, file_types=[], required=False, disabled=False):
        self.file_types = file_types
        super().__init__(title, name, required, disabled)
    
    def render(self):
        return f"""
        <div class="form-group">
            <label for="{self.name}>{self.title}{"*" if self.required else ""}:</label>
            <input 
            type="file" 
            class="form-control" 
            name="{self.name if self.name else ""}"
            {' accept="' + ",".join(self.file_types) + '"' if self.file_types else ""}
            {" required" if self.required else ""}
            {" disabled" if self.disabled else ""}>
        </div>

        """

class InputField(Field):
    def __init__(self, title, name, input_type, pattern, required=False, disabled=False):
        self.input_type = input_type
        self.pattern = pattern
        super().__init__(title, name, required, disabled)
    
    def render(self):
        return f"""
        <div class="form-group">
            <label for={self.name}>{self.title}{"*" if self.required else ""}:</label>
            <input type="{self.input_type}" 
            name="{self.name if self.name else ""}" 
            class="form-control-file" 
            {' value="' + self.value + '"' if self.value else ""}
            {' pattern="' + self.pattern + '"' if self.pattern else ""}
            {" required" if self.required else ""}
            {" disabled" if self.disabled else ""}>
        </div>

        """

class TextField(InputField):
    def __init__(self, title, name, pattern=None, required=False, disabled=False):
        super().__init__(title, name, "text", pattern, required, disabled)

class UsernameField(TextField):
    def __init__(self, title, name, required=False, disabled=False):
        pattern = "^[\w\.]{4,}$"
        super().__init__(title, name, pattern, required, disabled)

class PasswordField(InputField):
    def __init__(self, title, name, required=False, disabled=False):
        super().__init__(title, name, "password", None, required, disabled)

class EmailField(InputField):
    def __init__(self, title, name, required=False, disabled=False):
        super().__init__(title, name, "email", None, required, disabled)

class TelField(InputField):
    def __init__(self, title, name, required=False, disabled=False):
        pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
        super().__init__(title, name, "tel", pattern, required, disabled)

class DateField(InputField):
    def __init__(self, title, name, required=False, disabled=False):
        super().__init__(title, name, "date", None, required, disabled)

class URLField(InputField):
    def __init__(self, title, name, required=False, disabled=False):
        super().__init__(title, name, "url", None, required, disabled)

class TextAreaField(Field):
    def __init__(self, title, name, rows, cols, required=False, disabled=False):
        self.rows = rows
        self.cols = cols
        super().__init__(title, name, required, disabled)
    
    def render(self):
        return f"""
        <div class="form-group">
            <label for="{self.name}">{self.title}{"*" if self.required else ""}:</label>
            <textarea 
            class="form-control" 
            row="{self.rows}" 
            cols="{self.cols}" 
            name="{self.name if self.name else ""}"
            {" required" if self.required else ""}
            {" disabled" if self.disabled else ""}
            >{self.value if self.value else ""}</textarea>
        </div>
        """

class SelectField(Field):
    def __init__(self, title, name, options, required=False, disabled=False):
        self.options = options
        super().__init__(title, name, required, disabled)
    
    def render(self):
        start = f"""
        <div class="form-group">
            <label for="{self.name if self.name else ""}>{self.title}{"*" if self.required else ""}:</label>
            <select 
            class="form-control" 
            name="{self.name if self.name else ""}"
            {" required" if self.required else ""}
            {" disabled" if self.disabled else ""}>"""
        middle = ""
        for option in self.options:
            middle += f"""
                <option 
                value="{option[0]}"
                {" selected" if self.value == option[0] else ""}
                >{option[1]}</option>"""
        end = f"""
            </select>
        </div>
        """
        return start + middle + end

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
        <div class="form-group"><button class="btn btn-primary btn-block" type="submit">{self.submit}</button></div>
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