"""
================================================================================
              ADVANCED REGULAR EXPRESSIONS FOR LOG PARSING: A MASTERCLASS
================================================================================
Log parsing is one of the most demanding applications of Regular Expressions. 
Production logs are messy, unstructured, multi-lined, and massive. To parse them 
without crashing servers or introducing performance bottlenecks, you need deep 
control over the engine.

This tutorial covers advanced token mechanics (lookarounds, non-capturing groups)
and optimal usage of the built-in `re` module engine.
"""

import re
from datetime import datetime

# ================================================================================
# CONCEPT 1: Advanced Grouping & Lookarounds (The Core Mechanics)
# ================================================================================
# - Capturing Groups (...)    : Extracts data and assigns it a group index or name.
# - Non-Capturing Groups (?:...): Groups tokens together for quantifiers (*, +, {n}) 
#                               but skips saving them to memory, boosting speed.
# - Lookahead/Lookbehind      : Assertions that check if a pattern exists ahead 
#                               or behind WITHOUT matching/consuming characters.



print("--- Concept 1: Advanced Groups and Lookarounds ---")

sample_log = "2026-07-13 [SUCCESS] User: admin_dev | Action: login | Cost: 45ms"

# 1. Non-Capturing Group vs Capturing Group
# We want to match either SUCCESS or WARNING, but we don't need to isolate it as a variable.
# We do, however, want to capture the username.
group_pattern = r"\[(?:SUCCESS|WARNING)\]\sUser:\s(\w+)"
match = re.search(group_pattern, sample_log)
if match:
    print(f"Captured Username: {match.group(1)}") 
    # Notice match.groups() only contains 1 item because the status group was non-capturing (?:...)
    print(f"Total Captured Groups: {len(match.groups())}")

# 2. Lookarounds (Zero-Width Assertions)
# Extract the value after 'Action: ' only if it is immediately followed by ' | Cost:'
# Positive Lookahead: (?=...)  | Positive Lookbehind: (?<=...)
lookaround_pattern = r"(?<=Action:\s)\w+(?=\s\|)"
action_match = re.search(lookaround_pattern, sample_log)
if action_match:
    print(f"Extracted Action via Lookarounds: '{action_match.group()}'")
print("-" * 80 + "\n")


# ================================================================================
# CONCEPT 2: High-Performance Engine Flags & Compositions
# ================================================================================
# When reading raw config or server output, flags completely alter how tokens act:
# - re.IGNORECASE (re.I): Case-insensitive evaluation.
# - re.MULTILINE  (re.M): Makes ^ and $ match the start/end of individual lines, 
#                         instead of just the entire global string boundary.
# - re.DOTALL     (re.S): Makes the dot (.) match *any* character, including newlines (\n).
# - re.VERBOSE    (re.X): Allows you to write clean, multi-line regex with whitespace and comments!

print("--- Concept 2: Verbose Multi-line Compilations ---")

# Let's compile a highly complex log parser using re.VERBOSE.
# This makes cryptically dense regex easily maintainable by an engineering team.
advanced_log_parser = re.compile(r"""
    ^                        # Anchor to the beginning of the line
    (?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})  # Capture Named Group: Date
    \s                       # Spacer
    \[(?P<level>[A-Z]+)\]    # Capture Named Group: Log Severity level (INFO, ERROR)
    \s+-\s+                  # Separator string
    (?P<message>.*)          # Capture Named Group: The actual log description text
    $                        # Anchor to the end of the line
""", re.VERBOSE | re.MULTILINE)

raw_batch_data = (
    "2026-07-13 10:14:02 [INFO] - System heartbeat running stable.\n"
    "2026-07-13 10:15:59 [ERROR] - Connection failed unexpectedly."
)

# Using finditer is highly recommended for massive streams. It yields Match objects
# lazily one-by-one, keeping your app's memory footprint completely flat!
for log_item in advanced_log_parser.finditer(raw_batch_data):
    print(f"  Parsed [{log_item.group('level')}] Event at {log_item.group('timestamp')}: {log_item.group('message')}")
print("-" * 80 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Multi-line Exception Stack Trace Parser (re.DOTALL)
# ================================================================================
# Production application crashes throw multi-line stack traces. Standard regex fails 
# here because the dot (.) stops matching at the end of the first line. 
# We combine re.DOTALL and Non-Greedy matching (.*?) to grab the whole crash block.

stack_trace_logs = """
2026-07-13 11:00:22 [INFO] Routine background job executed.
2026-07-13 11:02:45 [CRITICAL] WebService Exception Intercepted
  Trackback (most recent call last):
    File "app/gateway.py", line 42, in route
      result = database.execute_query()
    ConnectionRefusedError: Remote DB port 5432 down.
2026-07-13 11:05:00 [INFO] System automatic failover initiated.
"""

# Pattern Breakdown:
# Find a line starting with a CRITICAL tag, then grab EVERYTHING lazily until 
# you hit the next timestamp sequence (or the end of the file).
trace_extractor = re.compile(
    r"^(\d{4}-\d{2}-\d{2}.*?\[CRITICAL\].*?)(?=\n\d{4}-\d{2}-\d{2}|$)", 
    re.DOTALL | re.MULTILINE
)

print("--- Real-World 1: Multi-Line Stack Trace Extraction ---")
extracted_incidents = trace_extractor.findall(stack_trace_logs)
for incident in extracted_incidents:
    print("Isolated Incident Block:")
    print(incident.strip())
print("-" * 80 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Complex Token Splitting and Value Extraction
# ================================================================================
# Sometimes logs contain query arguments or key-value structures where traditional 
# character extraction is messy. We leverage `re.split()` and negative lookbehinds 
# to split lines safely.

print("--- Real-World 2: Dynamic Log Tokens & Key-Value Splitting ---")

# Let's say we have an ultra-messy firewall payload
firewall_log = "SRC=192.168.1.100 DST=10.0.0.1 PROTO=TCP SPORT=443 DPORT=59201"

# Split by spaces, but only if they are not inside an encrypted string value (if applicable)
tokens = re.split(r"\s+", firewall_log)
print(f"Tokenized elements: {tokens}")

# Now let's extract key-values into a real Python dictionary using lookarounds.
# We look for a string of capitals, followed by an equals sign, followed by the value.
kv_pattern = re.compile(r"([A-Z]+)=(.*?)($|\s)")
parsed_metadata = {m.group(1): m.group(2) for m in kv_pattern.finditer(firewall_log)}
print(f"Clean Metadata Dict: {parsed_metadata}")
print("-" * 80 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: Context-Aware Security Redaction (re.sub)
# ================================================================================
# Regulations require scrubbing user passwords or API authorization keys out of 
# analytics logs. We can use `re.sub()` along with lookbehinds to replace sensitive 
# values without erasing the key label names.

print("--- Real-World 3: Context-Aware PII/Security Masking ---")

raw_audit_stream = (
    "user=john_doe session_token=secret_9942a1bc session_id=884\n"
    "user=admin_user session_token=auth_tok_551aa77b session_id=885"
)

# Advanced Replacement Pattern:
# Look for 'session_token=', and match any alphanumeric characters following it.
# We use a positive lookbehind (?<=session_token=) so the text 'session_token=' 
# itself is structurally protected and NOT replaced by the sub operator engine.
token_mask_pattern = r"(?<=session_token=)[a-zA-Z0-9_]+"

sanitized_stream = re.sub(token_mask_pattern, "[MASKED_CONFIDENTIAL]", raw_audit_stream)
print("Sanitized Output Stream for Analytics Tools:")
print(sanitized_stream)
print("-" * 80 + "\n")


# ================================================================================
# CRITICAL PERFORMANCE TIP SUMMARY
# ================================================================================
# 1. Pre-Compile Patterns: If running inside loops parsing millions of lines, 
#    ALWAYS use `re.compile()`. It eliminates compilation overhead on iterative calls.
# 2. Prefer Non-Greedy `.*?` carefully: Greedy matches `.*` can trigger massive 
#    backtracking sequences, resulting in Catastrophic Backtracking and frozen apps.
# 3. Use `finditer()` over `findall()`: `findall()` constructs the entire list of 
#    strings instantly in system RAM. `finditer()` processes items one line at a 
#    time on-demand via an iterator pipeline.
