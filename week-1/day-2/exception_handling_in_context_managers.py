"""
================================================================================
          EXCEPTION HANDLING IN CONTEXT MANAGERS: A COMPLETE TUTORIAL
================================================================================
When an exception occurs inside a `with` block, Python doesn't immediately crash. 
Instead, it pauses execution, takes the exception information, and hands it 
directly to the context manager's exit hook.

This makes context managers incredibly powerful for:
1. Guaranteeing cleanup runs even during critical runtime crashes.
2. Silently swallowing/suppressing specific expected errors.
3. Intercepting raw technical errors and re-raising clean, user-friendly errors.

We will master exception handling using both Class-Based and Generator-Based approaches.
"""

import os
import sqlite3
import logging
from contextlib import contextmanager

# Setup basic configuration for real-world logging simulations
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ================================================================================
# CONCEPT 1: The Anatomy of __exit__ Arguments
# ================================================================================
# In a class-based context manager, if an exception is raised inside the `with` block, 
# Python invokes `__exit__` and passes three vital arguments describing the failure:
#   1. exc_type: The exception class (e.g., ValueError, ZeroDivisionError)
#   2. exc_val:  The actual exception object instance containing the error message.
#   3. exc_tb:   A traceback object containing the detailed call stack.
#
# If the block finishes WITHOUT an error, all three arguments are passed as None.



class ExceptionInspector:
    def __enter__(self):
        print("[Enter] Context active. Monitoring code inside the block...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("\n[Exit] Block execution finished. Inspecting states:")
        print(f"  -> Exception Type:  {exc_type}")
        print(f"  -> Exception Value: {exc_val}")
        print(f"  -> Traceback Found: {exc_tb is not None}")
        
        # Fundamental Rule of __exit__:
        # Return True  -> "I handled this error. Swallow it and continue safely."
        # Return False -> "Propagate this error out to the main program execution." (Default behavior if no return)
        if exc_type is IndexError:
            print("  [Exit Decision] Index Error identified! Swallowing it safely.")
            return True 
        
        print("  [Exit Decision] No error, or unknown error. Letting normal flow handle it.")
        return False

print("--- Concept 1: The Exception Inspector Lifecycle ---")

# Case A: An error occurs that we want to suppress
with ExceptionInspector():
    print("  [Inside Block] Attempting an invalid list look-up...")
    numbers = [1, 2, 3]
    flawed_lookup = numbers[99] # Triggers IndexError

print("\nExecution safely continued past Case A because the error was swallowed.")

# Case B: No error occurs
print("\nStarting Case B:")
with ExceptionInspector():
    print("  [Inside Block] Doing safe operations.")
print("-" * 75 + "\n")


# ================================================================================
# CONCEPT 2: Exception Handling in Generator Contexts (@contextmanager)
# ================================================================================
# For generator-based context managers, exceptions raised inside the `with` block 
# are injected directly back into the generator at the point of the `yield` statement.
# Therefore, to manage exceptions, you wrap the `yield` statement in a standard 
# try/except/finally block!

@contextmanager
def generator_exception_handler():
    print("[Gen Setup] Preparing resource allocations...")
    try:
        yield  # Hand control over to the 'with' block body
        print("[Gen Success] The block finished completely without exceptions.")
    except ZeroDivisionError as err:
        print(f"[Gen Except] Intercepted math error: {err}. Resolving gracefully.")
    finally:
        print("[Gen Finally] Absolute Teardown running. This ALWAYS executes!")

print("--- Concept 2: Exception Management in Generators ---")
with generator_exception_handler():
    print("  [Inside Block] Calculating equations...")
    unstable_math = 50 / 0  # Triggers ZeroDivisionError

print("Program flows forward unbroken.")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Database Transaction Rollback Safety Gate
# ================================================================================
# Financial or inventory operations require atomicity: all operations must succeed, 
# or all operations must be undone (rolled back) to prevent data corruption.

class DBTransactionGuard:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        # Obtain query execution cursor
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Something crashed mid-transaction! Wipe operations clean.
            logging.error(f"Database transaction crashed: '{exc_val}'. Initiating emergency ROLLBACK...")
            self.connection.rollback()
            return False # Allow the error to propagate so the system knows the purchase failed
        else:
            # Everything ran perfectly. Save changes permanently.
            logging.info("Transaction executed flawlessly. Issuing permanent COMMIT.")
            self.connection.commit()
        return True

print("--- Real-World 1: Database Transaction Guard ---")
# Build a mockup in-memory user account database
db_conn = sqlite3.connect(":memory:")
cursor = db_conn.cursor()
cursor.execute("CREATE TABLE inventory (item TEXT, stock INT)")
cursor.execute("INSERT INTO inventory VALUES ('Smartphone', 5)")
db_conn.commit()

# Scenario: An invalid database query executed during checkout
try:
    with DBTransactionGuard(db_conn) as db:
        db.execute("UPDATE inventory SET stock = stock - 1 WHERE item = 'Smartphone'")
        print("  [DB Worker] Stock updated. Executing broken query next...")
        db.execute("UPDATE non_existent_table SET data = 1") # Crashes runtime
except sqlite3.OperationalError:
    print("[App Root] Gracefully caught database exception outside the context manager.")

# Check database state to confirm rollback protected the stock
cursor.execute("SELECT stock FROM inventory WHERE item = 'Smartphone'")
print(f"Current Stock Count: {cursor.fetchone()[0]} (Should still be 5!)")
db_conn.close()
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Silent Asset Deletion (Ignore Specific File Errors)
# ================================================================================
# During system folder cleanup processes, you often want to delete runtime lockfiles.
# If the file was already deleted by another process, os.remove() raises a FileNotFoundError.
# Instead of writing messy try/except tags everywhere, encapsulate it in a context manager.

@contextmanager
def suppress_file_errors():
    try:
        yield
    except FileNotFoundError:
        # Ignore this specific error silently because the desired end state matches (file is gone)
        logging.warning("FileNotFoundError intercepted and suppressed. End-state goal met.")
    except PermissionError as err:
        # Do NOT ignore permission problems! Re-raise it immediately.
        logging.critical("Security error identified. Propagating up!")
        raise err

print("--- Real-World 2: Silent Workspace Cleanup ---")

with suppress_file_errors():
    print("  [Cleanup] Attempting to remove an already deleted tracking asset file...")
    os.remove("ghost_file_2026.tmp")  # Triggers FileNotFoundError

print("Workspace operation finished moving forward smoothly without crashing.")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: API Sanitizer (Error Translation Masking)
# ================================================================================
# Exposing deep internal runtime backends directly to a web user interface is 
# a massive security vulnerability. We can use a context manager to intercept raw 
# network errors and translate them into friendly, stylized system exceptions.

class APIInternalError(Exception):
    """Custom high-level wrapper exception for our application domain layer."""
    pass

class APINetworkSanitizer:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, ConnectionError):
            # Intercept raw infrastructure failure logs
            logging.error(f"[Ops Log] Raw Infrastructure Failure detected: {exc_val}")
            
            # Mask and re-raise as a clean domain exception
            raise APIInternalError("Our service providers are currently timing out. Please try again shortly.") from None
        return False

print("--- Real-World 3: API Error Sanitization ---")

try:
    with APINetworkSanitizer():
        print("  [API Call] Querying remote external billing engine...")
        raise ConnectionResetError("TCP Reset by peer on port 443") # Simulate server failure
except APIInternalError as clean_app_error:
    print(f"\n[Client UI Screen received]: {clean_app_error}")
print("-" * 75 + "\n")


# ================================================================================
# SUMMARY OF BEST PRACTICES
# ================================================================================
# 1. Class-Based (`__exit__`): Return True to swallow exceptions, return False 
#    or None to let them propagate outwards.
# 2. Generator-Based (`@contextmanager`): Always place your `yield` statement 
#    inside a try/except/finally block to guarantee cleanup logic fires when errors hit.
# 3. Only suppress exceptions if the failure explicitly fulfills the application's 
#    functional target parameters. Never broadly suppress all BaseExceptions (`return True` unconditionally).