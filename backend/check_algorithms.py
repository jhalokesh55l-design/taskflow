from algorithms import (
    insertion_sort,
    binary_search,
    linear_search
)


records = [
    {"title": "Task C"},
    {"title": "Task A"},
    {"title": "Task B"},
]


print("Testing insertion_sort...")

insertion_sort(records, "title")

assert [record["title"] for record in records] == [
    "Task A",
    "Task B",
    "Task C",
]

print("PASS")


print("Testing binary_search...")

index = binary_search(records, "Task B", "title")

assert index != -1
assert records[index]["title"] == "Task B"

print("PASS")


print("Testing linear_search...")

index = linear_search(records, "Task C", "title")

assert index != -1
assert records[index]["title"] == "Task C"

print("PASS")


print("Testing missing value...")

index = linear_search(records, "Task Z", "title")

assert index == -1

print("PASS")


print("\nAll algorithm checks passed.")