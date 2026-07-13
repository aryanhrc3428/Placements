"""
================================================================================
                 MASTERING functools.wraps: A COMPLETE TUTORIAL
================================================================================
When you decorate a function, you are essentially replacing the original function 
with a nested wrapper function. 

The Major Flaw:
By default, this replacement causes the original function to lose its identity! 
Its name (`__name__`), documentation strings (`__doc__`), and type annotations 
are overwritten by the inner wrapper's metadata. This ruins debugging, breaks 
introspection tools, and completely scrambles automatic API documentation engines.

The Savior: `functools.wraps`
This is a built-in decorator that you apply to your inner wrapper function. It 
automatically copies all the original metadata back onto the wrapper, keeping 
your code pristine and transparent.
"""

import functools
import time
import logging

# Setup basic configuration for real-world logging simulations
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ================================================================================
# CONCEPT 1: The Problem (Metadata Identity Theft)
# ================================================================================
# Let's see what happens when we build a standard decorator WITHOUT using wraps.

def broken_decorator(func):
    def wrapper(*args, **kwargs):
        print("[Broken Decorator] Executing preprocessing...")
        return func(*args, **kwargs)
    return wrapper

@broken_decorator
def calculate_area(width, height):
    """Computes the geographic footprint area of a property lot."""
    return width * height

print("--- Concept 1: The Metadata Loss Problem ---")
# Let's execute the function
print(f"Result: {calculate_area(10, 20)}")

# Let's inspect the function's identity attributes:
print(f"Intended Name: calculate_area  | Actual Name: {calculate_area.__name__}")
print(f"Intended Doc:  Computes the... | Actual Doc:  {calculate_area.__doc__}")

print("\n🚨 Notice how the function now thinks its name is 'wrapper' and its docstring is completely gone!")
print("-" * 75 + "\n")


# ================================================================================
# CONCEPT 2: The Solution (Restoring Identity with functools.wraps)
# ================================================================================
# By adding `@functools.wraps(func)` right above our inner wrapper, the identity 
# crisis is instantly solved.

def correct_decorator(func):
    @functools.wraps(func)  # The magic fix! Copies metadata from 'func' to 'wrapper'
    def wrapper(*args, **kwargs):
        print("[Correct Decorator] Executing preprocessing...")
        return func(*args, **kwargs)
    return wrapper

@correct_decorator
def calculate_volume(width, height, depth):
    """Computes the cubic capacity volume of an asset container."""
    return width * height * depth

print("--- Concept 2: Identity Preserved via @functools.wraps ---")
print(f"Result: {calculate_volume(10, 20, 5)}")

# Let's re-inspect the metadata:
print(f"Actual Name: {calculate_volume.__name__}")
print(f"Actual Doc:  {calculate_volume.__doc__}")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Production Application Logger (Traceability)
# ================================================================================
# In production microservices, when an error occurs, the logger needs to output 
# the exact name of the function that failed. If metadata is lost, your logs 
# will misleadingly claim every single failure occurred in a function named 'wrapper'.

def operational_tracer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"⚡ [System Audit] Entering execution layer: '{func.__name__}'")
        try:
            result = func(*args, **kwargs)
            logging.info(f"✅ [System Audit] Exiting layer: '{func.__name__}' successfully.")
            return result
        except Exception as e:
            # Crucial: Without wraps, logging func.__name__ here would print 'wrapper'
            logging.error(f"❌ [CRITICAL FAILURE] Exception caught in '{func.__name__}': {e}")
            raise e
    return wrapper

@operational_tracer
def process_user_billing_payout(user_id, amount):
    """Dispatches real funds out to external credit networks."""
    if amount <= 0:
        raise ValueError("Payout request amount must be positive.")
    return f"Success_Txn_for_{user_id}"

print("--- Real-World 1: Transparent Production Auditing ---")
# Case A: A successful business transaction trace
process_user_billing_payout("usr_9921", 450.00)

# Case B: Catching a failure and verifying the accurate logging origin name
try:
    print("\nTriggering a faulty billing request...")
    process_user_billing_payout("usr_9921", -50.00)
except ValueError:
    pass
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Automated Documentation & OpenAPI Generators
# ================================================================================
# Modern web frameworks (like FastAPI, Flask, or Sphinx documentation tools) use 
# introspection to scan your codebase, read docstrings, and dynamically generate 
# public interactive API specification pages (Swagger UI). 
# If your decorators drop docstrings, your public API documentation goes completely blank!

def api_endpoint_metric_tracker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Simulate tracking API response hit latency metrics
        return func(*args, **kwargs)
    return wrapper

@api_endpoint_metric_tracker
def get_system_health_status():
    """
    GET /api/v1/health
    Returns operational diagnostic metrics for system databases, micro-caches, 
    and thread memory loops. Used by monitoring orchestration arrays.
    """
    return {"status": "GREEN", "uptime_seconds": 50400}

# Simulation of a Framework Document Generator Module scanning endpoints
def framework_documentation_generator(endpoint_callable):
    print(f"Scanning Endpoint Method: Named '{endpoint_callable.__name__}'")
    print("Extracting Specification Schema documentation:")
    doc = endpoint_callable.__doc__
    if doc:
        print(doc.strip())
    else:
        print("⚠️ ERROR: No description provided. Public API Docs will be blank!")

print("--- Real-World 2: Interactive API Documentation Builder ---")
framework_documentation_generator(get_system_health_status)
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Signature Introspection (Validating Input Types)
# ================================================================================
# Advanced tools rely on the `inspect` module to verify original function signatures 
# or type hints. `@functools.wraps` ensures these inspect queries skip right past 
# the wrapper layer directly to the target signature variables.

import inspect

def structural_signature_inspector(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@structural_signature_inspector
def provision_cloud_cluster(nodes: int, region: str = "us-east-1"):
    """Deploys specialized computation engines across cloud nodes."""
    pass

print("--- Real-World 3: Advanced Signature Introspection ---")
# Inspect the parameters of our decorated function
signature_spec = inspect.signature(provision_cloud_cluster)
print(f"Inspected parameters for '{provision_cloud_cluster.__name__}':")
for param_name, param_obj in signature_spec.parameters.items():
    print(f"  -> Argument: {param_name} | Default: {param_obj.default} | Hint: {param_obj.annotation}")
print("-" * 75 + "\n")


# ================================================================================
# SUMMARY & ESSENTIAL RULES
# ================================================================================
# 1. ALWAYS use `@functools.wraps(func)` when building a custom decorator. There is 
#    virtually no performance penalty, and it prevents silent architectural bugs.
# 2. It protects `__name__`, `__doc__`, `__module__`, and `__annotations__`.
# 3. It adds a special `__wrapped__` attribute to the function, allowing developers 
#    to access the original undecorated function directly if needed for unit testing!
#    Example: original_undecorated_version = calculate_volume.__wrapped__