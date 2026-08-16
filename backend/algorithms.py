def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0 and records[j][key] > current[key]:
            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current


def binary_search(sorted_records, target_value, key):
    low = 0
    high = len(sorted_records) - 1

    while low <= high:
        mid = (low + high) // 2
        value = sorted_records[mid][key]

        if value == target_value:
            return mid
        elif value < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def linear_search(records, target_value, key):
    for index, record in enumerate(records):
        if record[key] == target_value:
            return index

    return -1
def insertion_sort_count(records, key):
    comparisons = 0

    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if records[j][key] <= current[key]:
                break

            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return records, comparisons


def binary_search_count(sorted_records, target_value, key):
    comparisons = 0
    low = 0
    high = len(sorted_records) - 1

    while low <= high:
        mid = (low + high) // 2

        comparisons += 1

        if sorted_records[mid][key] == target_value:
            return mid, comparisons

        comparisons += 1

        if sorted_records[mid][key] < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


def linear_search_count(records, target_value, key):
    comparisons = 0

    for index, record in enumerate(records):
        comparisons += 1

        if record[key] == target_value:
            return index, comparisons

    return -1, comparisons