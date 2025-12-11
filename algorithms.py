"""
This file contains the sorting algorithms and data generation logic
for the Sorting Visualizer application.
"""

import random
import math
import config

# --- Data Generation ---

def generate_data(sort_type: str):
    """Generates data tailored to the specified sorting algorithm."""
    if sort_type == 'pigeonhole':
        n = config.PIGEONHOLE_NUM_ELEMENTS
        print(f"Generating shuffled list of {n:,} numbers for Pigeonhole Sort...")
        data = list(range(1, n + 1))
        random.shuffle(data)
        return data, config.PIGEONHOLE_MAX_VAL
    else:
        n = config.GENERAL_NUM_ELEMENTS
        min_v = config.GENERAL_MIN_VAL
        max_v = config.GENERAL_MAX_VAL
        print(f"Generating {n:,} random floats for {sort_type.title()} Sort...")
        data = [random.uniform(min_v, max_v) for _ in range(n)]
        return data, max_v

# --- Algorithm 1: Cascade Sort ---
# (Previous implementation remains unchanged)
def cascade_sort(data):
    """Generator-based Cascade Sort."""
    n = len(data)
    op_counter = 0
    bucket_size = 512
    for i in range(0, n, bucket_size):
        end = min(i + bucket_size, n)
        data[i:end] = sorted(data[i:end])
        op_counter += (end - i)
        if op_counter > config.UPDATE_FREQUENCY:
            yield {k for k in range(i, end)}, set(); op_counter = 0
    yield set(), set()
    width = bucket_size
    while width < n:
        for i in range(0, n, 2 * width):
            left, mid, right = i, min(i + width, n), min(i + 2 * width, n)
            if mid < right:
                temp = []
                l_ptr, r_ptr = left, mid
                while l_ptr < mid and r_ptr < right:
                    if data[l_ptr] <= data[r_ptr]: temp.append(data[l_ptr]); l_ptr += 1
                    else: temp.append(data[r_ptr]); r_ptr += 1
                temp.extend(data[l_ptr:mid]); temp.extend(data[r_ptr:right])
                for j, val in enumerate(temp):
                    data[left + j] = val
                    op_counter += 1
                    if op_counter > config.UPDATE_FREQUENCY: yield {left + j}, set(); op_counter = 0
        width *= 2
    yield set(), set()


# --- Algorithm 2: Pigeonhole Sort ---
# (Previous implementation remains unchanged)
def pigeonhole_sort(data):
    """Generator-based Pigeonhole Sort."""
    n = len(data)
    op_counter = 0
    for i in range(n):
        correct_value = i + 1
        while data[i] != correct_value:
            current_val = int(data[i])
            target_pos = current_val - 1
            if not (0 <= target_pos < n): break 
            data[i], data[target_pos] = data[target_pos], data[i]
            op_counter += 1
            if op_counter > (config.UPDATE_FREQUENCY / 100): yield {i, target_pos}, set(); op_counter = 0
    yield set(), set()


# --- Algorithm 3: Adaptive Balance Sort (Optimized) ---

def _heapify(data, n, i, start, op_counter):
    """Helper for Heapsort. Note: n is size, i is index, start is array offset."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and data[start + left] > data[start + largest]: largest = left
    if right < n and data[start + right] > data[start + largest]: largest = right
    if largest != i:
        data[start + i], data[start + largest] = data[start + largest], data[start + i]
        op_counter += 1
        yield {start + i, start + largest}, set()
        yield from _heapify(data, n, largest, start, op_counter)

def _heapsort_generator(data, start, end, op_counter):
    """A generator for in-place Heapsort on a slice of the data."""
    n = end - start + 1
    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        yield from _heapify(data, n, i, start, op_counter)
    # One by one extract elements
    for i in range(n - 1, 0, -1):
        data[start], data[start + i] = data[start + i], data[start]
        op_counter += 1
        yield {start, start + i}, set()
        yield from _heapify(data, i, 0, start, op_counter)

def _balance_sort_recursive(data, start, end, depth, depth_limit):
    """The recursive core of the Adaptive Balance Sort."""
    op_counter = 0
    
    # --- Worst-Case Protection ---
    if depth > depth_limit:
        yield from _heapsort_generator(data, start, end, op_counter)
        return

    if start >= end:
        return

    # --- Optimized Pivot Selection (Sampling) ---
    size = end - start + 1
    sample_size = min(size, 32) # Take a sample of up to 32 elements
    sample_indices = random.sample(range(start, end + 1), sample_size)
    sample = [data[i] for i in sample_indices]
    
    min_val, max_val = min(sample), max(sample)

    if min_val == max_val:
        # If sample is uniform, the whole segment might be. Fallback to heapsort.
        yield from _heapsort_generator(data, start, end, op_counter)
        return

    pivot = min_val + (max_val - min_val) / 2
    
    # --- Partitioning Phase ---
    i, j = start, end
    while i <= j:
        while data[i] < pivot: i += 1
        while data[j] >= pivot: j -= 1
        if i <= j:
            data[i], data[j] = data[j], data[i]
            op_counter += 1
            if op_counter > config.UPDATE_FREQUENCY / 5: # Update more often in this faster sort
                yield {i, j}, set()
                op_counter = 0
            i += 1
            j -= 1
    
    # --- Recurse ---
    if start < j:
        yield from _balance_sort_recursive(data, start, j, depth + 1, depth_limit)
    if i < end:
        yield from _balance_sort_recursive(data, i, end, depth + 1, depth_limit)

def balance_sort(data):
    """
    Adaptive Balance Sort: A fast, hybrid algorithm.
    - Uses sampling to find a "balance point" pivot.
    - Switches to Heapsort if recursion depth exceeds a limit, ensuring O(n log n) worst-case.
    """
    # Set a recursion depth limit to prevent worst-case scenarios
    depth_limit = 2 * math.log2(len(data) if len(data) > 1 else 1)
    yield from _balance_sort_recursive(data, 0, len(data) - 1, 0, depth_limit)
    yield set(), set() # Final yield to confirm completion