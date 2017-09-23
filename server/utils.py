"""
    server/utils.py
    Shared utilities
"""

def string_to_bool(s):
    """
    Convert string to boolean
    """
    true_list = ['true', 'yes', 'y']
    false_list = ['false', 'no', 'n']

    if s.lower() in true_list:
        return True
    elif s.lower() in false_list:
        return False

    raise ValueError("'{}' is not a valid boolean equivalent".format(s))
