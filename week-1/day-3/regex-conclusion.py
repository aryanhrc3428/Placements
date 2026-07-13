"""
================================================================================
                    PYTHON REGULAR EXPRESSIONS: A COMPLETE TUTORIAL
================================================================================
Regular Expressions (Regex) are powerful, text-matching blueprints used to 
search, parse, validate, and modify string data based on specific patterns.

The Ultimate Rule of Python Regex: ALWAYS use raw strings (r"pattern")!
Python strings use the backslash (\) for escape characters (like \n for newline).
Regex also uses backslashes for special characters (like \d for digit). 
Prefixing your pattern with an 'r' tells Python: "Leave these backslashes alone!"
"""

import re

# ================================================================================
# CONCEPT 1: Basic Searching (search, match, findall)
# ================================================================================
# Python's `re` module provides different functions depending on what you need:
# - re.match(): Checks for a match ONLY at the absolute beginning of the string.
# - re.search(): Scans the entire string and returns the FIRST match it finds.
# - re.findall(): Scans the entire string and returns a LIST of ALL matches.

text = "Code 2026 is awesome. Let's write code in 2026."

print("--- Concept 1: Core Regex Functions ---")

# 1. re.match() fails because the string starts with letters, not digits
match_obj = re.match(r"\d+", text) 
print(f"re.match result: {match_obj}")  # Output: None

# 2. re.search() succeeds because it scans until it finds the first digit sequence
search_obj = re.search(r"\d+", text)
if search_obj:
    print(f"re.search found: '{search_obj.group()}' at index positions {search_obj.span()}")

# 3. re.findall() returns everything it matches as a standard Python list
all_matches = re.findall(r"\d+", text)
print(f"re.findall list: {all_matches}")  # Output: ['2026', '2026']
print("-" * 70 + "\n")


# ================================================================================
# CONCEPT 2: Metacharacters and Character Classes
# ================================================================================
# Metacharacters act as wildcards or shorthand codes for character types:
#   \d = Any digit (0-9)            \D = Any NON-digit
#   \w = Alphanumeric + underscore  \W = Any NON-alphanumeric character
#   \s = Whitespace (spaces, tabs)   \S = Any NON-whitespace
#   .  = Any single character except a newline
#   [A-Z] = Custom character sets (matches any uppercase letter)

sample_data = "Item ID: AB-958283! Price: $45"

print("--- Concept 2: Character Classes ---")
# Extract just the digits
print(f"Digits only:      {re.findall(r'\d', sample_data)}")

# Extract custom range: uppercase letters or dashes
print(f"Custom set ([A-Z-]): {re.findall(r'[A-Z-]', sample_data)}")

# Negated set: Anything that is NOT a lowercase letter or space
print(f"Negated set ([^a-z ]): {re.findall(r'[^a-z ]', sample_data)}")
print("-" * 70 + "\n")


# ================================================================================
# CONCEPT 3: Quantifiers & Anchors
# ================================================================================
# Quantifiers specify *how many* times a character/class should repeat:
#   * = 0 or more times
#   +  = 1 or more times
#   ?  = 0 or 1 time (optional)
#   {n}= Exactly n times
# Anchors bind patterns to boundaries:
#   ^  = Forces match to start at the absolute beginning of a line
#   $  = Forces match to end at the absolute end of a line

print("--- Concept 3: Quantifiers & Anchors ---")

test_strings = ["123", "12345", "12", "abc123xyz"]

# Pattern: Match strings that consist of EXACTLY 3 to 5 digits from start to end
pattern = r"^\d{3,5}$"

for s in test_strings:
    if re.match(pattern, s):
        print(f"  -> '{s}' matches the strict 3-5 digit boundary criteria!")
    else:
        print(f"  -> '{s}' FAILED the criteria.")
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Email Validator and Extractor
# ================================================================================
# A frequent task is extracting clean email identifiers from a raw text dump.

raw_scraping_text = """
Contact support at help.desk@company.org or reach out to sales@global-corp.com. 
Invalid entries like john@com or @twitter won't pass our pattern check.
"""

# Pattern breakdown: 
# [a-zA-Z0-9._%+-]+ -> One or more valid starting characters
# @                 -> Followed by an explicit literal '@' symbol
# [a-zA-Z0-9.-]+    -> Domain name characters
# \.                -> An explicit literal dot '.' character
# [a-zA-Z]{2,}      -> A top-level domain extension (e.g., com, org) of at least 2 letters
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

print("--- Real-World 1: Email Extraction Pipeline ---")
extracted_emails = re.findall(email_pattern, raw_scraping_text)
for email in extracted_emails:
    print(f"  Valid Email Located: {email}")
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Structured Log Parsing via Capturing Groups
# ================================================================================
# Parentheses `()` in regex create "Capturing Groups". They allow you to isolate 
# specific segments of a massive match and instantly convert them into variables.

# Mock web server connection output records
server_logs = [
    "192.168.1.45 - [ERROR] - 404 - /api/v1/checkout",
    "10.0.0.112 - [SUCCESS] - 200 - /index.html",
    "172.16.254.1 - [WARNING] - 500 - /login/submit"
]

# Pattern breakdown:
# (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) -> Group 1: IP Address
#  - \[(.*?)\] -                      -> Group 2: Context Tag inside brackets (Non-greedy match)
#  - (\d{3}) -                         -> Group 3: HTTP Status Code (Exactly 3 digits)
#  - (.*)                              -> Group 4: The remainder URL path
log_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(.*?)\] - (\d{3}) - (.*)"

print("--- Real-World 2: Log Aggregator Parser ---")
# Pre-compiling patterns using re.compile() optimizes performance when reused in loops
compiled_log_regex = re.compile(log_pattern)

for log in server_logs:
    match = compiled_log_regex.search(log)
    if match:
        # Extract individual capturing groups by their index position index
        ip = match.group(1)
        status_tag = match.group(2)
        code = match.group(3)
        endpoint = match.group(4)
        
        print(f"  [IP: {ip:<14}] status: {status_tag:<9} | Code: {code} | Path: {endpoint}")
print("-" * 70 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 3: PII Data Masking / Sanitization (re.sub)
# ================================================================================
# Use `re.sub()` to search for patterns and replace them dynamically. This is 
# critical for filtering out Personally Identifiable Information (PII) before logs 
# hit analytics tools.

raw_customer_ticket = """
Customer requested account update. Phone number provided is 555-123-4567. 
Alternative callback contact info: 800-555-9999.
"""

# Pattern tracks 3 digits, a dash, 3 digits, a dash, and 4 digits
phone_pattern = r"(\d{3})-(\d{3})-(\d{4})"

print("--- Real-World 3: PII Privacy Anonymizer ---")

# Replace full numbers with generalized placeholders using re.sub()
sanitized_text_1 = re.sub(phone_pattern, "[REDACTED_PHONE]", raw_customer_ticket)
print("Option A (Full Redaction):")
print(sanitized_text_1.strip())

# Advanced Replacement: Keep the last 4 digits visible via group back-referencing (\3)
sanitized_text_2 = re.sub(phone_pattern, r"XXX-XXX-\3", raw_customer_ticket)
print("\nOption B (Partial Masking using Group Back-references):")
print(sanitized_text_2.strip())
print("-" * 70 + "\n")


# ================================================================================
# SUMMARY CHEAT SHEET
# ================================================================================
# 1. Use `re.search()` to confirm if a pattern exists anywhere inside a text string.
# 2. Use `re.findall()` to gather all matching records in text collections.
# 3. Use `re.sub()` to clean, fix typos, or redact sensitive string properties.
# 4. Use `r"..."` raw text notations globally to protect regex characters.