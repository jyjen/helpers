import os

def path_checker(path: str,
                 check_type: str = {'directory', 'file'},
                 to_raise: bool = False) -> bool:

    """Function which checks if a specified directory or file exists.

    Arguments:
        path {string} -- Path of directory/file to check
        check_type {string} -- Type of check to perform
        to_raise {bool} -- Whether or not to raise an exception if directory/file is not found
            (default: {False})

    Returns:
        exists {bool} -- Whether the specified directory/file exists
    """

    func_dict = {'directory': os.path.isdir,
                 'file': os.path.isfile}

    if not check_type in func_dict.keys():
        raise ValueError("The check_type - '{}' is invalid. Please choose from {'directory', 'file'}".format(path))

    exists = func_dict[check_type](path)

    if not to_raise:
        return exists

    if exists:
        return exists

    else:
        raise ValueError("The {} - '{}' does not exist".format(check_type, path))

