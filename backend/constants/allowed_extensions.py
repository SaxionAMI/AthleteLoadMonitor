from enum import Enum


class ImageExtensions(Enum):
    PNG = '.png',
    JPG = '.jpg',
    JPEG = '.jpeg'

    @staticmethod
    def is_allowed(extension):
        extension = extension.lower()
        return not (not extension == ImageExtensions.PNG.value[0] and
                    not extension == ImageExtensions.JPG.value[0] and
                    not extension == ImageExtensions.JPEG.value[0])
