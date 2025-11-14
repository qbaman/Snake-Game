# Small sorting demo used for a quick on-screen benchmark.
# We compare two classic algorithms:
#  - Mergesort: always O(n log n), stable (keeps equal items in order)
#  - Quicksort (simple recursive version): fast on average, but can be slow on
#    already-sorted or “bad” inputs without extra tricks.
#
# The time_sort() helper creates random data, runs the sort, and returns
# how long it took. We call it from the game when you press the B key.

import random
import time

def mergesort(a):
    """Return a new sorted list using the mergesort algorithm."""
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = mergesort(a[:mid])     # sort the left half
    right = mergesort(a[mid:])    # sort the right half
    return _merge(left, right)    # stitch halves together

def _merge(a, b):
    """Merge two already-sorted lists into one sorted list."""
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    # Add anything left over
    out.extend(a[i:])
    out.extend(b[j:])
    return out

def quicksort(a):
    """Return a new sorted list using a simple quicksort (recursive)."""
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    # items less than pivot, equal to pivot, greater than pivot
    less  = [x for x in a if x <  pivot]
    equal = [x for x in a if x == pivot]
    more  = [x for x in a if x >  pivot]
    return quicksort(less) + equal + quicksort(more)

def time_sort(sort_fn, n=5000, trials=1):
    """
    Measure how long a sort function takes.
    - sort_fn: the sorting function to test (e.g., mergesort)
    - n: how many random numbers to sort
    - trials: run multiple times and keep the best (fastest) run
    Returns: seconds (float)
    """
    best = float("inf")
    for _ in range(trials):
        data = [random.randint(0, n) for _ in range(n)]
        t0 = time.perf_counter()
        sort_fn(data)                 # sort a fresh list
        dt = time.perf_counter() - t0
        if dt < best:
            best = dt
    return best
