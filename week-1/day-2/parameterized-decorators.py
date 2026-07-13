"""
================================================================================
               PARAMETERIZED DECORATORS IN PYTHON: A COMPLETE TUTORIAL
================================================================================
Standard decorators only take one argument: the function they are decorating.
But what if you want to configure your decorator's behavior on the fly? 
For example:
  @repeat(num_times=3)
  @require_permission(role="admin")
  @rate_limit(calls_per_minute=60)

The Secret: The Decorator Factory (The 3-Layer Structure)
To pass arguments to a decorator, you must add an outer wrapper function. 
This outer function accepts the configuration arguments and returns the actual 
decorator, which then handles the target function as usual.

The Architecture Stack:
  Layer 1: Decorator Factory -> Accepts the custom configuration parameters.
  Layer 2: Decorator         -> Accepts the target execution function.
  Layer 3: Wrapper           -> Accepts the function's arguments (*args, **kwargs).
"""

import functools
import time
import random

# ================================================================================
# CONCEPT 1: The Three-Layer Blueprint
# ================================================================================
# Let's build a basic decorator that repeats a function execution a configurable
# number of times. Notice the three distinct 'def' statements.

def repeat(num_times):
    """Layer 1: The Factory - Receives the configuration parameter."""
    
    def decorator_repeat(func):
        """Layer 2: The Actual Decorator - Receives the core function."""
        
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            """Layer 3: The Wrapper - Receives the runtime function arguments."""
            result = None
            for i in range(num_times):
                print(f"[Repeat Loop] Running execution loop {i+1}/{num_times}...")
                result = func(*args, **kwargs)
            return result  # Returns the final execution result
            
        return wrapper_repeat
    return decorator_repeat

print("--- Concept 1: The 3-Layer Parameterized Structure ---")

@repeat(num_times=3)
def greet(name):
    print(f"   Hello, {name}!")

greet("Alice")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Parameterized Role-Based Access Control (RBAC)
# ================================================================================
# In enterprise software systems, different API endpoints or service modules 
# require distinct security clearances. Passing the permission string to the 
# decorator keeps verification logic elegant and clean.

# Simulated global current session state
CURRENT_USER_SESSION = {"username": "dev_coder", "clearance": "manager"}

def require_permission(required_clearance):
    """Decorator factory that configures custom authorization security barriers."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_clearance = CURRENT_USER_SESSION.get("clearance")
            
            # Hierarchical check simulation
            clearance_levels = {"guest": 1, "manager": 2, "admin": 3}
            
            if clearance_levels.get(user_clearance, 0) < clearance_levels.get(required_clearance, 0):
                print(f"🔒 [Security Error] Access Denied! '{func.__name__}' requires '{required_clearance}' status. "
                      f"User '{CURRENT_USER_SESSION['username']}' only has '{user_clearance}' clearance.")
                return None
                
            print(f"🔓 [Security Cleared] User authorized for level: '{required_clearance}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator

print("--- Real-World 1: Configurable Security Gates ---")

@require_permission(required_clearance="guest")
def view_dashboard():
    print("   -> Showing generalized generic graphs dashboard UI...")

@require_permission(required_clearance="admin")
def modify_system_billing():
    print("   -> ⚠️  CRITICAL: Financial variables updated successfully.")

# Test A: Expect success (manager >= guest)
view_dashboard()
print()
# Test B: Expect security rejection (manager < admin)
modify_system_billing()
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Specialized Execution Metric Logger
# ================================================================================
# You can use parameters to direct where logs are routed, change log formatting, 
# or tag metrics with custom context identifiers depending on the deployment layer.

def metric_logger(component_name, log_level="INFO"):
    """Tracks metrics and prints them with custom operational tags."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            
            # Execute original function logic
            result = func(*args, **kwargs)
            
            duration = time.perf_counter() - start_time
            print(f"[{log_level}] Component: {component_name} | Function: {func.__name__} | "
                  f"Latency: {duration:.5f}s")
            return result
        return wrapper
    return decorator

print("--- Real-World 2: Custom Component Metric Tracking ---")

@metric_logger(component_name="DATABASE_LAYER", log_level="DEBUG")
def fetch_user_profile(user_id):
    time.sleep(0.15)  # Simulate network latency
    return {"id": user_id, "name": "Bob Smith"}

@metric_logger(component_name="AI_ENGINE", log_level="CRITICAL")
def running_neural_inference():
    time.sleep(0.4)  # Simulate model load
    return "Inference matrix generation finalized."

fetch_user_profile("usr_404")
running_neural_inference()
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Adaptive Performance Caching Tool
# ================================================================================
# Let's build a real cache mechanism that allows developers to flag distinct 
# evaluation categories, specifying whether empty values should be skipped.

def smart_cache(cache_nulls=False):
    """Advanced closure pattern preserving independent unique local memory lookups."""
    def decorator(func):
        # Local lookup cache unique to this decorated instance function structure
        local_memory_vault = {}
        
        @functools.wraps(func)
        def wrapper(*args):
            # Args acts as the dictionary tuple memory lookup key
            if args in local_memory_vault:
                print(f"   [Cache Hit] Returning stored value for inputs {args}")
                return local_memory_vault[args]
                
            print(f"   [Cache Miss] Computing heavy logic for inputs {args}...")
            value_generated = func(*args)
            
            # Conditionally handle empty/None attributes based on decorator parameters
            if value_generated is None and not cache_nulls:
                print("   [Cache Warning] Discarding None value calculation per configuration criteria.")
                return value_generated
                
            local_memory_vault[args] = value_generated
            return value_generated
        return wrapper
    return decorator

print("--- Real-World 3: Adaptive Memory Cache Control ---")

@smart_cache(cache_nulls=False)
def search_inventory_index(item_id):
    # Simulate a database search that returns None if an item isn't found
    if item_id == 777:
        return "High-End Smartphone Asset"
    return None

print("Pass 1: Requesting valid product id 777:")
print(f"Result: {search_inventory_index(777)}")
print("\nPass 2: Requesting product id 777 again (Expect Cache Hit):")
print(f"Result: {search_inventory_index(777)}")

print("\nPass 3: Requesting missing item id 999 (Returns None):")
print(f"Result: {search_inventory_index(999)}")
print("\nPass 4: Requesting missing item id 999 again (Expect Cache Miss again, because cache_nulls=False):")
print(f"Result: {search_inventory_index(999)}")
print("-" * 75 + "\n")


# ================================================================================
# SUMMARY & TAKEAWAY CHEAT SHEET
# ================================================================================
# 1. Parameterized decorators require a 3-layer architecture stack: Factory -> Decorator -> Wrapper.
# 2. The outermost layer handles configuring data parameters, the middle layer handles 
#    functional references, and the inner layer deals with positional parameter processing.
# 3. Always apply `@functools.wraps(func)` on Layer 3 (the inner wrapper) to maintain 
#    clean metadata transparency across application code review frameworks.
