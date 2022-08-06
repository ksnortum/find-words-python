def get_string_from_file(file_name: str) -> str:
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    return '\n'.join(lines)