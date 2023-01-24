import os
from main import app


def return_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'logo{id}' in file_name:
            return file_name
        return 'default_logo.png'

def delete_file(id):
    file = return_image(id)
    if file != 'default_logo.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH']), file)