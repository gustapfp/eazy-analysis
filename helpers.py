import os
from main import app


def return_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'logo{id}' in file_name:
            return file_name
        return 'default_logo.png'