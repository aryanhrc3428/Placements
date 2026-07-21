The **Producer-Consumer Problem** (also called the bounded-buffer problem) is a classic concurrency scenario:

* **Producer**: Generates data and puts it into a shared buffer.
* **Buffer**: A fixed-size array holding items temporarily.
* **Consumer**: Takes data out of the buffer and processes it.

To keep them from stepping on each other's toes (or trying to pull from an empty buffer / push into a full one), we use **semaphores** to coordinate access.

---

## The Semaphore Primitives

* **`semaP(S)`** *(Wait / Down)*: Decrements semaphore `S`. If `S > 0`, execution continues. If `S == 0`, the process **blocks** until another process increments `S`.
* **`semaV(S)`** *(Signal / Up)*: Increments semaphore `S`. If any process was blocked waiting on `S`, it wakes up one of them.

---

## Shared Initialization

We define a circular buffer of size `N` along with three semaphores:

```c
#define N 5              // Maximum capacity of the buffer

int buffer[N];
int in = 0;              // Next slot for producer to insert
int out = 0;             // Next slot for consumer to remove

semaphore mutex = 1;     // Binary semaphore: guarantees only 1 thread modifies buffer pointers at a time
semaphore empty = N;     // Counting semaphore: tracks empty slots left for producer (starts at N)
semaphore full  = 0;     // Counting semaphore: tracks filled slots ready for consumer (starts at 0)

```

---

---

## Producer & Consumer Implementation

### Producer Process

```c
void producer() {
    int item;
    while (1) {
        item = produce_item();   // 1. Create a new data item
        
        semaP(empty);            // 2. Wait for an empty slot (blocks if empty == 0)
        semaP(mutex);            // 3. Lock access to the buffer (critical section)
        
        // --- Critical Section ---
        buffer[in] = item;       // Place item into buffer
        in = (in + 1) % N;       // Advance insert index
        // -------------------------
        
        semaV(mutex);            // 4. Unlock buffer access
        semaV(full);             // 5. Signal that a new item is available (increments 'full')
    }
}

```

### Consumer Process

```c
void consumer() {
    int item;
    while (1) {
        semaP(full);             // 1. Wait for a filled slot (blocks if full == 0)
        semaP(mutex);            // 2. Lock access to the buffer (critical section)
        
        // --- Critical Section ---
        item = buffer[out];      // Retrieve item from buffer
        out = (out + 1) % N;     // Advance remove index
        // -------------------------
        
        semaV(mutex);            // 3. Unlock buffer access
        semaV(empty);            // 4. Signal that a slot is now free (increments 'empty')
        
        consume_item(item);      // 5. Process the item
    }
}

```

---

## How It Operates Step-by-Step

1. **Empty Buffer state**: `empty = 5`, `full = 0`, `mutex = 1`.
2. **Producer runs first**:
* Calls `semaP(empty)` $\rightarrow$ `empty` becomes `4`.
* Calls `semaP(mutex)` $\rightarrow$ `mutex` becomes `0`.
* Inserts the item into `buffer[0]`, moves `in` to `1`.
* Calls `semaV(mutex)` $\rightarrow$ `mutex` goes back to `1`.
* Calls `semaV(full)` $\rightarrow$ `full` becomes `1`.


3. **Consumer runs next**:
* Calls `semaP(full)` $\rightarrow$ `full` drops back to `0`.
* Acquires `mutex`, retrieves item at `buffer[0]`, releases `mutex`.
* Calls `semaV(empty)` $\rightarrow$ `empty` returns to `5`.



> **Critical Pitfall — Order Matters!**
> Always call `semaP(empty)` **before** `semaP(mutex)`. If you reverse them to call `semaP(mutex)` first, you risk a **deadlock**. If the buffer is full, the producer locks the mutex and then blocks on `empty`. But because it's holding `mutex`, the consumer can never enter the critical section to free a slot, leaving both processes frozen indefinitely!