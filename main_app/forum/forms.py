from main_app.form_fields import *

class PostForm(Form):
    def __init__(self, title, legend, users):
        super().__init__(title, legend, "Post",
            TextField("Title", "title", required=True),
            TextAreaField("Body", "body", 4, 50, required=True)
        )

class ReplyForm(Form):
    def __init__(self, title, legend, users):
        super().__init__(title, legend, "Reply",
            TextAreaField("Body", "body", 4, 50, required=True)
        )