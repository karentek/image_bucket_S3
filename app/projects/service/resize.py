from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image as PILImage


def resize_image(image_field, min_size, max_size):

    image = PILImage.open(image_field)

    # исходные размеры и соотношение сторон
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    # определяем ориентацию
    if aspect_ratio > 1:  # горизонтальное
        resize_height = min_size
        percent = resize_height / original_height
        resize_width = int(percent * original_width)

    else:  # вертикальное или квадратное
        resize_width = min_size
        percent = resize_width / original_width
        resize_height = int(percent * original_height)

    # меняем размер
    resized_image = image.resize((resize_width, resize_height))

    #обрезаем
    if aspect_ratio > 1:
        print('горизонтальное', resized_image.size)
        if resize_width > max_size:
            print('в случе если :')
            left = (resize_width - max_size) / 2
            right = (resize_width + max_size) / 2
            upper = 0
            lower = min_size
            image = resized_image.crop((left, upper, right, lower))
        elif resize_width <= max_size:
            print(' elif resize_width <= max_size:')
            image = PILImage.new('RGB', (max_size, min_size), (255, 255, 255))

            # Calculate paste coordinates for centering
            x_offset = (max_size - resize_width) // 2
            y_offset = 0

            # Paste resized and cropped image onto final image
            image.paste(resized_image, (x_offset, y_offset))
    else:
        print('Вертикальное', resized_image.size)
        if resize_height > max_size:
            print('if resize_height > max_size:')
            left = 0
            right = min_size
            upper = (resize_height - max_size) / 2
            lower = (resize_height + max_size) / 2
            print('before crop')
            image = resized_image.crop((left, upper, right, lower))
            print('after crop')
        elif resize_width <= max_size:
            print('elif resize_width < max_size:')

            image = PILImage.new('RGB', (min_size, max_size), (255, 255, 255))

            # Calculate paste coordinates for centering
            x_offset = 0
            y_offset = (max_size - resize_height) // 2
            print('lflflf')
            # Paste resized and cropped image onto final image
            image.paste(resized_image, (x_offset, y_offset))

    # Return the final image as a ContentFile
    return get_content_file(image, image_field.name)


def get_content_file(image, name):
    """
    Convert the PIL Image to a ContentFile.
    """
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return ContentFile(image_io.read(), name=name + '.jpg')