## Question 1 [evidence]

> In udanax-green, does a retraction/delete record a single to-span, or can one retraction tuple carry multiple target spans?

## KB Synthesis

Based on the KB, a retraction/delete operates on a **single vspan** — one contiguous region specified as a start address plus a width.

The KB evidence is consistent across entries:

- **[ST-REMOVE/Finding 0006]**: "Deletion uses the DELETEVSPAN operation (FEBE command 12), which takes a vspan (start address + width)."
- **[PRE-DELETE/Finding 0040]**: `deletevspanpm()` checks only for zero-width on the single vspan argument — `iszerotumbler(&vspanptr->width)`.
- **[ST-DELETE/Finding 0075]**: The knife construction for DELETE sets `blade[0] = origin` and `blade[1] = origin + width` — a single interval, not a set of intervals.
- **[PRE-DELETE/Finding 0053]**: The subtraction in Case 2 shifts by a single `width` tumbler; there is no loop over multiple target spans.

The multi-span SpecSet pattern belongs to vcopy and retrieval [SS-SPECSET], not to DELETE. Multiple disjoint deletions require multiple separate DELETEVSPAN calls.

So: one retraction tuple carries exactly one target span (start + width).

---

## Code Exploration

I now have everything needed to give a complete, fully-cited answer.

---

## Answer: A retraction carries exactly one target span — never multiple

The entire call stack is hard-wired to a single `(stream, width)` span at every layer. Here is the proof, level by level.

---

### 1. Protocol parsing — `getdeletevspan`

**`backend/get1fe.c:138-146`** (FEBE front-end variant):
```c
bool getdeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    logstuff = TRUE; 
    fprintf(interfaceinput, "%d~", DELETEVSPAN);  
    return (
       gettumbler (taskptr, docisaptr)
    && getspan (taskptr, vspanptr, VSPANID));
}
```

It calls **`getspan`** (singular), not `getspanset`.

**`backend/get2fe.c:213-221`** — `getspan` itself:
```c
bool getspan(typetask *taskptr, typespan *spanptr, char id)
{
    spanptr->itemid = id;
    spanptr->next = NULL;                 // always terminates
    return (
       gettumbler (taskptr, &spanptr->stream)
    && gettumbler (taskptr, &spanptr->width));
}
```

`getspan` reads exactly two tumblers (start and width), sets `next = NULL`, and returns. It never loops. Compare this with `getspanset` (`get2fe.c:~195-210`), which reads a count and loops over `getspan` calls — but `getdeletevspan` does not use `getspanset`.

The interactive variant (`backend/get1.c:162-171`) is identical in structure: one `getspan` call only.

---

### 2. FEBE handler — `deletevspan`

**`backend/fns.c:333-347`**:
```c
void deletevspan(typetask *taskptr)
{
  typeisa docisa;
  typespan vspan;           // single struct, stack-allocated

    (void) getdeletevspan (taskptr, &docisa, &vspan);
    putdeletevspan (taskptr);
    if (!dodeletevspan (taskptr, &docisa, &vspan))
        ...
}
```

`vspan` is declared as a plain `typespan` (not `typespanset`, not a pointer to a list). There is no room for more than one span here.

---

### 3. Core operation — `dodeletevspan`

**`backend/do1.c:158-167`**:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

Takes a `typevspan *` (pointer to one span node) and passes it directly to `deletevspanpm`.

---

### 4. POOM layer — `deletevspanpm`

**`backend/orglinks.c:145-152`**:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

This reads `vspanptr->stream` and `vspanptr->width` directly. There is **no loop**, no traversal of `->next`. Even if a multi-node list were somehow passed in, only the head node's span would be processed and the rest would be silently ignored.

---

### 5. The type system allows lists, but `deletevspan` doesn't use them

**`backend/xanadu.h:65-74`**:
```c
typedef struct structtypespan {
    struct structtypespan *next;    // linked-list pointer
    typeitemid      itemid;
    tumbler stream;
    tumbler width;
} typespan;

typedef typespan typevspan;         // same struct — aliases
typedef typevspan * typevspanset;   // pointer = potential list
```

`typevspanset` (a pointer to a potentially-chained list of spans) exists and is used elsewhere — for example in `docopy`, `insertpm`, and link endpoint sets. But `deletevspan` explicitly uses the non-set type alias `typevspan` and constructs it on the stack as a single node with `next = NULL`.

---

### Summary

| Layer | File | What it does |
|---|---|---|
| Protocol parse | `get1fe.c:144-145` | Calls `getspan` (singular); `next = NULL` forced at `get2fe.c:217` |
| FEBE handler | `fns.c:335-336` | Declares `typespan vspan` (one struct on stack) |
| Core dispatch | `do1.c:158-167` | Passes single `typevspan *` to `deletevspanpm` |
| POOM execution | `orglinks.c:145-152` | Reads `->stream` and `->width` once; no iteration |

**A single retraction/delete call carries exactly one target span: `(stream, width)`. There is no mechanism at any layer — protocol, handler, core, or POOM — to carry multiple target spans in one tuple. To delete a non-contiguous region you must issue multiple `deletevspan` calls.**
