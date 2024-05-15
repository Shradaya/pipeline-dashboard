def escape_single_quotes_in_dict(input_dict):
    escaped_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, str):
            escaped_dict[key] = value.replace("'", "`")
        elif isinstance(value, dict):
            escaped_dict[key] = escape_single_quotes_in_dict(value)
        else:
            escaped_dict[key] = value
    return escaped_dict