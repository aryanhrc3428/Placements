"""
================================================================================
                    DECORATOR STACKING: A COMPLETE TUTORIAL
================================================================================
Decorator stacking occurs when you apply more than one decorator to a single
function or method. This allows you to combine multiple independent behaviors—
like authentication, caching, logging, and validation—onto a single endpoint.

The Absolute Golden Rule of Stacking: BOTTOM-UP (INSIDE-OUT)
Decorators execute in the order they are stacked, from the bottom (closest to the 
function) to the top (furthest away). 

Think of it like an onion:
1. The core function is in the center.
2. The bottom-most decorator wraps the core function directly.
3. The next decorator wraps that entire combination, and so on.

Syntax Breakdown:
    @decorator_A
    @decorator_B
    def my_function():
        pass

This is exactly equivalent to:
    my_function = decorator_A(decorator_B(my_function))
"""

import functools
import time

# ================================================================================
# CONCEPT 1: The Order of Execution (The Onion Flow)
# ================================================================================
# Let's create two simple visual decorators to trace exactly how control flows
# into and out of a stacked function pipeline.

def inner_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("  [🟢 Inner Decorator] Before original function runs...")
        result = func(*args, **kwargs)
        print("  [🟢 Inner Decorator] After original function runs...")
        return result
    return wrapper

def outer_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[🔵 Outer Decorator] Before inner wrapper runs...")
        result = func(*args, **kwargs)
        print("[🔵 Outer Decorator] After inner wrapper runs...")
        return result
    return wrapper

print("--- Concept 1: Visualizing the Stack Order ---")

@outer_wrapper
@inner_wrapper
def core_target():
    print("      🔥 CORE FUNCTION: Executing business logic.")

core_target()
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Enterprise Security Pipeline (Auth -> Role Check -> Audit)
# ================================================================================
# In professional web applications (like Flask or FastAPI architectures), requests
# pass through a gauntlet of verification checks. If any layer fails, the pipeline
# halts early, protecting the underlying target.

# Simulated global request context
CURRENT_REQUEST = {
    "user": "developer_jane",
    "is_logged_in": True,
    "role": "admin"
}

def verify_authentication(func):
    """Layer 1: Confirms the visitor is a recognized logged-in session user."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[Security Stage 1] Checking user login token...")
        if not CURRENT_REQUEST.get("is_logged_in"):
            print("  ❌ [Auth Error] Request aborted: User must be logged in.")
            return None
        print("  ✅ [Auth Success] User token validated.")
        return func(*args, **kwargs)
    return wrapper

def require_admin_role(func):
    """Layer 2: Confirms the authenticated user has sufficient administrative power."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[Security Stage 2] Evaluating RBAC clearance status...")
        if CURRENT_REQUEST.get("role") != "admin":
            print(f"  ❌ [Role Error] Rejection: Admin role required. User is '{CURRENT_REQUEST['role']}'.")
            return None
        print("  ✅ [Role Success] Administrative access authorized.")
        return func(*args, **kwargs)
    return wrapper

def audit_log_action(func):
    """Layer 3: Generates an un-wipeable diagnostic trace for compliance review."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[Audit Log Trigger] User '{CURRENT_REQUEST['user']}' is executing: '{func.__name__}'")
        return func(*args, **kwargs)
    return wrapper

# STACKED COMPOSITION:
# 1. verify_authentication wraps the base function first.
# 2. require_admin_role wraps that combination.
# 3. audit_log_action wraps the whole thing.
@audit_log_action
@require_admin_role
@verify_authentication
def wipe_production_database():
    print("      💥 [Danger Zone] Deep system table structure wiped successfully.")

print("--- Real-World 1: Execution under Authorized Parameters ---")
wipe_production_database()

print("\n--- Real-World 1: Execution under Compromised Parameters ---")
# Let's demote the user session to standard status and observe the pipeline break
CURRENT_REQUEST["role"] = "guest"
wipe_production_database() 
# Notice how verify_authentication ran, but require_admin_role caught it and halted before execution reached the core!
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: E-Commerce Pipeline (Sanitize Input -> Performance Profiler)
# ================================================================================
# Decorators can transform incoming inputs or evaluate outbound execution metrics. 
# Here we strip whitespace off item descriptions before tracking microsecond runtimes.

def performance_timer(func):
    """Measures exact execution runtime latency parameters."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"⏱️  [Metrics] '{func.__name__}' finalized execution in {duration:.5f} seconds.")
        return result
    return wrapper

def sanitize_string_inputs(func):
    """Cleans text arguments automatically by removing accidental trailing spaces."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Mutate positional arguments list on the fly
        cleaned_args = [arg.strip() if isinstance(arg, str) else arg for arg in args]
        return func(*cleaned_args, **kwargs)
    return wrapper

@performance_timer
@sanitize_string_inputs
def database_sku_lookup(item_name):
    print(f"  [DB Search] Querying database catalogs for exact matching value: '{item_name}'")
    time.sleep(0.1) # Simulate database query latency
    return f"SKU-SUCCESS-{hash(item_name)}"

print("--- Real-World 2: Combined Input Sanitization and Profiling ---")
# The string has messy surrounding spaces.
# The sanitizer will clean it up BEFORE the query prints, and the timer tracks the total cost.
lookup_result = database_sku_lookup("   Premium Wireless Headphones    ")
print(f"Final Return Value: {lookup_result}")
print("-" * 75 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Mixing Parameterized and Plain Decorators
# ================================================================================
# You can stack plain decorators alongside parameterized decorator factories. 
# Let's wrap a string output in custom HTML bold tags while simulating a JSON API parser.

def simulate_json_response(func):
    """Converts a standard return value into an API JSON string structure."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        raw_output = func(*args, **kwargs)
        return {"status": 200, "data": raw_output}
    return wrapper

def html_tag_wrapper(tag_name):
    """Parameterized decorator factory creating HTML wrappers around outputs."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            inner_content = func(*args, **kwargs)
            return f"<{tag_name}>{inner_content}</{tag_name}>"
        return wrapper
    return decorator

print("--- Real-World 3: Mixed Plain and Parameterized Decorators ---")

# Execution flow order here:
# 1. html_tag_wrapper('strong') wraps text output -> <strong>Hello</strong>
# 2. html_tag_wrapper('p') wraps that result     -> <p><strong>Hello</strong></p>
# 3. simulate_json_response wraps the string     -> {'status': 200, 'data': '<p><strong>...'}
@simulate_json_response
@html_tag_wrapper("p")
@html_tag_wrapper("strong")
def generate_web_banner(username):
    return f"Welcome back, {username}!"

api_payload = generate_web_banner("DevAdmin")
print(f"Formatted JSON API Response:\n{api_payload}")
print("-" * 75 + "\n")


# ================================================================================
# SUMMARY & KEY DESIGN TAKEAWAYS
# ================================================================================
# 1. Stacked decorators resolve from the bottom up (inside out).
# 2. Ensure every single decorator in the stack correctly passes down `*args` and 
#    `**kwargs` so parameters aren't dropped between layers.
# 3. Always apply `@functools.wraps(func)` inside every decorator, otherwise the 
#    name and docstring properties will be overwritten by whichever decorator 
#    happens to sit on the very top of the stack!