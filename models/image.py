"""
`image` module
"""
import zipfile
import os
import uuid


class Image:
    """
    This class manages the images stored locally
    """

    def __allowed_file(self, filename, ALLOWED_EXTENSIONS):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def add_images(self, destination_folder, ALLOWED_EXTENSIONS, images):
        """
        saves images locally
        """
        id = str(uuid.uuid4())
        image_urls = []
        if len(images) == 0:
            return image_urls
        for image in images:
            if self.__allowed_file(image.filename, ALLOWED_EXTENSIONS):
                    id = str(uuid.uuid4())
                    filename = id + '.' + image.filename.rsplit('.', 1)[1].lower()
                    image.save(os.path.join(destination_folder, filename))
                    image_urls.append(f'http://localhost:5000/properties/images/{filename}')
        return image_urls
