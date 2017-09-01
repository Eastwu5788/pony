"""
this script is designed to collect common python funcs
"""


def python_version():
    """
    check python version
    :return: if python is 2.x it will return 2 or it will return 3
    """
    import platform
    version = platform.version()
    if version.startwith("2"):
        return 2
    elif version.startwith("3"):
        return 3
    else:
        return 0
