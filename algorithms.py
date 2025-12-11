# ============================================================================
# Sorting Algorithms Visualization
# Educational implementation with step-by-step visualization support
# ============================================================================

from collections import namedtuple
from typing import Generator, List, Tuple

# Step tracking for visualization
Step = namedtuple("Step", ["type", "i", "j", "value", "description"])
# type: 'compare', 'swap', 'overwrite'


class SortingAlgorithm:
    """Base class for sorting algorithms with metrics tracking."""

    def __init__(self, arr: List[int]):
        self.arr = arr[:]
        self.comparisons = 0
        self.swaps = 0
        self.writes = 0

    def get_metrics(self) -> dict:
        """Return algorithm performance metrics."""
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "writes": self.writes,
            "total_operations": self.comparisons + self.swaps + self.writes
        }


def bubble_sort(arr: List[int]) -> Generator[Step, None, None]:
    """
    Bubble Sort - O(n²) time complexity
    Compares adjacent elements and swaps them if in wrong order.
    """
    arr = arr[:]
    n = len(arr)
    comparisons = swaps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            yield Step("compare", j, j + 1, None, f"Comparing arr[{j}] with arr[{j+1}]")
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                yield Step("swap", j, j + 1, None, f"Swapped arr[{j}] and arr[{j+1}]")
                swapped = True
        
        if not swapped:
            yield Step("complete", -1, -1, None, "Array is sorted - early exit")
            break

    yield Step("done", -1, -1, None, f"Bubble Sort Complete | Comparisons: {comparisons} | Swaps: {swaps}")


def selection_sort(arr: List[int]) -> Generator[Step, None, None]:
    """
    Selection Sort - O(n²) time complexity
    Finds minimum element and places it at the beginning.
    """
    arr = arr[:]
    n = len(arr)
    comparisons = swaps = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            yield Step("compare", min_idx, j, None, f"Comparing arr[{min_idx}] with arr[{j}]")
            
            if arr[j] < arr[min_idx]:
                min_idx = j

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            yield Step("swap", i, min_idx, None, f"Swapped arr[{i}] and arr[{min_idx}]")

    yield Step("done", -1, -1, None, f"Selection Sort Complete | Comparisons: {comparisons} | Swaps: {swaps}")


def insertion_sort(arr: List[int]) -> Generator[Step, None, None]:
    """
    Insertion Sort - O(n²) worst case, O(n) best case
    Builds sorted array one item at a time by inserting elements into position.
    """
    arr = arr[:]
    n = len(arr)
    comparisons = writes = 0

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        while j >= 0:
            comparisons += 1
            yield Step("compare", j, i, None, f"Comparing arr[{j}] with arr[{i}]")
            
            if arr[j] > key:
                arr[j + 1] = arr[j]
                writes += 1
                yield Step("overwrite", j + 1, None, arr[j], f"Shifted arr[{j}] to arr[{j+1}]")
                j -= 1
            else:
                break

        arr[j + 1] = key
        writes += 1
        yield Step("overwrite", j + 1, None, key, f"Inserted {key} at position {j+1}")

    yield Step("done", -1, -1, None, f"Insertion Sort Complete | Comparisons: {comparisons} | Writes: {writes}")


def merge_sort(arr: List[int]) -> Generator[Step, None, None]:
    """
    Merge Sort - O(n log n) time complexity
    Divide and conquer algorithm that divides array and merges sorted subarrays.
    """
    arr = arr[:]
    n = len(arr)
    aux = arr[:]
    comparisons = writes = 0

    def merge(l: int, m: int, r: int):
        nonlocal comparisons, writes
        i, j, k = l, m + 1, l

        while i <= m and j <= r:
            comparisons += 1
            yield Step("compare", i, j, None, f"Comparing arr[{i}] with arr[{j}]")
            
            if aux[i] <= aux[j]:
                arr[k] = aux[i]
                writes += 1
                yield Step("overwrite", k, None, arr[k], f"Merged arr[{i}] to position {k}")
                i += 1
            else:
                arr[k] = aux[j]
                writes += 1
                yield Step("overwrite", k, None, arr[k], f"Merged arr[{j}] to position {k}")
                j += 1
            k += 1

        while i <= m:
            arr[k] = aux[i]
            writes += 1
            yield Step("overwrite", k, None, arr[k], f"Merged remaining arr[{i}] to position {k}")
            i += 1
            k += 1

        while j <= r:
            arr[k] = aux[j]
            writes += 1
            yield Step("overwrite", k, None, arr[k], f"Merged remaining arr[{j}] to position {k}")
            j += 1
            k += 1

    def msort(l: int, r: int):
        if l >= r:
            return
        m = (l + r) // 2
        yield from msort(l, m)
        yield from msort(m + 1, r)
        
        for t in range(l, r + 1):
            aux[t] = arr[t]
        
        yield from merge(l, m, r)

    if n > 0:
        yield from msort(0, n - 1)
    
    yield Step("done", -1, -1, None, f"Merge Sort Complete | Comparisons: {comparisons} | Writes: {writes}")


def quick_sort(arr: List[int]) -> Generator[Step, None, None]:
    """
    Quick Sort - O(n log n) average, O(n²) worst case
    Divide and conquer using pivot partitioning.
    """
    arr = arr[:]
    n = len(arr)
    comparisons = swaps = 0

    def partition(l: int, r: int):
        nonlocal comparisons, swaps
        pivot = arr[r]
        i = l - 1

        for j in range(l, r):
            comparisons += 1
            yield Step("compare", j, r, None, f"Comparing arr[{j}] with pivot {pivot}")
            
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
                yield Step("swap", i, j, None, f"Swapped arr[{i}] and arr[{j}]")

        arr[i + 1], arr[r] = arr[r], arr[i + 1]
        swaps += 1
        yield Step("swap", i + 1, r, None, f"Placed pivot {pivot} at position {i+1}")
        return i + 1

    def qsort(l: int, r: int):
        if l < r:
            pi = yield from partition(l, r)
            yield from qsort(l, pi - 1)
            yield from qsort(pi + 1, r)

    if n > 0:
        yield from qsort(0, n - 1)
    
    yield Step("done", -1, -1, None, f"Quick Sort Complete | Comparisons: {comparisons} | Swaps: {swaps}")


# Export all algorithms
ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}
