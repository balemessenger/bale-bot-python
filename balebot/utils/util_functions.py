import math
import random
import binascii
from io import BufferedReader


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
