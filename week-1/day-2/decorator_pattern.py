"""
================================================================================
               THE DECORATOR PATTERN (@ SYNTAX): A COMPLETE TUTORIAL
================================================================================
The Decorator Pattern is a structural design pattern that allows you to dynamically 
add new behavior or responsibilities to an object (usually a function or a method) 
without altering its existing structural definition.

In Python, this pattern is built directly into the language syntax using the 
charming '@' symbol (often called "syntactic sugar").

Core Use Cases:
1. Separation of Concerns: Keep core business logic clean from cross-cutting 
   concerns like logging, security, validation, and benchmarking.
2. Code Reuse: Write a utility behavior once and easily inject it into dozens 
   of disparate functions across an enterprise application.
"""

import time
import functools

# ================================================================================
# CONCEPT 1: What is the '@' Syntax Sugar Actually Doing?
# ================================================================================
# The '@' symbol is just a cleaner, shorter way of reassignment. 
# Writing `@my_decorator` right above a function is exactly equivalent to writing:
# `my_function = my_decorator(my_function)`

def simple_logger(func):
    def wrapper():
        print(f"[Prep] About to execute function: {func.__name__}")
        func()
        print(f"[Done] Finished executing function: {func.__name__}")
    return wrapper

# --- Setup Way A: The Explicit Way ---
def standard_greet():
    print("   Hello from the explicit function code.")

print("--- Concept 1: Explicit Wrapper Reassignment ---")
# Manually wrapping the target function
explicit_wrapped_greet = simple_logger(standard_greet)
explicit_wrapped_greet()
print("-" * 75 + "\n")

# --- Setup Way B: The Pythonic Syntax Sugar Way ---
@simple_logger
def modern_greet():
    print("   Hello from the decorated function code.")

print("--- Concept 1: The Modern @ Syntax ---")
# Calling the decorated function directly executes the inner wrapper loop
modern_greet()
print("-" * 75 + "\n")


# ================================================================================
# CONCEPT 2: The Universal Decorator Template (*args, **kwargs, @wraps)
# ================================================================================
# Real production decorators must handle functions that take any combinations of 
# arguments and return values. Additionally, they should preserve the original 
# function's identity attributes using `functools.wraps`.

def universal_decorator_template(func):
    @functools.wraps(func)  # Keeps function name and __doc__ metadata intact
    def wrapper(*args, **kwargs):
        # 1. Add custom preprocessing hooks here
        print(f"[Universal Wrapper] Intercepting call to '{func.__name__}'")
        
        # 2. Execute target function and extract its internal return value
        result = func(*args, **kwargs)
        
        # 3. Add custom postprocessing hooks here
        return result  # Ensure the signature returns data correctly back to scope
    return wrapper


# ================================================================================
# REAL-WORLD EXAMPLE 1: Fault-Tolerant Network Retry Mechanism
# ================================================================================
# Microservices frequently drop connections due to temporary blips. A decorator 
# can trap exceptions and automatically retry execution before throwing an error screen.

def retry_on_failure(retries=3, delay=0.1):
    """A parameterized decorator factory that retries flaky execution targets."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    attempts += 1
                    print(f"⚠️  [Retry Tool] Attempt {attempts}/{retries} failed for '{func.__name__}': {error}")
                    if attempts >= retries:
                        print("🚨 [Retry Tool] Max retry thresholds breached. Raising exception...")
                        raise error
                    time.sleep(delay)
        return wrapper
    return decorator

# Simulating an unstable external financial service database hit
FLAKY_NETWORK_COUNTER = 0

@retry_on_failure(retries=3, delay=0.2)
def fetch_payment_status(transaction_id):
    global FLAKY_NETWORK_COUNTER
    FLAKY_NETWORK_COUNTER += 1
    
    # Intentionally fail the first two infrastructure calls
    if FLAKY_NETWORK_COUNTER < 3:
        raise ConnectionResetError("Remote server refused socket handshake.")
        
    return {"id": transaction_id, "status": "SETTLED", "amount": 2500.00}

print("--- Real-World 1: Resilient Remote Infrastructure Retry Pipeline ---")
try:
    payment_info = fetch_payment_status("TXN-99882")
    print(f"🎉 Successful Execution Result: {payment_info}")
except ConnectionResetError:
    print("Main script wrapper captured terminal infrastructure breakdown.")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Input Data Schema Validator
# ================================================================================
# Decorators are exceptionally powerful for decoupling sanitization checks from 
# processing calculations, instantly throwing bad requests out before execution processing.

def validate_positive_numbers(func):
    """Enforces that all numeric incoming arguments must strictly be greater than zero."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Scan positional args
        for val in args:
            if isinstance(val, (int, float)) and val <= 0:
                raise ValueError(f"Invalid Argument Exception: '{val}' must be strictly greater than 0.")
        # Scan keyword args
        for key, val in kwargs.items():
            if isinstance(val, (int, float)) and val <= 0:
                raise ValueError(f"Invalid Keyword Argument Exception: {key}='{val}' must be greater than 0.")
                
        return func(*args, **kwargs)
    return wrapper

@validate_positive_numbers
def process_wire_transfer(account_id, transfer_amount):
    print(f"🏦 [Core Logic] Processing Account ${account_id} routing payload of ${transfer_amount}...")

print("--- Real-World 2: Automated Validation Verification ---")
# Case A: Passing completely legal validation attributes
process_wire_transfer("ACC-45", 1450.75)

# Case B: Attempting a processing payload with a corrupted value
try:
    print("\nAttempting illegal negative balance submission...")
    process_wire_transfer("ACC-45", -500.00)
except ValueError as validation_error:
    print(f"🔒 Validation Engine Caught Anomaly: {validation_error}")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: The Framework Plugin Registry Pattern
# ================================================================================
# Web development tools like Flask and FastAPI use decorators to map URLs to code. 
# Here is a lightweight demonstration of how decorators act as central router collectors.

class MicroWebServerMock:
    def __init__(self):
        # Central routing path registration map repository
        self.route_registry = {}

    def route(self, url_path):
        """A decorator that registers an endpoint string directly to a function handler."""
        def decorator(func):
            # Map path string key to active callable function object reference value
            self.route_registry[url_path] = func
            return func  # Leave original function unmodified in local namespace
        return decorator

    def user_visit_trigger(self, path):
        """Simulates an external HTTP request hitting our platform gateway."""
        if path in self.route_registry:
            print(f"[Router Web Gateway] Matching inbound client call for path: '{path}'")
            return self.route_registry[path]()
        else:
            print(f"[Router Web Gateway] 404 Route Not Found for path: '{path}'")

# Initialize web service instance engine
app = MicroWebServerMock()

# Decorators automatically register handlers directly upon script interpretation
@app.route("/")
def home_view():
    return "<html>Welcome to our Homepage!</html>"

@app.route("/dashboard")
def analytics_view():
    return "{metrics: [25, 84, 91]}"

print("--- Real-World 3: Central System Registry Routing Map ---")
# Simulate real browser traffic traversing endpoints
print(f"Server Response: {app.user_visit_trigger('/')}")
print(f"Server Response: {app.user_visit_trigger('/dashboard')}")
app.user_visit_trigger("/unknown-malicious-url")
print("-" * 75 + "\n")


# ================================================================================
# SUMMARY OF ARCHITECTURAL RULES
# ================================================================================
# 1. Always use `functools.wraps` inside custom wrappers to protect name tracing signatures.
# 2. Maintain strict decoupling: ensure wrapper bodies handle infrastructure/metadata hooks 
#    and pass execution downstream cleanly without stealing operational computational logic.
# 3. If your decorator requires input parameters of its own (e.g., `@retry(retries=3)`), 
#    you must build a "Decorator Factory"—a function that takes arguments and returns 
#    the actual decorator function.