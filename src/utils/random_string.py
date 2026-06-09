# -*- coding: utf-8 -*-
"""
 Random generator string
"""

import random
import string


def random_string(string_length=10) -> str:
    """
    Generate a random string of fixed length

    :param string_length: longeur de la string à générer
    :return: string aléatoire
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(string_length))