
# Custom Sorting Algorithm Visualizer

This project is an interactive Python application that visualizes the inner workings of several custom-designed sorting algorithms in real-time. Using Pygame for the interface, it provides a clear, bar-based representation of how data is manipulated during the sorting process. The application features a tabbed interface to seamlessly switch between and compare the different algorithms.

## Features

- **Real-Time Visualization:** Watch algorithms sort large datasets of up to 100,000 elements, sampled into 10,000 visual bars.
- **Tabbed Interface:** Easily switch between three distinct, custom-built sorting algorithms.
- **Centralized Configuration:** All major parameters (screen size, element counts, colors) are managed in a single `config.py` file.
- **Advanced Algorithm Design:** Includes "Adaptive Balance Sort," a high-performance hybrid algorithm inspired by professional-grade sorting libraries.

## How to Run

1.  **Ensure you have Pygame installed:**
    ```bash
    pip install pygame
    ```

2.  **Run the main application:**
    ```bash
    python3 main.py
    ```
    This will launch a start menu. Click the "Start Visualizer" button to proceed to the main tabbed interface.

## File Structure

-   **`main.py`**: The main entry point of the application. It handles the Pygame window, UI (menus, tabs), event loop, and state management.
-   **`config.py`**: A centralized file for all application settings, including screen dimensions, colors, and data generation parameters.
-   **`algorithms.py`**: Contains the logic for all sorting algorithms and their corresponding data generation functions.


---

# The Algorithms

## 1. Cascade Sort

-   **Concept:** A bottom-up merge sort that performs a pre-pass to create small, sorted "chunks," which are then efficiently merged in exponentially increasing sizes.
-   **How it Works:**
    1.  **Bucketing Pre-pass:** The array is divided into small buckets (e.g., 512 elements each), and each bucket is sorted individually. This establishes a baseline level of order.
    2.  **Cascading Merge:** The algorithm then "cascades" up, first merging sorted chunks of 512 into sorted chunks of 1024, then those into 2048, and so on, until the entire array is sorted.
-   **Performance:**
    -   **Time Complexity:** O(n log n) in all cases.
    -   **Space Complexity:** O(n) due to the temporary arrays required for merging.
-   **Use Case:** A reliable and efficient general-purpose sort.

## 2. Pigeonhole Cycle Sort

-   **Concept:** A highly specialized algorithm designed to sort a permutation of numbers from 1 to N. It is not a general-purpose sort.
-   **How it Works:**
    1.  The algorithm knows that for any number `k`, its final position must be index `k-1`.
    2.  It iterates through the array. If the number at index `i` is not `i+1`, it swaps that number to its correct "pigeonhole."
    3.  This process creates a "cycle" of swaps that continues until the correct number finally lands in index `i`.
-   **Performance:**
    -   **Time Complexity:** O(n). It is extremely fast for its specific use case because each element is moved at most once or twice.
    -   **Space Complexity:** O(1).
-   **Use Case:** Only for sorting lists that contain a full, unique set of integers from 1 to N. It will fail on datasets with duplicates, floats, or arbitrary numbers.

## 3. Deep Dive: Adaptive Balance Sort (Stijn's creation XD)

This is the most advanced algorithm in the collection. It is a custom-designed hybrid sort, inspired by Introsort, one of the fastest sorting algorithms in existence.

-   **Concept:** A fast, recursive algorithm that uses sampling to find a good pivot but protects itself from worst-case scenarios by switching to a different sorting method when it detects poor performance.

-   **How it Works & Mathematical Optimizations:**

    The algorithm has two key components that make it fast and reliable:

    **1. Optimized Pivot Selection (Sampling):**
    A major bottleneck in simple recursive sorts is choosing the pivot (the value used to split the array). The original "Balance Sort" was slow because it scanned the entire array segment (`A'`) to find the pivot:

    -   **Slow Method:** `pivot = (min(A') + max(A')) / 2`
    -   **Mathematical Cost:** This has a time cost of O(n) for each partition, which adds up significantly.

    The **Adaptive** version is much smarter. It takes a small, fixed-size random sample (`S`) of size `k` (e.g., k=32) from the array segment `A'`.

    -   **Fast Method:** `pivot = (min(S) + max(S)) / 2`
    -   **Mathematical Cost:** The cost of finding the min and max of the sample is O(k). Since `k` is a constant, the pivot selection becomes an O(1) operation relative to the size of the array segment. This is a massive performance gain.

    **2. Worst-Case Protection (Hybridization with Heapsort):**
    Any sort that relies on pivots can suffer from a worst-case scenario where bad pivots lead to very unbalanced partitions. This can degrade performance to O(n²). Adaptive Balance Sort prevents this using a "safety net."

    -   **The Problem:** An ideal sort splits the array into two equal halves, leading to a recursion depth of `log₂(n)`.
    -   **The Trigger:** The algorithm tracks its own recursion depth. If the depth exceeds a set limit, it assumes the pivot choices have been unlucky and the sort is becoming inefficient.
    -   **The Limit (Formula):** The depth limit is set to `2 * log₂(n)`. This formula provides a generous ceiling; if the recursion depth doubles past the ideal, it's a strong sign of a pathological case.
    -   **The Solution (Heapsort):** When the depth limit is exceeded, the algorithm switches from a pivot-based strategy to **Heapsort** for that specific, problematic segment. Heapsort has a mathematically guaranteed worst-case performance of O(n log n). This ensures that even in the unluckiest scenario, the algorithm's overall performance never degrades below O(n log n).

-   **Overall Performance:**
    -   **Average Time Complexity:** O(n log n). It is extremely fast on average due to the efficient, sampling-based partitioning.
    -   **Worst-Case Time Complexity:** O(n log n). This is guaranteed because the Heapsort "safety net" kicks in to prevent O(n²) performance.
    -   **Space Complexity:** O(log n). The space is used by the recursion stack. The depth limit ensures the stack size is always controlled.
-   **Conclusion:** "Adaptive Balance Sort" is a robust, high-performance algorithm suitable for a wide variety of real-world data, mirroring the design philosophy of professionally engineered sorting libraries.
