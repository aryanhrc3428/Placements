"""
================================================================================
              UNDERSTANDING __enter__ AND __exit__: A COMPLETE TUTORIAL
================================================================================
In Python, any class that implements the context management protocol can be used 
with the `with` statement. This protocol is governed by two special methods:

1. __enter__(self):
   - Executes when control flow enters the `with` block.
   - It sets up the required resource (opens a file, locks a thread, connects to an API).
   - Whatever it returns is bound to the target variable defined after the `as` keyword.

2. __exit__(self, exc_type, exc_val, exc_tb):
   - Executes automatically when control leaves the `with` block (even if a crash happens).
   - It cleans up the resource (closes files, unlocks threads, disconnects APIs).
   - If an exception occurred inside the block, its details are passed into the 
     three parameters: type, value, and traceback.
"""

import os
import time

# ================================================================================
# CONCEPT 1: The Lifecycle Protocol
# ================================================================================
# Let's look at the chronological order of execution to see exactly when Python 
# triggers these two underlying methods.

class LifecycleDemo:
    def __init__(self, block_name):
        self.block_name = block_name
        print(f"[1. __init__] Initialized object for block: '{self.block_name}'")

    def __enter__(self):
        print(f"[2. __enter__] Entering the context code gate. Allocating resource...")
        return f"Tethered-Value-from-{self.block_name}"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[4. __exit__] Leaving the context code gate. Cleaning up resource...")
        # Returning None or False tells Python: "If there was an error, let it crash normally."
        return False 

print("--- Concept 1: The Context Manager Lifecycle ---")
with LifecycleDemo("Test_Run") as bound_variable:
    print(f"[3. Inside Block] Variable bound after 'as': {bound_variable}")
    print("   Executing core logic inside the indented block...")

print("Execution successfully past the 'with' scope block structure.")
print("-" * 75 + "\n")


# ================================================================================
# CONCEPT 2: Exception Interception and Suppression
# ================================================================================
# `__exit__` acts as a security guard for exceptions. You can inspect errors and 
# choose whether to let them crash the script or silently swallow them.

class ExceptionHandlerDemo:
    def __enter__(self):
        print("  [Enter] Resource ready.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("  [Exit] Checking for runtime structural errors...")
        
        if exc_type is not None:
            print(f"  [Exit] 🚨 Caught an error of type: {exc_type.__name__}")
            print(f"  [Exit] Error Message: {exc_val}")
            
            if exc_type is ZeroDivisionError:
                print("  [Exit] Actively swallowing ZeroDivisionError! Program will continue safely.")
                return True # Returning True suppresses/swallows the exception
                
        print("  [Exit] Cleanup done. No exceptions suppressed.")
        return False # Returning False propagates the exception out to the main engine

print("--- Concept 2: Exception Handling and Suppression Rules ---")

# Scenario A: Swallowing a specific known exception type
with ExceptionHandlerDemo():
    print("  [Inside Block] Dividing by zero now...")
    crash_test = 10 / 0 

print("\nScenario A complete. Notice the script didn't terminate!")

# Scenario B: Letting an unexpected exception bubble up normally
print("\nStarting Scenario B (Will be caught outside by a standard try-except block):")
try:
    with ExceptionHandlerDemo():
        print("  [Inside Block] Attempting to access an undefined variable name...")
        print(missing_variable) # Triggers NameError
except NameError:
    print("[Main Scope Root] Caught NameError safely outside the Context Manager!")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Secure SFTP / Remote Service Connection Manager
# ================================================================================
# When opening remote client communication interfaces, it is vital to guarantee 
# disconnection sequences execute so remote ports aren't locked open indefinitely.

class RemoteSSHClientMock:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_connected = False

    def __enter__(self):
        print(f"[Network] Establishing secure channel handshake to {self.host}:{self.port}...")
        time.sleep(0.3)  # Simulate latency
        self.is_connected = True
        return self  # Return the client instance to invoke methods on it

    def send_command(self, cmd):
        if not self.is_connected:
            raise RuntimeError("Cannot execute command. Not connected to a session.")
        print(f"  [SSH Session] Running: '{cmd}' -> Output: Success.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[Network] Severing active SSH sockets cleanly on port {self.port}...")
        self.is_connected = False
        print("[Network] Session disconnected successfully.")
        return False

print("--- Real-World 1: Secure Remote Infrastructure Channel ---")
with RemoteSSHClientMock("10.0.4.11", port=22) as client:
    client.send_command("docker ps")
    client.send_command("cat /var/log/nginx/access.log")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Thread-Safe Concurrency Lock Simulator
# ================================================================================
# In concurrent multithreaded jobs, multiple workers might try to modify a single 
# item simultaneously, corrupting data. Context managers isolate critical operations.

class DatabaseWriteLock:
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.is_locked = False

    def __enter__(self):
        print(f"[Concurrency Lock] Acquiring EXCLUSIVE lock on structural table: '{self.resource_name}'")
        self.is_locked = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[Concurrency Lock] Releasing lock on table: '{self.resource_name}'. Other processes may now write.")
        self.is_locked = False
        return False

print("--- Real-World 2: Thread/Database Resource Locking ---")
shared_ledger = {"balance": 1500}

with DatabaseWriteLock("UserAccountsTable"):
    print("  [Critical Section] Modifying system values safely...")
    shared_ledger["balance"] -= 200
    print(f"  [Critical Section] Modification successful. New Balance: ${shared_ledger['balance']}")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Temporary Working Directory Switcher
# ================================================================================
# Scripts often need to switch directories to process local assets, but failing 
# to switch back to the original operational path causes absolute chaos downstream.

class TempDirectorySwitcher:
    def __init__(self, target_directory):
        self.target_directory = target_directory
        self.original_directory = os.getcwd()

    def __enter__(self):
        print(f"[Dir Switcher] Stashing current working directory: {self.original_directory}")
        # Note: In a production environment, you would ensure the directory exists first.
        # os.chdir(self.target_directory)
        print(f"[Dir Switcher] Temporarily jumped to path: {self.target_directory}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always return control home regardless of any errors encountered inside
        # os.chdir(self.original_directory)
        print(f"[Dir Switcher] Reverting safely back to original path: {self.original_directory}")
        return False

print("--- Real-World 3: Automated Working Directory Control ---")
with TempDirectorySwitcher("/var/tmp/data_processor"):
    print("  [Operation Scope] Reading local logs inside raw path...")
    # Perform OS work here
    print("  [Operation Scope] Complete.")
print("-" * 75 + "\n")


# ================================================================================
# CRITICAL SUMMARY FOR EXAMS & CODE DESIGN
# ================================================================================
# 1. `__enter__` sets up and returns the active asset resource.
# 2. `__exit__` acts as an absolute safety engine, cleaning up connections or states.
# 3. If `__exit__` returns `True`, it silences errors. If it returns `False`, errors 
#    bubble up to standard handling scopes.