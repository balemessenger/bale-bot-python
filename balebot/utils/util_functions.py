import math
import random
import binascii
from io import BufferedReader
import re


def generate_random_id():
    return str(math.floor(random.random() * 1800000)) + str(math.floor(random.random() * 4000000)) + str(
        math.floor(random.random() * 55000))


def get_file_buffer(file, file_operation_mode="rb"):
    if isinstance(file, str):
        opened_file = open(file, file_operation_mode)
        buffer = opened_file.read()
        opened_file.close()
    elif isinstance(file, BufferedReader):
        buffer = file.read()
        file.close()
    elif isinstance(file, bytes):
        buffer = file
    else:
        return None

    return buffer


def get_file_size(file):
    buffer = get_file_buffer(file=file)
    return len(buffer)


def get_file_crc32(file):
    buffer = get_file_buffer(file=file)
    crc_buffer = (binascii.crc32(buffer) & 0xFFFFFFFF)
    return crc_buffer


def get_image_thumbnails(im):
    from io import BytesIO
    import base64
    from PIL import Image
    size = 80, 80
    im.thumbnail(size, Image.ANTIALIAS)
    output = BytesIO()
    im.save(output, format='JPEG')
    im_data = output.getvalue()
    thumb = '{}'.format(base64.b64encode(im_data).decode())
    return thumb


def arabic_to_eng_number(number):
    number = str(number)
    return number.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))


def eng_to_arabic_number(number):
    number = str(number)
    return number.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))


def phone_number_validation(phone_num):
    if re.match(r'^(\+98|0098|0)?9\d{9}$', phone_num):
        return True
    else:
        return False


def standardize_phone_number(number):
    number_str = str(number)
    if number_str.startswith("0098"):
        return "+98" + number_str[4:]
    elif number_str.startswith("0"):
        return "+98" + number_str[1:]
