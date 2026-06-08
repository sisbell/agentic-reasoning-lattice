## Question 11 [evidence]

> When INSERT places a span of length n at V-position v, does I-address allocation query the granfilade for max existing I-address under the document's molecule range and return max+1, with no global counter involved?

## KB Synthesis

Yes, exactly. The mechanism is stateless query-and-increment on the granfilade tree, with no global or session-local counter.

**The call chain for INSERT:**

`doinsert` → `inserttextingranf` → `findisatoinsertgr` → `findisatoinsertmolecule`

**Inside `findisatoinsertmolecule`** (`granf2.c:158-181`):
1. Computes an `upperbound` from the document ISA and atom type, scoping the search to the document's content subspace
2. Calls `findpreviousisagr` — a tree traversal that returns the highest existing I-address below that bound
3. Calls `tumblerincrement(&lowerbound, 0, 1, isaptr)` — increments by exactly 1

[SS-ADDRESS-SPACE, Finding 0061] states this explicitly: "The allocation is purely derived from current tree state — there is no cached 'next available' pointer." And [SS-ADDRESS-SPACE, Finding 0077] confirms: "There is no single global `Σ.next` counter... allocation is a family of independent functions partitioned by tumbler range."

**Key properties that follow:**
- Any session querying the same granfilade tree allocates identically [SS-ADDRESS-SPACE, Finding 0061]
- Sequential inserts produce contiguous I-addresses because each query finds the prior allocation as the max [SS-ADDRESS-SPACE, Finding 0033]
- CREATELINK breaks text contiguity because it also calls into the granfilade allocator, advancing the max [INV-MONOTONIC, Finding 0063]
- CREATENEWVERSION does NOT break contiguity because it uses `findisatoinsertnonmolecule` (document range, separate subtree) [INV-MONOTONIC, Finding 0077]

The "molecule range" bound is document-scoped: the upperbound is derived from `hintptr->hintisa` (the document ISA) so the search is restricted to that document's content subspace rather than the full granfilade.

---

## Code Exploration

I now have the full picture. Here is my complete answer.

---

## I-Address Allocation in INSERT: Full Code Trace

**Short answer: Yes.** I-address allocation works exactly as described — it queries the granfilade for the highest existing I-address under the document's molecule range, then returns max+1. There is no global counter anywhere in this path.

---

### Call Chain

```
fns.c:insert()
  → do1.c:doinsert()
    → granf1.c:inserttextingranf()
      → granf2.c:inserttextgr()
        → granf2.c:findisatoinsertgr()
          → granf2.c:findisatoinsertmolecule()
            → granf2.c:findpreviousisagr()   ← THE QUERY
```

---

### Step 1 — `insert` dispatches to `doinsert` [`fns.c:84-98`]

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);
    if (!doinsert (taskptr, &docisa, &vsa, textset))
        ...
}
```

The reply is sent before `doinsert` returns (the kluge version), but the allocation still happens inside `doinsert`.

---

### Step 2 — `doinsert` builds a hint and calls granfilade insertion [`do1.c:87-123`]

```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
  typehint hint;
  typespanset ispanset;
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);   // do1.c:117
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)    // do1.c:119
    );
    return(ret);
}
```

`makehint` at `do2.c:78-84` simply copies the fields into a `typehint` struct:

```c
typedef struct {
    INT supertype;   // DOCUMENT = 3
    INT subtype;     // ATOM = 4
    INT atomtype;    // TEXTATOM = 1
    typeisa hintisa; // = docisa
} typehint;          // xanadu.h:148-153
```

Constants: `DOCUMENT=3`, `ATOM=4`, `TEXTATOM=1` [`xanadu.h:140-146`].

The V-position `vsaptr` is NOT passed to the granfilade at all. I-address allocation is independent of V-space position. The V-address is used only later in `docopy` to wire the I-span into the document's virtual structure.

---

### Step 3 — `inserttextgr` calls `findisatoinsertgr` once, then writes [`granf2.c:83-109`]

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr,
                  typetextset textset, typeispanset *ispansetptr)
{
  tumbler lsa, spanorigin;
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))   // granf2.c:92
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);           // granf2.c:99
        tumblerincrement (&lsa, 0, textset->length, &lsa);           // granf2.c:100
    }
    ispanptr->stream = spanorigin;
    tumblersub (&lsa, &spanorigin, &ispanptr->width);                // granf2.c:106
    *ispansetptr = ispanptr;
    return (TRUE);
}
```

`findisatoinsertgr` is called **once** per INSERT operation to establish the start address `lsa`. Each text chunk advances `lsa` by `textset->length`. The returned `ispan` spans `[spanorigin, spanorigin+total_length)`.

---

### Step 4 — `findisatoinsertgr` routes to the molecule case [`granf2.c:130-156`]

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {     // TRUE for text insert
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
            return (FALSE);
        }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);   // granf2.c:142
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

`isaexistsgr` verifies the document's orgl exists (sanity check). Then `findisatoinsertmolecule` does the actual allocation.

---

### Step 5 — `findisatoinsertmolecule`: the granfilade query and max+1 [`granf2.c:158-181`]

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // granf2.c:162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);     // granf2.c:164

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        // First insert: lowerbound IS docisa (the orgl itself, no text atoms yet)
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);             // granf2.c:166
        tumblerincrement (isaptr, 1, 1, isaptr);                                  // granf2.c:167
    } else if (hintptr->atomtype == TEXTATOM) {
        // Subsequent inserts: lowerbound is the last text ISA
        tumblerincrement (&lowerbound, 0, 1, isaptr);                             // granf2.c:169
    } ...
}
```

**Line 162** computes `upperbound`:

For `docisa = D` and `TEXTATOM=1`:
- `tumblerincrement(D, rightshift=2, bint=2, &upperbound)` adds 2 to the position 2 past the last digit of `D`
- Result: `D.0.2` — the exclusive upper bound of the document's text I-address space

**Lines 163-164** query the granfilade:

`findpreviousisagr` [`granf2.c:255-278`] walks the enfilade tree recursively, accumulating widths:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // granf2.c:264
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ((tmp = whereoncrum(ptr, offset, upperbound, WIDTH)) == THRUME
         || tmp == ONMYRIGHTBORDER
         || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // recurse into child
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate width
        }
    }
}
```

At leaf nodes, `findlastisaincbcgr` [`granf2.c:280-284`] adjusts for multi-character GRANTEXT nodes:

```c
int findlastisaincbcgr(typecbc *ptr, typeisa *offset)
{
    if (ptr->cinfo.infotype == GRANTEXT)
        tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
}
```

If the last text node starts at address `A` and has length `N`, the accumulated `offset` after this call is `A + (N-1)` — the absolute address of the last character stored.

**Lines 165-169** branch on two cases:

**Case A (first insert):** `tumblerlength(docisa) == tumblerlength(lowerbound)` — the found lowerbound is `docisa` itself (the document orgl entry; no text atoms exist yet).
- `tumblerincrement(lowerbound, 2, 1, isaptr)` → `isaptr = docisa.0.1`
- `tumblerincrement(isaptr, 1, 1, isaptr)` → `isaptr = docisa.0.1.0.1`
- First text address is `docisa.0.1.0.1`

**Case B (subsequent inserts):** `lowerbound` is a text atom at `docisa.0.1.0.K` (deeper than docisa's level). `findlastisaincbcgr` has already adjusted it to be the last ISA in the last GRANTEXT node.
- `tumblerincrement(&lowerbound, 0, 1, isaptr)` — adds 1 to the last digit
- Result: `lowerbound + 1` = the next available address

This is the exact "max+1" mechanism. If the last insert wrote N characters starting at address `A`, `lowerbound = A + N - 1`, and the new allocation starts at `A + N`.

---

### No Global Counter Exists

A search across all `.c` files finds no global or static counter variable used in the I-address allocation path. The only `counter`-named symbols in the codebase are `foocounter` and `barcounter` — two stub functions in `insert.c:71-72` that return 0 and are never called. The `nextaddress` in `insert.c:23` is a local variable inside `insertseq`, used only for enfilade geometry (splitting/sizing crums around the insertion point), not for address selection.

The `typehint` hint passed into the allocation carries only the document's ISA (`hintisa`), the type constants, and nothing persistent. Nothing is threaded back out as updated state for the next call.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Does allocation query the granfilade? | Yes | `findpreviousisagr` called at `granf2.c:164` |
| Is the query bounded to the document's molecule range? | Yes | `upperbound = docisa.0.(atomtype+1)` at `granf2.c:162` |
| Is the result max+1? | Yes | `tumblerincrement(&lowerbound, 0, 1, isaptr)` at `granf2.c:169`; first-insert case builds `docisa.0.1.0.1` at `granf2.c:166-167` |
| Is there a global counter? | No | No such variable exists anywhere in the allocator path |

The I-address allocation is **purely derived** from the current state of the granfilade tree on each call. Two concurrent sessions inserting into the same document would each query the same tree and potentially allocate the same address — but that is a separate concurrency concern, not a counter.
