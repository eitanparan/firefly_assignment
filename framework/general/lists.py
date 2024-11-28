def list_to_string(l):
    """

    :param l:
    :return:
    """
    try:
        output = ''
        for s in l:
            output += s + " "
        return output
    except Exception as err:
        raise Exception(err)


def string_to_list(s, seperator=' '):
    """

    :param s:
    :param seperator:
    :return:
    """
    try:
        if isinstance(s, list):
            return s
        output = []
        for cmd in s.split(seperator):
            output.append(cmd)
        return output
    except Exception as err:
        raise Exception(f"Failed converting string to list: {err}")