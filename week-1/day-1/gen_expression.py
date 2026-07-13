"""
================================================================================
               PYTHON GENERATOR EXPRESSIONS: A COMPLETE TUTORIAL
================================================================================
Generator expressions are the high-performance, memory-saving siblings of 
list comprehensions. They allow you to create a generator object on the fly 
using a single line of code.

Syntax Breakdown:
- List Comprehension:      my_list = [x * 2 for x in range(10)]  # Evaluates instantly
- Generator Expression:   my_gen  = (x * 2 for x in range(10))  # Evaluates lazily
"""

import sys
import time

# ================================================================================
# CONCEPT 1: Syntax & Core Behavior
# ================================================================================
# Generator expressions look exactly like list comprehensions, but they use
# parentheses () instead of square brackets [].

print("--- Concept 1: Syntax Comparison ---")

# 1. List Comprehension creates the whole list in memory immediately
square_list = [n ** 2 for n in range(5)]
print(f"List Comprehension: {square_list}")
print(f"Type: {type(square_list)}")

# 2. Generator Expression creates a generator object that waits to produce values
square_gen = (n ** 2 for n in range(5))
print(f"\nGenerator Expression: {square_gen}")
print(f"Type: {type(square_gen)}")

# Extracting values from the generator expression:
print("Extracting values manually:")
print(next(square_gen))  # Output: 0
print(next(square_gen))  # Output: 1
print(list(square_gen))  # Consumes the remaining elements: [4, 9, 16]
print("-" * 50 + "\n")


# ================================================================================
# CONCEPT 2: Inline Aggregations & Memory Savings
# ================================================================================
# Generator expressions shine when passed directly into reduction functions like
# sum(), max(), min(), or join(). You don't even need double parentheses!

print("--- Concept 2: Efficient Aggregations ---")

# Calculate the sum of squares up to 10,000,000
# Notice we just pass the expression straight into sum() without extra brackets.
total_sum = sum(x ** 2 for x in range(10_000_000))
print(f"Sum of squares: {total_sum}")

# Memory check: Let's see how much memory that expression takes vs a list
list_memory = sys.getsizeof([x ** 2 for x in range(1_000_000)])
gen_memory = sys.getsizeof((x ** 2 for x in range(1_000_000)))

print(f"Memory used by List approach: {list_memory:,} bytes")
print(f"Memory used by Gen approach:  {gen_memory:,} bytes")
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Data Cleaning & Short-Circuit Optimization
# ================================================================================
# When using functions like any() or all(), generator expressions short-circuit. 
# This means they stop evaluating the moment they find a definitive answer, 
# saving massive amounts of compute time.

# A massive list of simulated server status logs
server_logs = ["OK"] * 500_000 + ["CRITICAL_FAILURE"] + ["OK"] * 500_000

print("--- Real-World 1: Short-Circuiting with any() ---")

start = time.perf_counter()
# The generator evaluates lazily. The moment it hits index 500,000 and finds
# "CRITICAL_FAILURE", any() stops executing completely.
has_failure = any(log == "CRITICAL_FAILURE" for log in server_logs)
end = time.perf_counter()

print(f"System has failure? {has_failure}")
print(f"Time taken to check 1,000,001 items: {end - start:.6f} seconds")
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Processing and Formatting Huge Lists of Dictionaries
# ================================================================================
# Imagine processing a massive stream of user database rows, extracting email 
# domains, filtering invalid entries, and feeding them to a mailing system.

users_db = [
    {"name": "Alice", "email": "alice@gmail.com", "active": True},
    {"name": "Bob", "email": "bob@yahoo.com", "active": False},
    {"name": "Charlie", "email": "charlie@outlook.com", "active": True},
    {"name": "InvalidUser", "email": "malformed_email", "active": True},
    {"name": "David", "email": "david@gmail.com", "active": True},
]

print("--- Real-World 2: Data Pipeline Transformation ---")

# Generator Expression 1: Filter active users and extract domains safely
domain_stream = (
    user["email"].split("@")[1] 
    for user in users_db 
    if user["active"] and "@" in user["email"]
)

# Generator Expression 2: Format them into clean strings (Chaining generators!)
formatted_output = (f"Target Domain: {domain.upper()}" for domain in domain_stream)

# No work has been done yet! The calculations happen only when we loop:
for targeting_line in formatted_output:
    print(targeting_line)
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Space-Efficient String Concatenation
# ================================================================================
# Joining lines or words from raw data can create massive intermediate lists.
# Generator expressions feed substrings directly to text streams.

words = ["Python", "Generator", "Expressions", "Are", "Incredibly", "Clean"]

print("--- Real-World 3: Memory-Safe String Join ---")

# Modifies text on the fly and builds the string without making an intermediate list
sentence = " | ".join(word.upper() for word in words)
print(sentence)
print("-" * 50 + "\n")


# ================================================================================
# SUMMARY & BEST PRACTICES
# ================================================================================
# 1. Use List Comprehensions when you absolutely need the index methods, slicing,
#    or intend to iterate over the data multiple times (Generators exhaust after 1 run).
# 2. Use Generator Expressions when passing data directly into aggregators (sum, max, join),
#    when dealing with huge/infinite streams, or when execution can benefit from short-circuiting.