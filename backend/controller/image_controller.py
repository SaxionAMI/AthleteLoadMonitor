import os

from flask import send_file

from app import app, error_handler


@app.route('/api/image/<filename>', methods=['GET'])
@error_handler
def get_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
