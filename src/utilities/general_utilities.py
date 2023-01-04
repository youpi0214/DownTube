# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#           general operation functions go here              #
#                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import pathlib

import unicodedata
import re


def slugify(value, allow_unicode=False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def relative_to_abs_path(p_relative_path: str) -> str:
    """takes a path relative to the current project directory and converts it to an
    absolute path"""
    path = pathlib.Path(__file__).parent.parent.parent.resolve()
    return path.joinpath(p_relative_path).__str__()


def does_path_exist(p_path: str) -> bool:
    """returns whether the path exist or not. useful to verify a file or a directory existence"""
    return os.path.exists(p_path)
