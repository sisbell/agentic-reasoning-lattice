## Question 17 [evidence]

> When the same I-address appears at multiple V-positions within the read span due to self-transclusion, does the read return the content once per V-position, faithfully reproducing each occurrence in the arrangement?

## KB Synthesis

Yes. `retrieve_contents` faithfully returns content once per V-position, reproducing every occurrence in V-order, even when the same I-addresses appear at multiple locations due to self-transclusion.

**Mechanism:** The read path is V→I, not I→V. `specset2ispanset` walks the POOM for each V-position in the requested range, producing an ordered list of I-spans in V-address order. `ispanset2vstuffset` then copies bytes for each I-span sequentially. Because each V-position maps to exactly one I-address (the POOM is a function in the V→I direction), the traversal visits every occupied V-position once and emits its bytes in order.

**Supporting entries:**

- **[EC-SELF-TRANSCLUSION]** (Finding 0028 §2) gives the concrete example: after `vcopy(doc, Span(1.1, 0.4), doc, end)` on "Original", the post-state V-stream is "OriginalOrig" — both occurrences present at V 1.1..1.8 and V 1.9..1.12.

- **[SS-POOM-MULTIMAP]** (Finding 0039) confirms the POOM stores V 1.10 → i_B *and* V 1.19 → i_B as independent entries. The multimap property applies to the I→V direction (link discovery returning multiple V-spans per I-address); the V→I direction (reading) is single-valued per V-position.

- **[ST-VCOPY]** (Finding 0039): after internal transclusion creating "text" at V 1.10..1.13 and again at V 1.19..1.22, `compare_versions` finds shared spans at both locations — confirming both are present and distinguishable in the document.

- **[SS-CONTENT-IDENTITY]** / **[INV-IADDR-IMMUTABILITY]** — shared I-addresses are immutable; the reader obtains the same bytes from each occurrence, but obtains them twice because the V-span covers two distinct sub-ranges.

The duplication of I-addresses in the ispanset is transparent to `ispanset2vstuffset` ([SS-CONTENT-IDENTITY] Finding 0034: `movmem()` raw byte copy). It copies bytes for each I-span entry without deduplication, so "Orig" bytes are returned twice — once for each V-occurrence.

---

## Code Exploration

---

## Answer: Self-Transclusion in doretrieve

**Yes — udanax-green returns content once per V-position, faithfully reproducing each occurrence in the arrangement. There is no deduplication.**

Here is the full execution trace with code citations.

---

### Scenario

Suppose content at I-address `[100, 105)` is transcluded at two V-positions: `[10, 15)` and `[20, 25)`. The POOM (permutation matrix / spanfilade) contains two bottom crums:
- Entry A: V=[10,15) ↔ I=[100,105)
- Entry B: V=[20,25) ↔ I=[100,105)

A read over V-span `[5, 30)` covers both.

---

### Phase 1 — V→I Mapping (POOM walk)

**Entry point**: `fns.c` calls `doretrievev` which chains:

```
specset2ispanset [do2.c:14]
  └─ vspanset2ispanset [orglinks.c:397]
       └─ permute [orglinks.c:404]
            └─ span2spanset [orglinks.c:425]  ← one call per V-span in the restriction
```

Inside `span2spanset` [orglinks.c:435]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
```

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:229] walks the POOM tree:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), ...);   // recurse
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // [retrie.c:263]
    }
}
```

Both Entry A and Entry B qualify (both have V∩[5,30) ≠ ∅). Each produces a context that is appended to the list via `incontextlistnd` [context.c:75]. That function is a **sorted insertion only** — it sorts by position, but has **no duplicate-address check**:

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```
[context.c:74-111]

Back in `span2spanset` [orglinks.c:439-444], both contexts are converted to I-spans:

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`context2span` [context.c:176-212] clips each POOM entry's ranges to the restriction V-span and returns the corresponding I-range. For Entry A (V=[10,15), I=[100,105)), the restriction [5,30) does not clip either end, so it returns I=[100,105). Identically for Entry B.

The resulting `ispanset` contains **two entries**: `I=[100,105)` and `I=[100,105)`.

Note also that span consolidation is **explicitly commented out** at [orglinks.c:412-413]:

```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

An incomplete stub for `consolidatespanset` exists as dead code at [orglinks.c:455-462], never implemented.

---

### Phase 2 — Content Retrieval (Granfilade walk)

`ispanset2vstuffset` [granf1.c:58-74] iterates over **every** entry in the ispanset without any duplicate-span check:

```c
bool ispanset2vstuffset(typetask *taskptr, typegranf granfptr,
                        typeispanset ispanset, typevstuffset *vstuffsetptr)
{
  typevstuffset *save;
  typevstuffset *ispan2vstuffset();
  save = vstuffsetptr;
  *vstuffsetptr = NULL;
  for (; ispanset; ispanset = ispanset->next) {
      vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
  }
  return (TRUE);
}
```
[granf1.c:58-74]

Each call to `ispan2vstuffset` [granf2.c:286-318] queries the granfilade for that I-span and appends a vstuff item (a `typetext` with the character data) to the result set. Because the ispanset has two identical spans — one per V-occurrence — `ispan2vstuffset` is called twice with `I=[100,105)`, and the same characters are appended to the vstuffset twice.

---

### Summary of the Chain

| Step | Code | What happens |
|------|------|-------------|
| POOM walk | `findcbcinarea2d` [retrie.c:252-264] | Finds **both** bottom crums; creates one context each |
| Context list | `incontextlistnd` [context.c:75] | Sorted insert — **no dedup** |
| I-span computation | `context2span` [context.c:176-212] | Each POOM entry maps to its I-span; same I-address produced twice |
| Span consolidation | [orglinks.c:412-413] | **Commented out** — never runs |
| Content fetch | `ispanset2vstuffset` → `ispan2vstuffset` [granf1.c:67, granf2.c:286] | Iterates every ispanset entry; no overlap check |

**The retrieval is position-faithful, not content-faithful.** Each V-position in the requested span that maps to content produces one vstuff item in the result. Self-transclusion — the same I-address at N different V-positions — yields N copies of the content in the response, one per occurrence in the virtual arrangement.
