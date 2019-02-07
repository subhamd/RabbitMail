import os


def rel(*path):
    """
    Converts path relative to the project root into an absolute path

    :rtype: str
    """
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            *path
        )
    ).replace("\\", "/")
