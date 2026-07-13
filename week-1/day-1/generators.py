"""
================================================================================
                   PYTHON GENERATORS & YIELD: A COMPLETE TUTORIAL
================================================================================
A generator function is a special type of function in Python that returns an 
iterator object. Instead of computing all values at once and returning them in 
a bulk list, a generator produces values dynamically—one at a time—on demand.

The Core Secret: The 'yield' keyword.
- 'return' completely terminates a function and destroys its local state.
- 'yield' pauses the function, saves all its environment/variables, and emits 
  a value back to the caller. When called again, it resumes exactly where it left off.
"""

import sys
import time

# ================================================================================
# CONCEPT 1: Yield vs Return (The Basics)
# ================================================================================
# Let's see how a generator pauses and resumes execution sequentially.

def simple_generator():
    print("[Gen] Starting execution...")
    yield "First Stop"
    
    print("[Gen] Resuming to second item...")
    yield "Second Stop"
    
    print("[Gen] Almost done...")
    yield "Final Stop"
    # When the function finishes or hits a return, StopIteration is automatically raised.

print("--- Concept 1: The Behavior of Yield ---")
# Calling the function does NOT run the code; it returns a generator object.
gen = simple_generator()
print(f"Object type: {type(gen)}")

print("\n--- Triggering the values manually ---")
print(f"Pulled: {next(gen)}")
print(f"Pulled: {next(gen)}")
print(f"Pulled: {next(gen)}")

# Calling next(gen) one more time would cause a StopIteration exception.
print("-" * 50 + "\n")


# ================================================================================
# CONCEPT 2: Generator Expressions vs List Comprehensions (Memory Battle)
# ================================================================================
# Lists store all elements in memory simultaneously. Generators evaluate values 
# lazily, requiring virtually zero memory overhead regardless of size.

print("--- Concept 2: Memory Consumption Comparison ---")
limit = 1_000_000

# 1. List Comprehension (Square brackets) -> Allocates memory for 1 million items immediately
list_comp = [x ** 2 for x in range(limit)]
list_memory = sys.getsizeof(list_comp)
print(f"List Comprehension Memory: {list_memory:,} bytes")

# 2. Generator Expression (Parentheses) -> Stores only the instruction to make the items
gen_exp = (x ** 2 for x in range(limit))
gen_memory = sys.getsizeof(gen_exp)
print(f"Generator Expression Memory: {gen_memory:,} bytes")
print(f"-> The Generator is roughly {list_memory // gen_memory}x more memory efficient!")
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Reading Massive Files Safely (Log Parser)
# ================================================================================
# If you attempt to open a 10GB server log file using file.readlines(), your RAM 
# will instantly saturate and crash your system. Generators stream it line-by-line.

# First, let's create a mockup log file string to simulate a real file payload
mock_log_data = """
2026-07-13 10:00:00 [INFO] System booted successfully.
2026-07-13 10:01:23 [WARNING] High memory usage detected.
2026-07-13 10:02:45 [ERROR] Database connection timed out.
2026-07-13 10:05:12 [INFO] User logged out.
""".strip().split('\n')

def log_reader_generator(log_lines):
    for line in log_lines:
        # Pretend we are reading lines lazily from a massive file stream
        yield line

def filter_errors(log_stream):
    for line in log_stream:
        if "[ERROR]" in line:
            yield f"CRITICAL INCIDENT ALERT: {line}"

print("--- Real-World 1: Pipelining / Streaming Log Files ---")
# We chain two generators together here. Neither holds the whole file in memory.
raw_stream = log_reader_generator(mock_log_data)
error_alerts = filter_errors(raw_stream)

# The parsing logic executes incrementally as the loop requests items!
for alert in error_alerts:
    print(alert)
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Infinite Data Streams (Unique Transaction ID Generator)
# ================================================================================
# Because generators generate values lazily, you can represent completely 
# infinite mathematical or procedural data series safely without crashing.

def transaction_id_generator(prefix="TXN"):
    sequence_number = 1001
    while True:  # Yes, an infinite loop is safe here because it pauses!
        yield f"{prefix}-{sequence_number}-{int(time.time())}"
        sequence_number += 1

print("--- Real-World 2: Infinite Unique Sequence Generator ---")
id_vault = transaction_id_generator("US-EAST")

# Generate IDs indefinitely on demand without running out of memory
print(f"Generated Order ID 1: {next(id_vault)}")
print(f"Generated Order ID 2: {next(id_vault)}")
time.sleep(1) # Simulating time gap
print(f"Generated Order ID 3: {next(id_vault)}")
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: State Tracking & Resetting (The Fibonacci Iterator)
# ================================================================================
# Generators remember the context variables internally. Here's how easily they
# calculate algorithmic values that depend heavily on previous states.

def fibonacci_generator(max_limit):
    a, b = 0, 1
    while a < max_limit:
        yield a
        a, b = b, a + b

print("--- Real-World 3: State Preservation (Fibonacci Sequence) ---")
# Generate Fibonacci numbers below 100
for fib_num in fibonacci_generator(100):
    print(fib_num, end=" ")
print("\n" + "-" * 50 + "\n")


# ================================================================================
# SUMMARY & TAKEAWAY
# ================================================================================
# Use generators when:
# 1. You are working with large datasets, long file processing, or big SQL queries.
# 2. You want to save RAM overhead.
# 3. You need to produce infinite data streams.
# 4. You want clean, pipelines that decouple data generation from data consumption.