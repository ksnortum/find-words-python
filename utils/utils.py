def get_string_from_file(file_name: str) -> str:
    """Given a text file "file_name", return a string of all lines in "file_name" concatenated."""
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    return ''.join(lines)


def are_lists_equal(list1: list, list2: list) -> bool:
    """Given two lists of equal length, return true if all elements are equal, otherwise return false."""
    if len(list1) != len(list2):
        print(f"Lists are not the same length, len(list1) = {len(list1)}, len(list2) = {len(list2)}")
        return False

    for i in range(len(list1)):
        if list1[i] != list2[i]:
            print(f"Lists differ at index {i}, list1[i] = {list1[i]}, list2[i] = {list2[i]}")
            return False

    return True
