from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os

############################################################
# HELPER FUNCTIONS
############################################################

def doc_from_id(collection, id):
    return collection.find_one({"_id": ObjectId(id)})

def rename_file(file, filename):
    file.filename = f"{filename}.{file.filename.split('.')[1]}"
    return file.filename

def save_file(file, filename, *folders):
    if file:
        filename = rename_file(file, filename)
        filename = secure_filename(filename)
        path = main.root_path
        for folder in folders:
            path = os.path.join(path, folder)
        file.save(os.path.join(path, filename))