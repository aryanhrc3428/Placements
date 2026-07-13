"""
================================================================================
               STREAMING DATA PIPELINES IN PYTHON: A COMPLETE TUTORIAL
================================================================================
A streaming data pipeline processes data piece-by-piece (or in small micro-batches) 
in real-time as it arrives, rather than waiting for an entire dataset to be collected 
(which is Batch Processing).

Streaming pipelines follow the classic ETL/Data Engineering architecture:
  [ Data Source ]  --->  [ Transform / Filter ]  --->  [ Data Sink / Load ]
    (Generators)             (Intermediate)              (Consumers/DBs)

By leveraging Python generators, we can construct highly decoupled, memory-efficient 
pipelines where memory utilization stays completely flat, even if processing billions 
of streaming events.
"""

import time
import random
import json

# ================================================================================
# CONCEPT 1: The Anatomy of a Stream (Source -> Transform -> Sink)
# ================================================================================
# Let's build the simplest form of a 3-stage streaming pipeline to see how data 
# flows smoothly from a producer to a consumer.

# 1. DATA SOURCE (Producer)
def simple_source():
    """Generates a continuous sequence of raw transactions."""
    for i in range(1, 4):
        print(f"\n[Source] Emitting raw event #{i}")
        yield {"txn_id": i, "amount": i * 50, "status": "pending"}

# 2. TRANSFORMER (Processor)
def simple_transformer(events):
    """Enriches the incoming data stream on the fly."""
    for event in events:
        print(f"  [Transform] Modifying event #{event['txn_id']} -> Setting status to APPROVED")
        event["status"] = "APPROVED"
        yield event

# 3. DATA SINK (Consumer)
def simple_sink(final_stream):
    """Consumes the fully processed stream and writes it to a 'database'."""
    for event in final_stream:
        print(f"    [Sink] Saving event #{event['txn_id']} to Database: {event}")

print("--- Concept 1: The Basic 3-Stage Streaming Pipeline ---")
# Tie the pipeline stages together by passing the generator objects into each other
raw_stream = simple_source()
processed_stream = simple_transformer(raw_stream)

# The entire pipeline remains dormant until the ultimate Sink pulls the data!
simple_sink(processed_stream)
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: IoT Sensor Network (Filtering & Alerts)
# ================================================================================
# Imagine a smart factory with temperature sensors on machines. The data stream 
# is constant, and we need to dynamically filter out normal readings and trigger 
# immediate alerts for critical overheating spikes.

def mock_iot_sensor_stream(total_readings=6):
    """Simulates live hardware sensor feeds emitting every fraction of a second."""
    machine_ids = ["MACH-01", "MACH-02", "MACH-03"]
    for _ in range(total_readings):
        time.sleep(0.2)  # Simulate real-time stream delay
        yield {
            "machine": random.choice(machine_ids),
            "temperature": round(random.uniform(60.0, 115.0), 1),
            "timestamp": int(time.time())
        }

def filter_anomaly_stream(sensor_stream, threshold=100.0):
    """Filters out normal behavior and passes only high-risk exceptions."""
    for reading in sensor_stream:
        if reading["temperature"] >= threshold:
            yield reading

def alert_dispatcher_sink(anomaly_stream):
    """Acts as the termination point, broadcasting emergency alerts."""
    print("Monitoring live IoT stream... Listening for anomalies...")
    alerts_triggered = 0
    for incident in anomaly_stream:
        alerts_triggered += 1
        print(f"  ⚠️ ALERT #{alerts_triggered}! {incident['machine']} is overheating at {incident['temperature']}°C!")
    
    if alerts_triggered == 0:
        print("  Stream session concluded. System status: Nominal.")

print("--- Real-World 1: IoT Sensor Alert Pipeline ---")
sensor_source = mock_iot_sensor_stream()
critical_only_stream = filter_anomaly_stream(sensor_source, threshold=100.0)

# Start execution
alert_dispatcher_sink(critical_only_stream)
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: E-Commerce Clickstream Analytics (Window Metrics)
# ================================================================================
# E-commerce sites monitor user clicks to analyze user intent. In this scenario, 
# we stream raw user click payloads, parse them, extract tracking parameters, 
# and dynamically mask sensitive data.

# Simulated raw messy tracking data arriving from an HTTP webhook webhook
raw_clickstream_logs = [
    '{"user": "u92", "action": "view_item", "ip": "192.168.1.5", "query": "buy shoes"}',
    '{"user": "u41", "action": "add_to_cart", "ip": "10.0.0.12", "query": ""}',
    '{"user": "u92", "action": "checkout", "ip": "192.168.1.5", "query": ""}',
    '{"user": "u12", "action": "search", "ip": "172.16.2.8", "query": "cheap laptop"}'
]

def log_stream_source(logs):
    for log in logs:
        yield log

def parse_json_transformer(stream):
    for raw_item in stream:
        yield json.loads(raw_item)

def anonymize_ip_transformer(stream):
    for payload in stream:
        # Mask IP address bytes for privacy compliance
        payload["ip"] = "XXX.XXX.XXX.XXX"
        yield payload

def analytics_dashboard_sink(clean_stream):
    print("Analyzing Live E-Commerce Event Clickstream:")
    for click_event in clean_stream:
        action_upper = click_event["action"].upper()
        print(f"  [Dashboard Metric] User {click_event['user']} performed: {action_upper} | Privacy Mask: {click_event['ip']}")

print("--- Real-World 2: E-Commerce Clickstream Processing ---")
# Construct a multi-stage streaming pipeline layout
stage_1 = log_stream_source(raw_clickstream_logs)
stage_2 = parse_json_transformer(stage_1)
stage_3 = anonymize_ip_transformer(stage_2)

# Pull data through the chained pipeline execution
analytics_dashboard_sink(stage_3)
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Infinite Log Watcher (Simulating 'tail -f')
# ================================================================================
# Real production streaming pipelines often run infinitely. This example demonstrates 
# how a pipeline runs indefinitely, idling seamlessly until a new record drops.

def infinite_file_tailer(max_cycles=3):
    """Simulates an active log file tail reader observing live system events."""
    cycle = 0
    events_pool = ["USER_LOGIN", "PAYMENT_SUCCESS", "FILE_UPLOADED"]
    
    while cycle < max_cycles:
        time.sleep(0.4)
        cycle += 1
        yield f"2026-07-13 12:00:0{cycle} | [SYS_LOG] | {random.choice(events_pool)}"

def log_parser_transformer(raw_lines):
    for line in raw_lines:
        timestamp, type_tag, message = line.split(" | ")
        yield {"time": timestamp, "msg": message}

print("--- Real-World 3: Reactive Log Tail Stream Processor ---")
raw_lines_generator = infinite_file_tailer()
parsed_logs_generator = log_parser_transformer(raw_lines_generator)

for live_metric in parsed_logs_generator:
    print(f"  Fetched at {live_metric['time']} -> Event Processed: {live_metric['msg']}")
print("-" * 70 + "\n")


# ================================================================================
# SUMMARY & PRINCIPLES OF STREAMING PIPELINES
# ================================================================================
# 1. Lazy Evaluation: Memory requirements stay constant O(1) relative to total volume.
# 2. Tight Coupling Prevention: Every module does one job (Source, Transform, or Sink) 
#    and yields data forward independently.
# 3. Stream Termination: A pipeline will never run unless a consumer/sink actively 
#    loops through it using a `for` loop, `next()`, or a reducing function.