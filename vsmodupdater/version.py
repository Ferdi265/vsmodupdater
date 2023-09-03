from typing import List

def as_list(ver: str) -> List[int]:
    try:
        return [int(v) for v in ver.split(".")]
    except ValueError:
        raise ValueError("unparseable version")

def compare(ver1: str, ver2: str) -> int:
    list1 = as_list(ver1)
    list2 = as_list(ver2)

    if list1 == list2:
        return 0
    elif list1 < list2:
        return -1
    elif list1 > list2:
        return 1
    else:
        raise ValueError("uncomparable versions")
