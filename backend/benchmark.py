import random
import time

from algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)


def make_records(n):
    return [
        {
            "title": f"Task {i:05d}",
            "priority": random.choice(["low", "medium", "high"])
        }
        for i in range(n)
    ]


def run_benchmark(n, trials=5):
    insertion_times = []
    insertion_comparisons = []

    binary_times = []
    binary_comparisons = []

    linear_times = []
    linear_comparisons = []

    for _ in range(trials):
        records = make_records(n)

        # Insertion sort
        sort_records = [record.copy() for record in records]

        start = time.perf_counter()
        sorted_records, comparisons = insertion_sort_count(
            sort_records,
            "title"
        )
        elapsed = time.perf_counter() - start

        insertion_times.append(elapsed)
        insertion_comparisons.append(comparisons)

        # Search target
        target = f"Task {n // 2:05d}"

        # Binary search
        start = time.perf_counter()
        _, comparisons = binary_search_count(
            sorted_records,
            target,
            "title"
        )
        elapsed = time.perf_counter() - start

        binary_times.append(elapsed)
        binary_comparisons.append(comparisons)

        # Linear search
        start = time.perf_counter()
        _, comparisons = linear_search_count(
            records,
            target,
            "title"
        )
        elapsed = time.perf_counter() - start

        linear_times.append(elapsed)
        linear_comparisons.append(comparisons)

    return {
        "n": n,
        "insertion_avg_ms": (
            sum(insertion_times) / trials * 1000
        ),
        "insertion_avg_comparisons": (
            sum(insertion_comparisons) / trials
        ),
        "binary_avg_ms": (
            sum(binary_times) / trials * 1000
        ),
        "binary_avg_comparisons": (
            sum(binary_comparisons) / trials
        ),
        "linear_avg_ms": (
            sum(linear_times) / trials * 1000
        ),
        "linear_avg_comparisons": (
            sum(linear_comparisons) / trials
        )
    }


if __name__ == "__main__":
    for n in [100, 1000, 5000]:
        result = run_benchmark(n)

        print("\n--- Benchmark ---")
        print(f"n = {result['n']}")
        print(
            f"Insertion Sort: "
            f"{result['insertion_avg_ms']:.4f} ms, "
            f"{result['insertion_avg_comparisons']:.2f} comparisons"
        )
        print(
            f"Binary Search: "
            f"{result['binary_avg_ms']:.4f} ms, "
            f"{result['binary_avg_comparisons']:.2f} comparisons"
        )
        print(
            f"Linear Search: "
            f"{result['linear_avg_ms']:.4f} ms, "
            f"{result['linear_avg_comparisons']:.2f} comparisons"
        )