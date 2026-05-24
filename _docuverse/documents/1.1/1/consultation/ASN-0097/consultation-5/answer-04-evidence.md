## Question 4 [evidence]

> Does udanax-green's link-creation primitive reject endsets whose span tuples are empty or whose spans all have zero width, or does it accept such endsets without precondition failure?

## KB Synthesis

The KB gives a clear answer for zero-width spans, and is silent on the empty-endset case.

**Zero-width endpoint spans: crash, not clean rejection**

`create_link` with zero-width endpoints crashes the backend (Bug 0017). There is no graceful precondition failure — the process aborts. The minimum valid endpoint width is 1.

> "Links with zero-width endpoints crash (Bug 0017). The minimum valid endpoint width for link creation is 1." — [PRE-LINK-CREATE], [PRE-ZERO-WIDTH]

The precondition as reconstructed from the KB:

```
pre(create_link) = source_content_exists
                 ∧ target_content_exists
                 ∧ source.width >= 1
                 ∧ target.width >= 1
                 ∧ valid(home_doc)
```

**Empty endset tuples (zero spans): not answerable from KB**

The KB documents zero-width spans but does not record a test of passing an empty span list (no spans at all) to `create_link`. The crash-on-zero-width behavior suggests the implementation performs no defensive input validation before dereferencing endpoint data, so an empty tuple would likely also crash or produce undefined behavior — but this is inference, not a KB finding. The KB does not say so explicitly.

---

## Code Exploration

I'll present the full answer now. The finding write requires permission — I'll report what the code shows directly.

---

## Answer: createlink Does Not Reject Empty or Zero-Width Endsets

**Short answer:** No precondition failure. Empty endsets and zero-width vspans are silently accepted. The one zero-width check that exists is unreachable for normal V-space endsets and causes `abort()` (not a clean rejection) when reached via the I-space path.

---

### Execution path traced

#### 1. FEBE handler — `fns.c:100-112`

```c
void createlink(typetask *taskptr)
{
    if (
       getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
        putcreatelink (taskptr, &linkisa);
    }else
        putrequestfailed (taskptr);
}
```

`getcreatelink` only parses bytes off the wire. No content validation here.

#### 2. Core logic — `do1.c:195-221`

```c
return (
     createorglingranf (...)
  && ...
  && specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
  && specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
  && specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
  && setlinkvsas (...)
  && insertendsetsinorgl (...)
  && insertendsetsinspanf (...)
);
```

All three endset specsets are forwarded directly. No width or emptiness guard before or after.

#### 3. The validation stub — `do2.c:110-113`

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

`acceptablevsa` is a complete no-op. Despite the name, it validates nothing.

#### 4. Specset conversion — `sporgl.c:14-33`

```c
*sporglsetptr = NULL;
for (; specset; specset = ...) {    // ← never enters on empty specset
    ...
}
*sporglsetptr = NULL;
return (TRUE);                      // ← TRUE with NULL sporglset
```

An empty specset returns `TRUE` with `*sporglsetptr = NULL`.

#### 5. vspan-to-sporgl — `sporgl.c:35-65`

```c
for (; vspanset; vspanset = vspanset->next) {  // ← skipped if vspanset is NULL
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ...) {
        movetumbler (&ispanset->width, &sporglset->sporglwidth);
        ...
    }
}
return (sporglsetptr);    // ← returns unchanged NULL
```

Empty vspanset → no sporgls.

#### 6. Zero-width vspan path — `orglinks.c:425-454`

```c
// span2spanset:
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, ...);
for (c = context; c; c = c->nextcontext) {   // ← skipped if context is NULL
    context2span(c, ...);
}
if (!context)
    return (targspansetptr);    // ← returns unchanged NULL
```

A zero-width vspan represents an empty interval `[x, x)`. `retrieverestricted` returns NULL for an empty range. `span2spanset` returns with no ispans added → empty ispanset → empty sporglset.

#### 7. Insertion with empty sporglset — `orglinks.c:86-133`

```c
bool insertpm(..., typesporglset sporglset)
{
    if (iszerotumbler (vsaptr))    // ← checks insertion position, NOT endset width
        return (FALSE);
    ...
    for (; sporglset; ...) {       // ← skipped entirely if sporglset is NULL
        unpacksporgl (...);
        insertnd (...);
    }
    return (TRUE);                 // ← succeeds with no insertions
}
```

The link is committed to POOM and spanfilade with empty endsets. No failure.

#### 8. Zero-width detection — reachable only via I-space direct path

`unpacksporgl` at `sporgl.c:195-202` does check:

```c
if (iszerotumbler (widthptr)) {
    qerror ("zero width in unpacksporgl\n");
}
```

And `qerror` at `genf.c:546-551` calls `abort()`. But this is only reached when a raw `ISPANID` item with zero width is embedded directly in the specset (`sporgl.c:20-22` takes the pointer as-is without validation). For the normal `VSPECID` path, `span2spanset` produces no ispans for a zero-width range, so `unpacksporgl` is never called for those spans.

---

### Summary table

| Input | Outcome |
|---|---|
| Empty specset (no entries) | **Accepted** — link created, empty endset |
| vspec with empty vspanset | **Accepted** — link created, empty endset |
| vspan with zero-width tumbler | **Accepted** — empty enfilade retrieval → empty endset |
| ispan with zero-width tumbler (`ISPANID` direct) | **Fatal `abort()`** — not a clean precondition failure |

No precondition failure is returned for empty span tuples or zero-width vspans. The system silently creates a link with empty endpoints. The only zero-width detection (`unpacksporgl`) fires `abort()` via `qerror` [`genf.c:546-551`] — which is a crash, not a protocol-level rejection — and it is unreachable via the V-space endset code path for these inputs.
