## Question 18 [evidence]

> Does the cursor returned to the reader expose absolute progress (e.g., index k of total), or only enough state to request the next window without revealing how many links remain?

## KB Synthesis

The cursor exposes only enough state to request the next window — it does not reveal absolute progress or total count.

From [SS-PAGINATE-LINKS]: the cursor is a **link ISA tumbler** — an identity address of the last link seen, not a positional index. On each call, `FINDNEXTNLINKSFROMTOTHREE` re-executes the full search from scratch, linearly scans for an exact tumbler match on the cursor, then truncates the result list destructively at N items. The return value is only the N-item page plus an actual-count field.

Nothing in the call returns how many links precede or follow the window. The caller learns: "here are N links starting after link X" — not "you are at position k of total m." If the cursor link is no longer in the result set (deleted between calls), the response is simply empty with count=0 [EC-CURSOR-INVALIDATION].

A separate opcode, `FINDNUMOFLINKSFROMTOTHREE` [SS-FIND-LINKS / Finding 0035], does materialize the full result list and count it — but that is a distinct non-paginated call, not part of the cursor protocol.

---

## Code Exploration

I now have all the evidence needed. Let me compile the answer from the source.

---

## Answer: The Cursor Is Opaque — It Exposes No Absolute Progress

The backend implements three distinct link-query operations, visible in `fns.c`:

- **`findlinksfromtothree`** (`fns.c:189`) — returns all matching links at once
- **`findnumoflinksfromtothree`** (`fns.c:204`) — returns the total count as a plain integer (this is the only place the backend voluntarily discloses the total)
- **`findnextnlinksfromtothree`** (`fns.c:219`) — the paginated form; this is where cursors live

---

### What the cursor is

`getfindnextnlinksfromtothree` (`get1fe.c:115–121`) reads the request:

```c
bool getfindnextnlinksfromtothree(typetask *taskptr, ..., typeisa *lastlinkptr, INT *nptr)
{
    return
       getfindlinksfromtothree (taskptr, ...)
    && gettumbler (taskptr, lastlinkptr)   // ← the cursor
    && getnumber  (taskptr, nptr);         // ← window size
}
```

The cursor is `lastlink`: a raw tumbler (Xanadu address) of the last link address the client previously received. It is not an integer index. There is no field for "position k of total N".

---

### How the backend uses the cursor — no index arithmetic

`findnextnlinksfromtothreesp` (`spanf1.c:117–149`) is the implementation:

```c
bool findnextnlinksfromtothreesp(..., typeisa *lastlinkisaptr, typelinkset *nextlinksetptr, INT *nptr)
{
    INT n = 0;
    // Re-runs the full search from scratch every time:
    findlinksfromtothreesp (taskptr, spanf, ..., &linkset);

    if (iszerotumbler (lastlinkisaptr)) {
        *nextlinksetptr = linkset;              // first window: start from head
    } else {
        for (; linkset; linkset = linkset->next) {
            if (tumblereq (&linkset->address, lastlinkisaptr)) {
                *nextlinksetptr = linkset->next; // resume after the cursor address
                break;
            }
        }
    }
    // Then truncate to n items:
    for (linkset = *nextlinksetptr; linkset; linkset = linkset->next) {
        if (++n >= *nptr) { linkset->next = NULL; break; }
    }
    *nptr = n;
    return (TRUE);
}
```

The backend **re-runs the full search every time**, then does a linear scan to find where the cursor address sits in the list, then walks forward `n` steps and truncates. It never stores state between calls. The cursor is a resume-point address, not an index.

---

### What the response sends back

`putfindnextnlinksfromtothree` (`putfe.c:290–295`):

```c
int putfindnextnlinksfromtothree(typetask *taskptr, INT n, typelinkset nextlinkset)
{
    putnumber (taskptr->outp, FINDNEXTNLINKSFROMTOTHREE);
    putitemset (taskptr, (typeitemset)nextlinkset);
}
```

The function signature accepts `INT n` (the actual count returned after truncation), but **does not serialize it**. The wire response contains only:

1. The command code
2. The link set for this window (count of items in the window + their tumbler addresses)

There is no total, no position, no "k of N" field. The `n` computed at `spanf1.c:147` (`*nptr = n`) is passed up through `fns.c:231` into `putfindnextnlinksfromtothree` and silently dropped.

---

### The only way to learn the total

The backend does have a separate command — `findnumoflinksfromtothree` — whose sole purpose is to expose the total. Its output routine (`putfe.c:277–281`):

```c
int putfindnumoflinksfromtothree(typetask *taskptr, INT num)
{
    putnumber (taskptr->outp, FINDNUMOFLINKSFROMTOTHREE);
    putnumber (taskptr->outp, num);
}
```

This sends the count as a plain integer. The implementation (`spanf1.c:105–115`) calls `findlinksfromtothreesp` and counts the list — the same full scan the paginated form also does internally.

---

### Summary

| Question | Answer |
|---|---|
| Does the cursor encode "index k of total"? | **No.** It is the raw tumbler address of the last link seen (`get1fe.c:119`). |
| Does the paginated response include a total count? | **No.** `putfindnextnlinksfromtothree` sends only the link window (`putfe.c:290–295`). The `n` parameter is received but not serialized. |
| Does the response tell the client how many are left? | **No.** The client infers exhaustion when it receives an empty set or fewer links than it requested. |
| Can the reader learn the total if they want it? | **Yes**, but only by issuing a separate `findnumoflinksfromtothree` command (`fns.c:204`). This reveals the total count as a plain integer — but it is a distinct, explicit round-trip, not part of the cursor protocol. |

The cursor is deliberately minimal: it carries only enough state to resume iteration (the address of the last link seen, or zero to start from the beginning). The backend does not volunteer how many links remain. A reader who wants that information must ask separately — and even then, because the backend re-runs the full search fresh on each paginated call (`spanf1.c:124`), the count returned by `findnumoflinksfromtothree` is not guaranteed to match what a subsequent `findnextnlinksfromtothree` will actually find if the link set changes between calls.
