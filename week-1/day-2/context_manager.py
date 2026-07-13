"""
================================================================================
                PYTHON CONTEXT MANAGERS & THE WITH STATEMENT
================================================================================
Resource management can be messy. When you open a file, connect to a database, 
or acquire a network socket, you must remember to close it. If your code crashes 
midway, resources stay leaked, locking up system memory or connection pools.

The `with` statement automates this process by defining a safe "setup" and 
"teardown" protocol, ensuring that clean-up logic runs no matter what happens 
inside the block—even if exceptions are raised.

There are two primary ways to create custom context managers:
1. Class-Based: Implementing `__enter__` and `__exit__` magic methods.
2. Generator-Based: Using the `@contextmanager` decorator from `contextlib`.
"""

import sqlite3
import time
from contextlib import contextmanager

# ================================================================================
# CONCEPT 1: The Eager/Manual Way vs. The 'with' Statement
# ================================================================================
# Traditionally, ensuring resources are closed requires tedious try/finally blocks.

print("--- Concept 1: Manual vs. Automatic Resource Management ---")

# The Old, Manual Way:
file_handle = open("demo_temp.txt", "w")
try:
    file_handle.write("Hello, Eager World!")
finally:
    # This guarantees the file closes even if write() crashes
    file_handle.close()
    print("[Manual] File safely closed via try/finally.")

# The Modern Way (Context Manager):
with open("demo_temp.txt", "w") as file_handle:
    file_handle.write("Hello, Clean World!")
# The file is AUTOMATICALLY closed the exact millisecond we exit the indented block.
print("[Automatic] File safely closed via 'with' statement.")
print("-" * 70 + "\n")


# ================================================================================
# CONCEPT 2: Building a Class-Based Context Manager
# ================================================================================
# To implement a class-based context manager, define two core magic methods:
# - `__enter__`: Sets up the resource and returns the object tied to the `as` target.
# - `__exit__`: Handles teardown. It receives details about any exceptions raised.

class CustomFileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"  [Class Enter] Opening file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file  # This is what gets assigned to the variable after 'as'

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("  [Class Exit] Running teardown/cleanup logic...")
        if self.file:
            self.file.close()
            
        # Error handling capability:
        if exc_type is not None:
            print(f"  [Class Exit] Caught an exception inside the block: {exc_val}")
            # Returning True suppresses the exception. 
            # Returning False (or None) allows the exception to propagate upward.
            return False 

print("--- Concept 2: Class-Based Context Manager ---")
with CustomFileOpener("custom_demo.txt", "w") as f:
    f.write("Writing via custom class!")
    print("  [Inside Block] Successfully wrote data.")

print("\n--- Testing Exception Safety ---")
try:
    with CustomFileOpener("custom_demo.txt", "w") as f:
        print("  [Inside Block] About to trigger a ZeroDivisionError...")
        result = 10 / 0
except ZeroDivisionError:
    print("[Main Scope] ZeroDivisionError was successfully caught here after cleanup ran!")
print("-" * 70 + "\n")


# ================================================================================
# CONCEPT 3: Generator-Based Context Managers (@contextmanager)
# ================================================================================
# Writing a class can be wordy. The `contextlib` module allows you to write a single 
# generator function instead. Everything before the `yield` statement is setup, 
# and everything after is teardown.

@contextmanager
def simple_tag_wrapper(tag_name):
    # Setup Phase
    print(f"<{tag_name}>")
    try:
        yield  # Pauses here, hands control back to the 'with' block body
    finally:
        # Teardown Phase (Always wrap in try/finally to ensure this part runs!)
        print(f"</{tag_name}>")

print("--- Concept 3: Generator-Based (@contextmanager) ---")
with simple_tag_wrapper("div"):
    print("   This content is wrapped cleanly inside HTML tags.")
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Database Transaction Management (Commit / Rollback)
# ================================================================================
# Context managers are crucial for database state operations. If queries fail, 
# we want to abort and rollback all changes to keep database records pristine.

class DatabaseTransaction:
    def __init__(self, db_name=":memory:"):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        print("[DB Connection] Opening connection and starting transaction...")
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # An error occurred inside the block! Roll back changes.
            print(f"[DB Rollback] Exception triggered ({exc_val}). Aborting updates!")
            self.connection.rollback()
        else:
            # No errors! Commit safely to the database.
            print("[DB Commit] No errors detected. Saving changes permanently.")
            self.connection.commit()
            
        self.connection.close()
        return True  # Suppress the exception to keep our demo script running smoothly

print("--- Real-World 1: Database Transaction Protection ---")
# Let's seed an in-memory test database structure
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INT, name TEXT)")
conn.commit()

# Case A: A successful database update
with DatabaseTransaction() as db:
    db.execute("CREATE TABLE accounts (user_id INT, balance REAL)")
    db.execute("INSERT INTO accounts VALUES (1, 500.00)")
    print("  [DB Operation] Queries executed cleanly.")

# Case B: An operation encountering an unexpected crash
with DatabaseTransaction() as db:
    db.execute("INSERT INTO accounts VALUES (2, 750.00)")
    print("  [DB Operation] Intentionally executing a faulty query next...")
    db.execute("INSERT INTO non_existent_table VALUES (99)") # Will crash!
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Performance Profiler (Execution Timer)
# ================================================================================
# You can use context managers to benchmark execution durations across isolated 
# blocks of processing logic effortlessly.

@contextmanager
def CodeBlockTimer(description):
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        print(f"⏱️  [Timer] Block '{description}' finished in {elapsed:.5f} seconds.")

print("--- Real-World 2: Runtime Code Block Timer ---")

with CodeBlockTimer("List Comprehension vs Loops"):
    # Code block execution being timed
    large_list = [x ** 2 for x in range(5_000_000)]

with CodeBlockTimer("Simulated Remote API Call Network Hold"):
    time.sleep(0.8)

print("-" * 70 + "\n")


# ================================================================================
# CLEANUP & SUMMARY
# ================================================================================
# Clean up files created during this tutorial session
import os
for temp_file in ["demo_temp.txt", "custom_demo.txt"]:
    if os.path.exists(temp_file):
        os.remove(temp_file)

# Summary:
# Use Context Managers whenever your code relies on resources that need initialization 
# and cleanup (files, DBs, thread locks, mock environments, sockets, configurations).