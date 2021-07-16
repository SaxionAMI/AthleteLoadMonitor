import os
import uuid
from typing import Optional

from constants.allowed_extensions import ImageExtensions


class FileUploadService:
    def __init__(self, app):
        self.app = app

    def upload_image(self, file) -> Optional[str]:
        if file is None:
            return None
        _, file_extension = os.path.splitext(file.filename)
        if not ImageExtensions.is_allowed(file_extension):
            raise Exception('Not supported file extension')
        filename = f'{str(uuid.uuid4())}{file_extension}'
        file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], f'{filename}'))
        return filename

