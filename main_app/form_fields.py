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
        <label>
            {self.title}{"*" if self.required else ""}:
            <input 
            type="file" 
            name="{self.name if self.name else ""}"
            {' accept="' + ",".join(self.file_types) + '"' if self.file_types else ""}
            {" required" if self.required else ""}
            {" disabled" if self.disabled else ""}>
        </label>
        """

class InputField(Field):
    def __init__(self, title, name, input_type, required=False, disabled=False):
        self.input_type = input_type
        super().__init__(title, name, required, disabled)
    
    def render(self):
        return f"""
        <label>
            {self.title}{"*" if self.required else ""}:
            <input type="{self.input_type}" 
            name="{self.name if self.name else ""}"
            {' value="' + self.value + '"' if self.value else ""}
            {" required" if self.required else ""}
            {" disabled" if self.disabled else ""}>
        </label>
        """

class TextAreaField(Field):
    def __init__(self, title, name, rows, cols, required=False, disabled=False):
        self.rows = rows
        self.cols = cols
        super().__init__(title, name, required, disabled)
    
    def render(self):
        return f"""
        <label>
            {self.title}{"*" if self.required else ""}:
            <textarea 
            row="{self.rows}" 
            cols="{self.cols}" 
            name="{self.name if self.name else ""}"
            {" required" if self.required else ""}
            {" disabled" if self.disabled else ""}
            >{self.value if self.value else ""}</textarea>
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
            <select 
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
        </label>
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