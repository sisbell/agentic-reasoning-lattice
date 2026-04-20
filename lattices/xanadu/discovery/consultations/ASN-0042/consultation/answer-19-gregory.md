## Question 19 [gregory]

> Does the `.0.` separator play any role in ownership computation, or is it purely a human-readable convention — specifically, does any code path use the position of zero digits to determine where one ownership level ends and another begins?

## KB Synthesis

The `.0.` separator is functional — it IS the hierarchy encoding — but no code path scans for zero positions to determine ownership. The mechanism is arithmetic, not pattern-matching.

**How containment actually works** [SS-TUMBLER-CONTAINMENT]:

```c
tumblertruncate(&A, tumblerlength(&B), &truncated);
tumblereq(&truncated, &B);  // TRUE if A is under B
```

`tumblerlength()` returns `nstories(t) - t.exp`, where `nstories` counts the last *non-zero* significant digit. This means trailing zeros don't count toward length — so `1.1.0.2` has length 4 (stops at the `2`), not 6. Containment is pure digit-count prefix matching: truncate the candidate to parent's length, compare.

**How zeros get there** [SS-ADDRESS-ALLOC, SS-ADDRESS-SPACE]:

`makehint` encodes a `depth` value (1 for same-type hierarchy, 2 for cross-type). `tumblerincrement(hintisa, depth-1, 1)` places the increment `1` at position `depth-1` digits from the right of the significant portion. When allocating a document (depth=2) under account `1.1.0.2`:
- Increment at position 1 from right → places a `1` two digits past the account, with a zero in between
- Produces `1.1.0.2.0.1` — the `.0.` is synthesized by the arithmetic, not written explicitly

**The key distinction**:

The zeros are structurally essential — the total order puts `1.1.0.2 < 1.1.0.2.0.1` because `nstories` of the shorter address is 4, and truncating the longer to length 4 yields exact equality. But the code never asks "where is the next zero?" It asks "what is the digit count?" The `.0.` boundaries emerge from how `tumblerincrement` with the right `rightshift` distributes digits across the mantissa.

**Confirming evidence** from [PRE-ADDRESS-ALLOC]: Bug 0013 was a containment failure — after `findpreviousisagr` found `1.1.0.1.0.1`, allocation incorrectly used it as a base for account `1.1.0.2`. The fix added a post-check: truncate the found address to parent length and verify equality. No zero-scanning — pure prefix length arithmetic.

**Summary**: The `.0.` separators are not a human-readable convention — they are the actual stored hierarchy encoding. But they are produced and checked via length arithmetic (`tumblerlength`, `tumblerincrement` with `rightshift`, `tumblertruncate`), not by locating zero-digit positions in the mantissa.

---

## Code Exploration

Now I have all the facts needed from the actual source. Let me write the definitive answer.

---

## Does `.0.` Play a Functional Role in Ownership Computation?

**Yes — the `.0.` separator is mechanically significant in `tumbleraccounteq`, and its zero positions directly determine ownership boundaries. It is not purely decorative.**

---

### The Core: `tumbleraccounteq` — `tumble.c:38–70`

This is the single function that implements "is document `a` under account `b`?" It does not compare tumblers digit-by-digit. Instead, it counts zero-valued digits in the account tumbler:

```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);   // account boundary reached → document is under account
        }
        // first zero: skip mismatch check for this position
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);  // non-zero digit must match exactly
        }
    }
}
```

The algorithm has two distinct behaviors triggered by zero digits:

1. **First zero** (`j_b == 1`): the match check is skipped. The document can have *any* value at this position.
2. **Second zero** (`j_b == 2`): the function returns `TRUE` immediately — the account's owned space has been fully traversed, and the document falls within it.

---

### How This Interacts with the `1.1.0.1` Account Structure

The default account is defined at `be.c:37`:

```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

Its mantissa array is `[1, 1, 0, 1, 0, 0, ...]`. Walking `tumbleraccounteq` with this account:

| Index | `bptr->mantissa[i]` | Action | `j_b` |
|-------|---------------------|--------|--------|
| 0 | 1 | non-zero → require match on `aptr[0]` | 0 |
| 1 | 1 | non-zero → require match on `aptr[1]` | 0 |
| 2 | **0** | **first zero → skip match check (wildcard)** | **1** |
| 3 | 1 | non-zero → require match on `aptr[3]` | 1 |
| 4 | **0** | **second zero → return TRUE** | **2** |

The structural `.0.` at mantissa index 2 is zero #1. The first trailing zero at index 4 is zero #2 — the terminator. Without the structural `.0.`, an account like `1.1.1` would require *two* consecutive trailing zeros before returning TRUE, placing the ownership boundary two positions further along and changing which document addresses match.

The `.0.` separator also has a wildcard effect: when the account has `0` at index 2, the document's value at index 2 is *not checked*. This is what allows a document `1.1.X.1.0.1` to technically match account `1.1.0.1` for any `X`. In standard usage all documents have `0` at that structural position, so this wildcard is invisible — but the mechanism is real.

---

### The Call Chain: Ownership All the Way Up

**`isthisusersdocument`** — `be.c:171–175` / `socketbe.c:197–201`:

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

All ownership queries reduce to `tumbleraccounteq`.

**`checkforopen`** — `bert.c:81`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // open permitted without an explicit bert entry
} else {
    return -1;
}
```

Whether a connection may open a document without holding a bert lock depends entirely on whether `tumbleraccounteq` returns true for that document against the user's account tumbler. The zero positions in the account tumbler gate every access check.

**`do1.c:270`** uses the function directly for version creation routing:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

If the document address is under the user's account (per zero-counting), the hint is anchored to the document itself; otherwise to the account. The `.0.` structure is what distinguishes these two cases.

---

### `.0.` Is Also Generated as a Structural Boundary

`findisatoinsertnonmolecule` — `granf2.c:203–241` — explicitly inserts `.0.` separators when creating the first document under an account. With `depth = 2` (when `supertype != subtype`, i.e., crossing a hierarchy level), `tumblerincrement` shifts the new address two "stories" to the right of the hint:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// ...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
}
```

The comment at `granf2.c:151` spells this out literally:

```
the account address itself (1.1.0.1 instead of 1.1.0.1.0.1).
```

The `.0.` between `1.1.0.1` (account) and the trailing `1` (first document) is deliberately placed by `tumblerincrement` with `rightshift=2`. The zero digit at the boundary position is not an accident of padding — it is inserted as the separator between hierarchy levels.

---

### The `istextcrum`/`islinkcrum` Distinction — `orglinks.c:246–261`

Zero positions also gate content-type classification:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr)
{
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

`mantissa[1] == 0` identifies text content (a "1.0" address family); `mantissa[1] != 0` identifies link content (a "1.n" address family). These checks are what the comment in `islinkcrum` describes as "1.n tumbler where n != 0." Zero at mantissa index 1 is the dividing line between text ownership space and link space — a direct structural role.

---

### Summary

| Function | File:Line | How zero digits are used |
|----------|-----------|--------------------------|
| `tumbleraccounteq` | `tumble.c:38–70` | Counts zeros in account tumbler; first zero = wildcard; second zero = ownership boundary reached |
| `isthisusersdocument` | `be.c:171–175` | Delegates to `tumbleraccounteq` |
| `checkforopen` | `bert.c:81` | Gates document access on `isthisusersdocument` |
| `do1.c:270` | `do1.c:270` | Routes version creation based on `tumbleraccounteq` result |
| `findisatoinsertnonmolecule` | `granf2.c:235–237` | Inserts `.0.` separator when crossing hierarchy levels with `depth=2` |
| `istextcrum` / `islinkcrum` | `orglinks.c:246–261` | `mantissa[1] == 0` determines text vs. link ownership subspace |

**The `.0.` separator is not purely human-readable convention.** In `tumbleraccounteq`, the zero digit at the structural separator position advances the zero counter, which governs when ownership is declared. The trailing zero of the account's mantissa array fires the boundary return only because the structural `.0.` has already advanced `j_b` to 1. Zero positions also gate text-vs-link classification (`orglinks.c`) and hierarchy-level transitions during address generation (`granf2.c`). All three are real code paths, not cosmetic notation.
