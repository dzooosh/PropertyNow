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
        if images[0] and self.__allowed_file(images[0].filename, ALLOWED_EXTENSIONS):
                filename = id + '.' + images[0].filename.rsplit('.', 1)[1].lower()
                images[0].save(os.path.join(destination_folder, filename))
                image_urls.append(f'http://localhost:5000/properties/images/{filename}')
        if len(images) == 1:
             return image_urls
        zip_path = os.path.join(destination_folder, f'{id}.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for image in images:
                        if image.filename != '' and self.__allowed_file(image.filename, ALLOWED_EXTENSIONS):
                                file_data = image.read()
                                zip_file.writestr(image.filename, file_data)
        image_urls.append(f'http://localhost:5000/properties/images/{id}.zip')
        return image_urls
