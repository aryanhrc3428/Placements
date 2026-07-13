"""
================================================================================
                    PYTHON ITERATORS: A COMPLETE TUTORIAL
================================================================================
In Python, loops (like 'for item in collection:') work behind the scenes using
the "Iterator Protocol". This protocol relies on two special magic methods:

1. __iter__(): Returns the iterator object itself. It prepares the object 
   to be looped over.
2. __next__(): Returns the next item in the sequence. If there are no more 
   items, it must raise a 'StopIteration' exception to signal the loop to end.

Difference between Iterable and Iterator:
- Iterable: An object that can return an iterator (has __iter__ defined, e.g., lists, strings).
- Iterator: An object with a state that remembers where it is during iteration (has both __iter__ and __next__ defined).
"""

import time
import requests  # Built-in or standard simulation below

# ================================================================================
# CONCEPT 1: How Python's Behind-the-Scenes Loop Works
# ================================================================================
# When you write a 'for' loop, Python secretly turns the collection into an 
# iterator and repeatedly calls next() on it until StopIteration is raised.

print("--- Concept 1: Behind the Scenes of a For-Loop ---")
numbers = [10, 20]

# Standard way:
# for x in numbers: print(x)

# What Python ACTUALLY does:
iterator_obj = iter(numbers)  # Secretly calls numbers.__iter__()
print(next(iterator_obj))     # Secretly calls iterator_obj.__next__() -> Output: 10
print(next(iterator_obj))     # Secretly calls iterator_obj.__next__() -> Output: 20

try:
    print(next(iterator_obj)) # No more items! Raises StopIteration
except StopIteration:
    print("Caught StopIteration! The loop ends gracefully here.")
print("-" * 50 + "\n")


# ================================================================================
# CONCEPT 2: Building a Custom Iterator
# ================================================================================
# Let's build a simple custom Counter that acts exactly like a step-down timer.

class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        # An iterator must return itself when __iter__ is called
        return self

    def __next__(self):
        if self.current <= 0:
            # Tell Python there are no more items to process
            raise StopIteration
        
        result = self.current
        self.current -= 1
        return result

print("--- Concept 2: Custom CountDown Iterator ---")
counter = CountDown(3)
for num in counter:
    print(f"Countdown: {num}")
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 1: Infinite Cycle Iterator (The Carousel)
# ================================================================================
# Imagine you are building a UI component like a image carousel or a game loop 
# where background tracks or team turns cycle indefinitely.

class TurnCycle:
    def __init__(self, players):
        self.players = players
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # We use modulo to wrap the index back around to 0, creating an infinite loop
        current_player = self.players[self.index]
        self.index = (self.index + 1) % len(self.players)
        return current_player

print("--- Real-World 1: Infinite Player Turn Cycle ---")
game_turns = TurnCycle(["Alice", "Bob", "Charlie"])

# We only pull 5 turns because this iterator never raises StopIteration!
for _ in range(5):
    print(f"It's {next(game_turns)}'s turn!")
print("-" * 50 + "\n")


# ================================================================================
# REAL-WORLD EXAMPLE 2: Memory-Efficient Database/API Paginator
# ================================================================================
# Imagine you have a database with millions of rows. Loading all of them into 
# memory at once will crash your application. An iterator allows you to stream 
# or "paginate" data from the database one batch at a time, lazily on-demand.

class NetworkDataStream:
    def __init__(self, total_pages=3):
        self.current_page = 1
        self.total_pages = total_pages
        
    def __iter__(self):
        return self
        
    def _fetch_page_from_api(self, page_num):
        # Simulating a laggy network request fetching a chunk of data
        time.sleep(0.4) 
        return [f"Record_P{page_num}_A", f"Record_P{page_num}_B"]

    def __next__(self):
        if self.current_page > self.total_pages:
            raise StopIteration
            
        print(f"[API Log] Fetching data chunk for page {self.current_page}...")
        data_chunk = self._fetch_page_from_api(self.current_page)
        self.current_page += 1
        return data_chunk

print("--- Real-World 2: Memory-Efficient API Pagination ---")
data_stream = NetworkDataStream(total_pages=3)

# Notice how the output pauses slightly between iterations? 
# It's fetching records dynamically, keeping memory overhead completely flat!
for batch in data_stream:
    print(f"   Processing batch: {batch}")
print("-" * 50 + "\n")


# ================================================================================
# SUMMARY & TAKEAWAY
# ================================================================================
# Custom iterators are exceptional for:
# 1. Handling infinitely looping logic safely.
# 2. Saving massive amounts of memory via lazy-loading/streaming pipelines.
# 3. Encapsulating custom traversal algorithms over complex data structures.