# utf-8

import os


def mkDir(dir_path):
    is_exists = os.path.exists(dir_path)
    if not is_exists:
        os.makedirs(dir_path)
