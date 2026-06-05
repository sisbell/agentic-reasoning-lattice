## Question 13 [evidence]

> How are the three endsets encoded inside the link orgl's enfilade — as separate subspaces within the orgl, or as a flat sporglset, and does the read return them as distinct spans?

## KB Synthesis

## Link Orgl Endset Encoding

The KB gives a clear picture when you combine the FOLLOWLINK, RETRIEVEENDSETS, and SPORGL entries.

### Inside the Link Orgl

The link orgl is a granfilade orgl accessed via `retrieverestricted()`. The three endsets are stored at **distinct positional subspaces** within that orgl:

- `0.1` — FROM endset (source)
- `0.2` — TO endset (target)
- `0.3` — THREE endset (type)

`link2sporglset()` at `sporgl.c:67-95` calls `retrieverestricted()` on the link orgl with the requested position to extract that endset's sporglset. Each endset is a `typesporglset` — a linked list of sporgls, one per contiguous I-address region. [SS-FOLLOWLINK]

A single user-supplied V-span can expand into **multiple** sporgls if the span covers content transcluded from distinct sources (non-contiguous I-address regions). [SS-LINK-ENDPOINT Finding 0037]

### In the Spanfilade (Discovery Layer)

At link creation, `insertendsetsinspanf()` tags each sporgl with its endpoint type using ORGLRANGE prefixes: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`. [INT-SPORGL-LINK-INDEX]

RETRIEVEENDSETS searches the spanfilade with these ORGLRANGE constants as separate restriction dimensions, returning three distinct sporglsets. [SS-RETRIEVE-ENDSETS]

### On Read: Two Paths Return Different Things

| Operation | Source | Returns |
|-----------|--------|---------|
| FOLLOWLINK | link orgl at `0.whichend` | one sporglset → one specset |
| RETRIEVEENDSETS | spanfilade by I-address ∩ ORGLRANGE | three specsets simultaneously |

FOLLOWLINK reads the permanent link orgl directly; RETRIEVEENDSETS discovers endpoints by content-identity intersection. Both convert sporgls back to V-specs via `linksporglset2specset()`, which silently drops unreferenced I-addresses. [INV-ITOV-FILTERING]

### Not to Confuse With

The `2.x`/`3.x` V-subspace distinction in [SS-SUBSPACE-CONVENTION] is a **document-level** encoding — where the link's ISA reference is stored in the *home document's* POOM. That is separate from the internal structure of the link orgl itself.

---

## Code Exploration

I have everything needed. Here is the complete answer.

---

## How Link Endsets Are Encoded in the Link Orgl

### Short answer

The three endsets are stored as **three separate subspaces within a single link orgl enfilade**, each keyed by a distinct VSA (virtual space address) tumbler. They are not a flat sporglset. On retrieval, one subspace is returned per call — the caller selects which endset by passing `whichend`.

---

### 1. The VSA key scheme

`setlinkvsas()` in `do2.c:169-183` assigns each endset its permanent address inside the orgl:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // mantissa[0] = 1
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // mantissa[1] = 1  → from-set at 1.1

    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // mantissa[0] = 2  → to-set at 2.1
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);

    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // mantissa[0] = 3 → three-set at 3.1
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

The first tumbler dimension (`mantissa[0]`) is the subspace discriminator: 1 = from, 2 = to, 3 = three. These integers match the spanfilade type constants declared in `xanadu.h:36-38`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

---

### 2. Insertion: two parallel indexing operations

`docreatelink()` in `do1.c:195-221` runs the complete link creation pipeline:

```c
   createorglingranf (taskptr, granf, &hint, linkisaptr)       // allocate link's own orgl
&& specset2sporglset (taskptr, fromspecset,  &fromsporglset, …)
&& specset2sporglset (taskptr, tospecset,    &tosporglset,   …)
&& specset2sporglset (taskptr, threespecset, &threesporglset,…)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)                    // line 217
&& insertendsetsinorgl (taskptr, linkisaptr, link,               // line 218
       &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr,             // line 219
       fromsporglset, tosporglset, threesporglset)
```

**`insertendsetsinorgl()`** at `do2.c:130-149` calls `insertpm()` once per endset at its distinct VSA:

```c
insertpm(taskptr, linkisaptr, link, fromvsa,  fromsporglset)   // line 132 — into 1.1
insertpm(taskptr, linkisaptr, link, tovsa,    tosporglset)     // line 133 — into 2.1
insertpm(taskptr, linkisaptr, link, threevsa, threesporglset)  // line 137 — into 3.1
```

Each `insertpm` call inserts one sporglset (a set of address-origin-width triples pointing back into the referenced documents) at the designated subspace position within the link's own granfilade.

**`insertendsetsinspanf()`** at `do2.c:116-128` additionally registers each sporglset in the global spanfilade under the typed constants, enabling reverse lookup (find all links touching a given span):

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset,  LINKFROMSPAN)   // line 119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,    LINKTOSPAN)     // line 120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)  // line 123
```

So after link creation the orgl holds **three independent subspace entries** addressable by VSA 1.1, 2.1, 3.1; and the spanfilade holds three typed reverse-index entries.

---

### 3. Retrieval: one endset per call, selected by `whichend`

The FEBE `FOLLOWLINK` handler in `fns.c:114-126` reads both the link ISA and an integer `whichend` from the wire:

```c
void followlink(typetask *taskptr)
{
  typeisa linkisa;
  typespecset specset;
  INT whichend;

    if (
       getfollowlink (taskptr, &linkisa, &whichend)       // line 122
    && dofollowlink  (taskptr, &linkisa, &specset, whichend)){   // line 123
        putfollowlink (taskptr, specset);
    }
}
```

`dofollowlink()` at `do1.c:223-232` delegates to `link2sporglset()`, passing `whichend` unchanged:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &…sporgladdress, sporglset, specsetptr, …));
}
```

`link2sporglset()` at `sporgl.c:67-95` constructs a probe vspan using `whichend` directly as the first tumbler dimension:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // line 81
tumblerincrement (&zero, 0,        1, &vspan.width);    // line 82
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, …, I, …)) {
```

This targets exactly one subspace of the orgl — VSA `[whichend, 1]`. `retrieverestricted()` returns only the content stored there, which is then packaged into a sporglset and converted to a specset by `linksporglset2specset()`.

**One `FOLLOWLINK` call returns one endset.** To recover all three the client must send three separate requests with `whichend` = 1, 2, 3 respectively.

---

### Summary

| Aspect | Encoding |
|--------|----------|
| Storage | Three separate subspaces in a single link orgl (granfilade), keyed by VSA `1.1`, `2.1`, `3.1` |
| Discriminator | First tumbler dimension: 1=from, 2=to, 3=three — matching `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` in `xanadu.h:36-38` |
| Not a flat sporglset | Each endset is inserted by a separate `insertpm()` call at a distinct VSA; they are never merged into one flat list within the orgl |
| Spanfilade index | Also indexed separately under the three type constants, enabling reverse (find-links-by-span) lookups |
| Read protocol | `FOLLOWLINK` takes a `whichend` integer; `link2sporglset()` probes `retrieverestricted()` with `[whichend, 1]`, returning exactly one endset per call as a `typespecset` |
