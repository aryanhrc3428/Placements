"""
================================================================================
                       PYTHON DECORATORS: A COMPLETE TUTORIAL
================================================================================
A decorator is a design pattern in Python that allows you to modify or extend 
the behavior of a function or method without permanently changing its source code.

Think of it like wrapping a gift: the gift inside (your function) stays the same, 
but the wrapping paper (the decorator) adds extra flair or functionality before 
and after it's opened.
"""

import time
from functools import wraps

# ================================================================================
# CONCEPT 1: Functions as First-Class Citizens
# ================================================================================
# In Python, functions can be passed around as arguments, returned from other 
# functions, and assigned to variables. This is the foundation of decorators.

def greet(name):
    return f"Hello, {name}!"

def execute_function(func, value):
    # We are passing a function as an argument here
    return func(value)

print("--- Concept 1: First-Class Functions ---")
print(execute_function(greet, "Alice"))  # Output: Hello, Alice!
print("-" * 40 + "\n")


# ================================================================================
# CONCEPT 2: The Basic Decorator Structure
# ================================================================================
# A decorator is simply a function that takes another function as an argument,
# wraps its behavior in a nested function, and returns that nested function.

def simple_decorator(original_function):
    def wrapper_function():
        print("[Before] Doing something before the function runs...")
        original_function()
        print("[After] Doing something after the function runs...")
    return wrapper_function

# The Standard Way to use a decorator is using the '@' symbol syntax:
@simple_decorator
def say_hello():
    print("   -> Hello World! (Inside the core function)")

print("--- Concept 2: Basic Decorator ---")
say_hello()
print("-" * 40 + "\n")


# ================================================================================
# CONCEPT 3: Decorating Functions that Accept Arguments
# ================================================================================
# To make a decorator universal, the inner wrapper function must accept 
# *args and **kwargs so it can handle any arguments passed to the original function.

def universal_decorator(original_function):
    def wrapper_function(*args, **kwargs):
        print(f"[Log] Calling {original_function.__name__} with args: {args}")
        result = original_function(*args, **kwargs)
        print(f"[Log] {original_function.__name__} finished execution.")
        return result  # Don't forget to return the original function's result!
    return wrapper_function

@universal_decorator
def add_numbers(a, b):
    return a + b

print("--- Concept 3: Handling Arguments ---")
sum_result = add_numbers(5, 7)
print(f"Result of addition: {sum_result}")
print("-" * 40 + "\n")


# ================================================================================
# CONCEPT 4: Preserving Identity with functools.wraps
# ================================================================================
# When you decorate a function, it technically becomes the wrapper function. 
# To prevent losing the original function's name and docstring, always use 
# `@wraps(original_function)` from the built-in `functools` module.

def proper_decorator(original_function):
    @wraps(original_function)  # Preserves metadata
    def wrapper(*args, **kwargs):
        return original_function(*args, **kwargs)
    return wrapper

@proper_decorator
def identity_test():
    """This is a very important docstring."""
    pass

print("--- Concept 4: Preserving Metadata ---")
print(f"Function Name: {identity_test.__name__}")  # Output: identity_test
print(f"Docstring:     {identity_test.__doc__}")   # Output: This is a very important docstring.
print("-" * 40 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Performance Timer (Profiling)
# ================================================================================
# A common real-world use case is measuring how long a function takes to execute.

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"[Timer] Function '{func.__name__}' took {execution_time:.6f} seconds to run.")
        return result
    return wrapper

@timer_decorator
def heavy_computation():
    print("Starting heavy processing...")
    time.sleep(1.5)  # Simulating a heavy network request or database operation
    print("Processing complete.")

print("--- Real-World 1: Execution Timer ---")
heavy_computation()
print("-" * 40 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Authentication & Authorization Sim
# ================================================================================
# Decorators are heavily used in web frameworks (like Flask or Django) to restrict 
# access to certain routes based on user permissions.

# Simulation of a global current user session
CURRENT_USER = {"username": "dev_user", "is_authenticated": True, "role": "admin"}

def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not CURRENT_USER.get("is_authenticated"):
            print("[Auth Error] User is not logged in!")
            return None
        if CURRENT_USER.get("role") != "admin":
            print(f"[Auth Error] User '{CURRENT_USER['username']}' is not authorized to perform this action!")
            return None
        return func(*args, **kwargs)
    return wrapper

@require_admin
def delete_user_database():
    print("[Success] Danger Zone! Database successfully wiped out.")

print("--- Real-World 2: Authorization Check ---")
# Case A: Admin access (Should succeed)
print("Attempt 1 (As Admin):")
delete_user_database()

# Case B: Demoting user to standard user (Should fail)
print("\nAttempt 2 (As Standard User):")
CURRENT_USER["role"] = "standard_user"
delete_user_database()
print("-" * 40 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Basic Caching / Memoization
# ================================================================================
# If a function is expensive, you can cache its results to avoid doing the same 
# work twice for identical inputs.

def memoize(func):
    cache = {}  # This dictionary persists in memory thanks to closures
    
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"[Cache Hit] Fetching result for {args} from memory.")
            return cache[args]
        
        print(f"[Cache Miss] Calculating result for {args}...")
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@memoize
def expensive_multiplication(n):
    time.sleep(1) # Simulate delay
    return n * 2

print("--- Real-World 3: Caching Results ---")
print(expensive_multiplication(10)) # Calculates (Takes 1 second)
print(expensive_multiplication(10)) # Instant! Fetched from cache
print(expensive_multiplication(5))  # Calculates (Takes 1 second)
print(expensive_multiplication(10)) # Instant! Fetched from cache
print("-" * 40)