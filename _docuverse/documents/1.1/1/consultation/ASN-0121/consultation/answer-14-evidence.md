## Question 14 [evidence]

> When matching the third-set (type/connector endset), does the search compare against the link's type endset I-addresses stored in the spanfilade, or against the registered type namespace at `1.0.2.x` — and does an empty third-set act as a wildcard matching any connector?

## KB Synthesis

## Third-Set (Type Endset) Matching

**Search mechanism — spanfilade I-address intersection, not direct namespace lookup.**

When `CREATELINK` is called with a type spec (e.g., `QUOTE_TYPE` referencing `1.0.2.3` in the bootstrap document), `insertendsetsinspanf()` indexes the type endpoint's I-addresses into the spanfilade under the LINKTHREESPAN=3 ORGLRANGE subspace [ST-CREATE-LINK, INT-SPORGL-LINK-INDEX]. The type I-addresses stored are the permascroll I-addresses of the content at `1.0.2.x` — not a symbolic reference to the type namespace.

When `findlinksfromtothreesp` receives a non-empty `three_spec`, it converts that spec to I-addresses via `specset2sporglset` and then performs an I-address intersection search in the LINKTHREESPAN subspace of the spanfilade — the same content-identity intersection mechanism used for FROM and TO endpoints [SS-FIND-LINKS, SS-RETRIEVE-ENDSETS]. The registered type namespace at `1.0.2.x` matters only insofar as all uses of the same type constant share the same I-addresses, enabling the intersection to succeed.

**Empty third-set (NOSPECS) = wildcard.**

Consistent with the AND semantics established in Finding 0029: `find_links(source, NOSPECS, NOSPECS)` constrains only the source endpoint; the type dimension imposes no restriction [SS-FIND-LINKS]. This matches observed behavior — unfiltered `find_links` returns links of all types.

**Critical caveat: type filtering is currently non-functional when a spec IS provided.**

[EC-TYPE-FILTER-NONFUNCTIONAL] documents that `find_links(source, NOSPECS, type_spec)` returns empty results even when unfiltered search finds links of those exact types. The architecture is correct by design, but the current implementation fails to produce non-empty results when filtering by type. The NOSPECS wildcard path works; the active type-filter path does not.

---

## Code Exploration

I now have all the evidence needed. Here is the full answer.

---

## Third-Set Matching in udanax-green: Full Analysis

### 1. The search compares against I-addresses in the spanfilade — never against `1.0.2.x`

The type/connector endset (third-set) is stored and retrieved using purely internal positional constants in the spanfilade index. There is no lookup against any registered type namespace.

The constants are defined in `backend/xanadu.h:36-38`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

#### Storage at link creation

`fns.c:100-112` dispatches `createlink` → `docreatelink`. Inside `do1.c:195-221`:

```c
specset2sporglset (taskptr, fromspecset,  &fromsporglset,  NOBERTREQUIRED)  // do1.c:214
specset2sporglset (taskptr, tospecset,    &tosporglset,    NOBERTREQUIRED)  // do1.c:215
specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)  // do1.c:216
...
insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)  // do1.c:219
```

`insertendsetsinspanf` at `do2.c:116-128` then writes each endset into the spanfilade under its type prefix:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)    // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)      // do2.c:120
if (threesporglset)
    insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)  // do2.c:123
```

`insertspanf` at `spanf1.c:22` bakes the type constant into the stored I-address prefix:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

The type information is thus **positionally encoded as tumbler prefix 1, 2, or 3** in the ORGL dimension of the spanfilade crum. There is no type namespace at `1.0.2.x` or anywhere else involved.

---

### 2. Call chain for link lookup

`fns.c:189-202` (`findlinksfromtothree` FEBE handler):

```c
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
dofindlinksfromtothree  (taskptr, fromvspecset, tovspecset, threevspecset, (typeispan*)NULL, &linkset)
```

`do1.c:348-352` (`dofindlinksfromtothree`) is a thin wrapper:

```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
```

`spanf1.c:56-103` (`findlinksfromtothreesp`) is the core logic:

```c
// Step 1: Convert each V-specset to an I-sporglset
if (fromvspecset)   specset2sporglset(taskptr, fromvspecset,   &fromsporglset,   NOBERTREQUIRED);  // :70-71
if (tovspecset)     specset2sporglset(taskptr, tovspecset,     &tosporglset,     NOBERTREQUIRED);  // :72-73
if (threevspecset)  specset2sporglset(taskptr, threevspecset,  &threesporglset,  NOBERTREQUIRED);  // :74-75

// Step 2: Query the spanfilade for each endset independently
if (fromvspecset)  { sporglset2linkset(..., fromsporglset,   &fromlinkset,   ..., LINKFROMSPAN);  }  // :76-83
if (tovspecset)    { sporglset2linkset(..., tosporglset,     &tolinkset,     ..., LINKTOSPAN);    }  // :84-91
if (threevspecset) { sporglset2linkset(..., threesporglset,  &threelinkset,  ..., LINKTHREESPAN); }  // :92-99

// Step 3: Intersect
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // :100
```

The `sporglset2linkset` call uses the same `LINKTHREESPAN=3` prefix to restrict the spanfilade range it searches — it will only find crums whose ORGL dimension starts with 3, i.e., links whose type-endset I-addresses overlap the query sporglset. No external namespace is consulted at any step.

---

### 3. An empty third-set acts as a wildcard

Two guard clauses enforce this:

**Guard 1 — conversion skipped** (`spanf1.c:74-75`):
```c
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);
```
If `threevspecset` is NULL, `threesporglset` is never set.

**Guard 2 — lookup skipped** (`spanf1.c:92-99`):
```c
if (threevspecset) {
    sporglset2linkset(..., threesporglset, &threelinkset, ..., LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return (TRUE); }
}
```
If `threevspecset` is NULL, this entire block is skipped. `threelinkset` stays `NULL` (initialized at `spanf1.c:69`).

**Guard 3 — wildcard intersection** (`spanf2.c:63-79`):
```c
/* If only one linkset is non-null, then just use it */
if (linkset1 && !linkset2 && !linkset3)   *linkset4ptr = linkset1;   // :64-65
else if (!linkset1 && linkset2 && !linkset3) *linkset4ptr = linkset2; // :66-67
else if (!linkset1 && !linkset2 && linkset3) *linkset4ptr = linkset3; // :68-69
else *linkset4ptr = NULL;                                              // :70-71
```

When only from- and to-sets are specified (third-set NULL), `threelinkset` is NULL, `linkset3 == NULL`, and the two-way intersection at `spanf2.c:95-104` runs without any type filtering:

```c
if (!linkset3) {
    for (; temp1; temp1 = temp1->next)
        for (temp2 = linkset2; temp2; temp2 = temp2->next)
            if (tumblereq (&temp1->address, &temp2->address)) { ... }
}
```

**Confirmed**: an empty/NULL third-set means no type constraint is applied — the search matches links regardless of what type endset (or none) was stored in their LINKTHREESPAN spanfilade slot.

---

### Summary

| Question | Answer |
|---|---|
| What does third-set match against? | I-addresses stored in the spanfilade under the `LINKTHREESPAN=3` prefix — baked in at creation time via `prefixtumbler` [`spanf1.c:22`] |
| Is `1.0.2.x` type namespace consulted? | No. The type constants (1, 2, 3) are positional prefixes in the crum's ORGL dimension, not namespace lookups |
| Empty third-set = wildcard? | Yes, unconditionally. Two `if (threevspecset)` guards at `spanf1.c:74` and `spanf1.c:92` skip all third-set processing when it is NULL, and `intersectlinksets` at `spanf2.c:63-78` returns the un-type-filtered from/to intersection |
