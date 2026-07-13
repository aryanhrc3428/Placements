"""
================================================================================
                    NESTED CONTEXT MANAGERS: A COMPLETE TUTORIAL
================================================================================
In real-world applications, you rarely manage just one resource at a time. 
Often, you need to read from one file while writing to another, acquire multiple 
thread locks simultaneously, or open a database transaction while streaming to a log.

Python allows you to nest context managers so that multiple resources are handled 
together. The runtime guarantees that ALL entered contexts will execute their 
clean-up/teardown logic (`__exit__`), regardless of success or failure.

Evolution of Syntax:
1. Historical Way:  Deeply nested, heavily indented individual 'with' blocks.
2. Modern Way:      Comma-separated context managers on a single line.
3. Multi-line Way:  Parentheses-wrapped groups (Python 3.10+).
4. Dynamic Way:     'contextlib.ExitStack' for handling an unknown number of resources.
"""

import os
import sqlite3
from contextlib import ExitStack, contextmanager

# Setup dummy files for the concepts
with open("source_raw.txt", "w") as f:
    f.write("Line 1: Raw Data\nLine 2: Raw Data\n")


# ================================================================================
# CONCEPT 1: The Evolution of Nested Syntax
# ================================================================================
# Let's look at how Python evolved to prevent the "arrow anti-pattern" (excessive indentation).

print("--- Concept 1: Syntax Layouts ---")

# 1. The Legacy/Nested Indentation Way (Pre-Python 3.1 style, still valid but wordy)
with open("source_raw.txt", "r") as src:
    with open("dest_nested.txt", "w") as dest:
        dest.write(src.read().upper())
print("[Legacy] Successfully transferred data using stacked blocks.")

# 2. The Modern Comma-Separated Way (Python 3.1+)
with open("source_raw.txt", "r") as src, open("dest_comma.txt", "w") as dest:
    dest.write(src.read().replace("Raw", "Processed"))
print("[Modern] Successfully transferred data using comma-separated syntax.")

# 3. The Multi-line Parentheses Way (Python 3.10+)
# This is incredibly useful when file paths are long and you want clean formatting.
with (
    open("source_raw.txt", "r") as src,
    open("dest_multiline.txt", "w") as dest
):
    dest.write(src.read())
print("[Multi-line] Successfully transferred data using parenthesized syntax.")
print("-" * 75 + "\n")


# ================================================================================
# CONCEPT 2: Order of Execution (First In, Last Out)
# ================================================================================
# When nesting context managers, they behave exactly like a Stack (LIFO - Last In, First Out).
# The first manager entered is the LAST manager exited.

@contextmanager
def dummy_context(name):
    print(f"  [→ Enter] Open Context: {name}")
    try:
        yield
    finally:
        print(f"  [← Exit]  Close Context: {name}")

print("--- Concept 2: The Order of Teardown ---")
with dummy_context("Manager_A"), dummy_context("Manager_B"), dummy_context("Manager_C"):
    print("     ★ [Inside Block] Executing code core logic...")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Simultaneous File I/O (Streaming Data Transfer)
# ================================================================================
# Imagine processing a huge log file. You cannot read the whole file into memory, 
# nor can you open/close files iteratively. You must stream line-by-line using 
# dual context handles.

print("--- Real-World 1: Line-by-Line Log Transformer ---")

# Generating a mockup messy log file
with open("server_dirty.log", "w") as f:
    f.write("INFO: User login\nDEBUG: Internal trace\nERROR: Database timeout\n")

# Open both the reader and writer context concurrently
with open("server_dirty.log", "r") as infile, open("server_clean.log", "w") as outfile:
    for line in infile:
        if "DEBUG" not in line:  # Filter out noise on the fly
            outfile.write(f"[PROCESSED] {line}")

print("  Log processing complete. Clean log generated without memory bloat.")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Database Audit Pipeline (DB Txn + File Sync)
# ================================================================================
# When making critical financial modifications in a database, you often want to 
# write to an external encrypted security audit text log concurrently. If either 
# system fails, the whole block must fail gracefully.

class AuditLogger:
    def __enter__(self):
        print("[Audit Log] Opening security write channel...")
        self.file = open("security_audit.txt", "a")
        return self
    def log(self, text):
        self.file.write(f"AUDIT: {text}\n")
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[Audit Log] Flushing buffers and closing channel.")
        self.file.close()
        return False # Do not swallow exceptions

print("--- Real-World 2: Dual Target Transaction Processing ---")

# Setup an in-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE accounts (user TEXT, balance REAL)")
cursor.execute("INSERT INTO accounts VALUES ('Alice', 1000.0)")
conn.commit()

# Nesting the DB connection context manager and our Custom Audit Logger
with conn, AuditLogger() as logger:
    # `with conn:` automatically handles commits if successful, rollbacks if crashed.
    print("  [Action] Initiating fund transfer...")
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE user = 'Alice'")
    logger.log("Transferred $100 from Alice's Account.")
    
    # Check updated balance
    cursor.execute("SELECT balance FROM accounts WHERE user = 'Alice'")
    print(f"  [DB Current Status] Alice's New Balance: ${cursor.fetchone()[0]}")

print("Transaction completed and secure audit trail locked away.")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Dynamic Nesting using ExitStack
# ================================================================================
# What happens if you need to open 3 files today, but 50 files tomorrow? You cannot 
# hardcode comma-separated variables into your `with` statement. 
# `contextlib.ExitStack` lets you register a dynamic list of context managers programmatically.

print("--- Real-World 3: Batch File Merger via ExitStack ---")

# Let's create a few separate chunk files dynamically
chunk_names = ["chunk_part1.dat", "chunk_part2.dat", "chunk_part3.dat"]
for index, name in enumerate(chunk_names, start=1):
    with open(name, "w") as chunk:
        chunk.write(f"Part {index} payload data. ")

# We want to open all chunks simultaneously, read them, and stitch them to a master file
with ExitStack() as stack:
    print("Dynamically opening all chunk streams...")
    # Enter the master file destination context manager
    master_file = stack.enter_context(open("combined_master.dat", "w"))
    
    # Enter an arbitrary number of source context managers safely in a loop
    opened_file_handles = [stack.enter_context(open(name, "r")) for name in chunk_names]
    
    # Process all resources now that they are concurrently secured open
    print("Streaming and merging payloads...")
    for handle in opened_file_handles:
        master_file.write(handle.read())

print("ExitStack closed. All resource hooks successfully cleared.")
with open("combined_master.dat", "r") as master:
    print(f"Final Merged File Content: {master.read()}")
print("-" * 75 + "\n")


# ================================================================================
# HOUSEKEEPING: CLEANUP TEMPORARY TUTORIAL FILES
# ================================================================================
print("Cleaning up tutorial assets...")
temporary_files = [
    "source_raw.txt", "dest_nested.txt", "dest_comma.txt", "dest_multiline.txt",
    "server_dirty.log", "server_clean.log", "security_audit.txt",
    "chunk_part1.dat", "chunk_part2.dat", "chunk_part3.dat", "combined_master.dat"
]
for temp_file in temporary_files:
    if os.path.exists(temp_file):
        os.remove(temp_file)
print("Cleanup complete. Environment pristine.")