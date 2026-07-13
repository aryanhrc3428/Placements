"""
================================================================================
               PYTHON MEMORY PROFILING: A COMPLETE TUTORIAL
================================================================================
Optimizing code isn't just about speed (time complexity); it's also about footprint 
(space complexity). If your program eats up all the RAM, the OS will aggressively 
shut it down. 

In Python, we have two primary built-in weapons for inspecting memory:
1. sys.getsizeof(): A quick tool to check the exact size of a single object.
2. tracemalloc: A powerful module to track full memory allocations, take snapshots, 
   and locate memory leaks down to the exact line of code.
"""

import sys
import tracemalloc
import gc
import time

# ================================================================================
# CONCEPT 1: The Basics of sys.getsizeof()
# ================================================================================
# `sys.getsizeof()` returns the memory size of an object in bytes. 
# Crucial Caveat: It only measures the "shallow" size of the object. For containers 
# (like lists or dicts), it counts the size of the container structure itself, 
# NOT the items stored inside it!

print("--- Concept 1: Shallow Memory with sys.getsizeof() ---")

basic_int = 42
large_int = 2**1000
empty_list = []
populated_list = [1, 2, 3, 4, 5]

print(f"Size of integer 42:          {sys.getsizeof(basic_int)} bytes")
print(f"Size of a massive integer:   {sys.getsizeof(large_int)} bytes")
print(f"Size of an empty list:       {sys.getsizeof(empty_list)} bytes")
print(f"Size of list with 5 items:   {sys.getsizeof(populated_list)} bytes")

# The Shallow Size Trap:
nested_list = [[1, 2, 3, 4, 5]]
print(f"Size of a nested list wrapper: {sys.getsizeof(nested_list)} bytes") 
print("Notice how the outer list container weighs the same regardless of what's inside!")
print("-" * 60 + "\n")


# ================================================================================
# CONCEPT 2: The Basics of tracemalloc
# ================================================================================
# `tracemalloc` tracks every single memory block allocated by the Python interpreter.
# Steps: 1. start() -> 2. Take Snapshot 1 -> 3. Run Code -> 4. Take Snapshot 2 -> 5. Compare

print("--- Concept 2: Introduction to tracemalloc ---")

# Start tracking memory allocations
tracemalloc.start()

snapshot_before = tracemalloc.take_snapshot()

# Allocate some memory intentionally
temporary_strings = [str(x) for x in range(10000)]

snapshot_after = tracemalloc.take_snapshot()

# Compare the snapshots to see what changed
stats = snapshot_after.compare_to(snapshot_before, 'lineno')

print("[Top Memory Changes]")
for stat in stats[:3]:  # Print top 3 memory-consuming lines
    print(stat)

# Clean up memory and stop tracking for the next example
del temporary_strings
gc.collect()  # Force garbage collection
tracemalloc.stop()
print("-" * 60 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Comparing Data Structure Efficiency
# ================================================================================
# Let's say you need to store 100,000 unique IDs. Should you use a List or a Set?
# Let's profile their peak memory footprints using tracemalloc.

def profile_data_structures():
    print("--- Real-World 1: Data Structure Memory Battle ---")
    
    # Track List
    tracemalloc.start()
    list_data = [x for x in range(100000)]
    current, peak_list = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del list_data
    gc.collect()

    # Track Set
    tracemalloc.start()
    set_data = {x for x in range(100000)}
    current, peak_set = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del set_data
    gc.collect()

    print(f"Peak memory for List: {peak_list / 1024:.2f} KB")
    print(f"Peak memory for Set:  {peak_set / 1024:.2f} KB")
    print("-> Sets offer O(1) lookups, but consume significantly more RAM than lists!")
    print("-" * 60 + "\n")

profile_data_structures()


# ================================================================================
# REAL-WORLD EXAMPLE 2: Hunting a Memory Leak
# ================================================================================
# Memory leaks happen when objects stay referenced in memory even though they 
# aren't needed anymore. Let's write a leaky simulation and catch it red-handed.

LEAKY_CACHE = []

def access_api_and_leak_data(user_id):
    # Simulating data processing that accidentally saves a reference globally
    session_data = {"id": user_id, "timestamp": time.time(), "payload": "A" * 500}
    LEAKY_CACHE.append(session_data)  # The leak: appending to a global list indefinitely

print("--- Real-World 2: Finding a Memory Leak ---")
tracemalloc.start()
start_snapshot = tracemalloc.take_snapshot()

# Run the leaky function multiple times
for i in range(1000):
    access_api_and_leak_data(i)

end_snapshot = tracemalloc.take_snapshot()
leaky_stats = end_snapshot.compare_to(start_snapshot, 'traceback')

# Print the exact file and line number causing the biggest memory spike
# leaky_stats is a sorted list. [0] extracts the single worst 'StatisticDiff' object.
top_leak = leaky_stats[0]

print(f"CRITICAL: Biggest memory consumer found!")
print(f"Size: {top_leak.size / 1024:.2f} KB")

# top_leak.traceback.format() turns the allocation call stack into a list of strings
# ordered from oldest to newest. Using [-1] safely snipers the very last frame,
# pointing directly to the exact line of code responsible for triggering the leak.
print(f"Line Reference:\n{top_leak.traceback.format()[-1].strip()}")

# Clear leak and stop tracking
LEAKY_CACHE.clear()
tracemalloc.stop()
print("-" * 60 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Monitoring Peak Memory of a Heavy Operation
# ================================================================================
# When running large batch jobs or ETL scripts, you want to know the absolute max 
# RAM your script demanded, so you can provision your cloud servers accurately.

def heavy_batch_processor():
    # Simulate loading millions of records, processing them, and freeing them
    chunk_1 = [bytes(1024) for _ in range(5000)]   # ~5MB allocated
    chunk_2 = [bytes(1024) for _ in range(10000)]  # ~10MB allocated
    del chunk_1
    del chunk_2
    gc.collect()

print("--- Real-World 3: Measuring Server Provisioning (Peak RAM) ---")
tracemalloc.start()

heavy_batch_processor()

# get_traced_memory() returns a tuple: (current_size, peak_size)
current_ram, peak_ram = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Current RAM active: {current_ram / (1024 * 1024):.2f} MB")
print(f"Peak RAM requested: {peak_ram / (1024 * 1024):.2f} MB")
print("-> Provision this cloud script with at least 20MB of overhead safety headroom.")
print("-" * 60)