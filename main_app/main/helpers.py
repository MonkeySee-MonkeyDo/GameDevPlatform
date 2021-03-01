from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os
from main_app import app

def get_id(id):
    return {"_id": ObjectId(id)}

def rename_file(file, filename):
    file.filename = f"{filename}"
    return file.filename

def save_file(file, filename, *folders):
    if file:
        filename = secure_filename(filename)
        file.filename = filename
        path = app.root_path
        path = os.path.join(path, "static")
        for folder in folders:
            path = os.path.join(path, folder)
        path = os.path.join(path, filename)
        if os.path.exists(path):
            file.save(f"{path}.tmp")
            os.replace(f"{path}.tmp", path)
        else:
            file.save(path)