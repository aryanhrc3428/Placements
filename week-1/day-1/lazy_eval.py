"""
================================================================================
                     LAZY EVALUATION IN PYTHON: A COMPLETE TUTORIAL
================================================================================
Lazy evaluation (also known as call-by-need) is an evaluation strategy that 
delays the computation of an expression until its value is actually needed.

The Opposite: Eager Evaluation
- Eager evaluation computes everything upfront, loading variables and running 
  functions immediately, regardless of whether they are actually used.

Benefits of Lazy Evaluation:
1. Significant performance gains by avoiding unnecessary computations.
2. Massive memory savings by not storing intermediate, unused values.
3. The ability to work with infinitely large data structures.
"""

import time

# Helper function to simulate a heavy operation
def compute_heavy_metric(name):
    print(f"   [Compute] Running intensive calculation for '{name}'...")
    time.sleep(1)  # Simulate a heavy 1-second process
    return 100


# ================================================================================
# CONCEPT 1: Short-Circuit Evaluation (Built-in Laziness)
# ================================================================================
# Python natively implements lazy evaluation via logic operators (`and`, `or`).
# If the first condition satisfies the statement, Python skips evaluating the rest!

print("--- Concept 1: Short-Circuit Logic ---")

# Scenario: We have a flag. If it's False, we don't care about the heavy metric.
is_admin = False

print("Evaluating condition eagerly (Manually):")
# An eager approach would calculate the metric first:
# metric = compute_heavy_metric("User Request")
# if is_admin and metric > 50: ...

print("\nEvaluating condition lazily (Python Native):")
# Because `is_admin` is False, Python doesn't even run `compute_heavy_metric()`!
if is_admin and compute_heavy_metric("Admin Security Check") > 50:
    print("Access Granted.")
else:
    print("Access Denied (Instantly skipped the heavy function!)")

print("-" * 60 + "\n")


# ================================================================================
# CONCEPT 2: Lazy Properties (On-Demand Object Attributes)
# ================================================================================
# In object-oriented programming, initializing heavy datasets inside `__init__` 
# slows down object creation. Instead, we can use the `@property` decorator to 
# delay loading data until the exact moment someone tries to read the attribute.

class UserProfile:
    def __init__(self, username):
        self.username = username
        self._activity_logs = None  # Placeholder: Not loaded yet!

    @property
    def activity_logs(self):
        # The computation happens ONLY when this property is requested
        if self._activity_logs is None:
            print(f"[Lazy Load] Fetching history logs for {self.username} from database...")
            # Simulate fetching data
            time.sleep(1)
            self._activity_logs = ["Logged In", "Updated Profile", "Logged Out"]
        return self._activity_logs

print("--- Concept 2: Lazy Properties in Classes ---")
print("Creating user object...")
user = UserProfile("tech_guru")  # Instant execution!
print("User object created successfully.")

print("\nAccessing property for the FIRST time:")
# This will trigger the actual heavy calculation/loading
print(f"Logs: {user.activity_logs}")

print("\nAccessing property for the SECOND time:")
# It's already cached; it returns immediately!
print(f"Logs: {user.activity_logs}")
print("-" * 60 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Infinite Stream Processing (Sensor Data Monitoring)
# ================================================================================
# Lazy evaluation allows us to describe entirely infinite series. Since Python 
# only computes the next value when requested, the application never runs out of RAM.

def infinite_sensor_stream():
    """Simulates a continuous hardware sensor pulling temperature readings."""
    temperature = 20.0
    reading_id = 1
    while True:
        # Think of this as a constant hardware feed
        yield {"id": reading_id, "temp": round(temperature, 2)}
        temperature += 0.15
        reading_id += 1

print("--- Real-World 1: Infinite Lazy Data Stream ---")
sensor_feed = infinite_sensor_stream()

# We can safely handle a stream that logically never ends
for _ in range(4):
    data_point = next(sensor_feed)
    print(f"Processed Sensor Data -> ID: {data_point['id']}, Temp: {data_point['temp']}°C")
print("-" * 60 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Chained Lazy Pipelines (Large Scale ETL Data Processing)
# ================================================================================
# When dealing with huge datasets, chaining transformations eagerly creates massive 
# intermediate arrays in memory. Chaining them lazily processes items one-by-one 
# through the entire pipeline.

# Mock raw customer database rows
raw_data = [
    "  id:101 | name:alice | spend:250.0  ",
    "  id:102 | name:bob   | spend:45.5   ",
    "  id:103 | name:charles| spend:1200.0 ",
    "  id:104 | name:david | spend:15.0   "
]

def lazy_strip(lines):
    for line in lines:
        yield line.strip()

def lazy_parse(lines):
    for line in lines:
        parts = line.split(" | ")
        yield {
            "id": parts[0].split(":")[1],
            "name": parts[1].split(":")[1].strip(),
            "spend": float(parts[2].split(":")[1])
        }

def lazy_filter_vip(customers):
    for customer in customers:
        if customer["spend"] >= 100.0:
            yield customer

print("--- Real-World 2: Lazy Data Transformation Pipelines ---")
# Setting up the pipeline blueprints. NO data has been processed yet!
stripped_stream = lazy_strip(raw_data)
parsed_stream = lazy_parse(stripped_stream)
vip_stream = lazy_filter_vip(parsed_stream)

print("Pipeline linked. Beginning execution...")
# The data flows through the pipelines incrementally only when the loop demands it.
for vip in vip_stream:
    print(f"  -> Sending Promo Code to VIP Customer: {vip['name'].upper()} (Spent: ${vip['spend']})")
print("-" * 60 + "\n")


# ================================================================================
# SUMMARY & KEY TAKEAWAYS
# ================================================================================
# 1. Lazy evaluation defers computing values until they are absolutely essential.
# 2. Python defaults to lazy behaviors in logic gates, generators, and map/filter objects.
# 3. Use lazy evaluation when working with large/infinite data files, complex 
#    database entity attributes, or long execution networks to optimize memory and speed.