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
        raise ValueError("The check_type - '{}' - is invalid. Please choose from {'directory', 'file'}".format(path))

    exists = func_dict[check_type](path)

    if not to_raise:
        return exists

    if exists:
        return exists

    else:
        raise ValueError("The {} - '{}' - does not exist".format(check_type, path))

def flatten_dict(d: dict):

    """Flattens dictionary with subdictionaries.

    Arguments:
        d {dict} -- Dict to flatten

    Returns:
        flattened {dict} -- Flattened dict
    """

    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    flattened = dict(items())

    return flattened

def flatten_list(ls: list) -> list:

    """Flattens list with sublists.

    Arguments:
        ls {list} -- List to flatten
    Returns:
        flattened {list} -- Flattened list"""

    flattened = [item for sublist in ls for item in sublist]
    return flattened

def check_continuous(n: int, l: list):

    """Checks for continuous numbers in a list.

    Arguments:
        n {int} -- Number of entries in a list
        l {list} -- List to check

    Returns:
        any_continuous {bool} -- Whether there are any continuous numbers in l
    """

    subs = [l[i:i+n] for i in range(len(l)) if len(l[i:i+n]) == n]
    any_continuous = any([(sorted(sub) in range(min(l), max(l)+1))
                          for sub in subs])

    return any_continuous
