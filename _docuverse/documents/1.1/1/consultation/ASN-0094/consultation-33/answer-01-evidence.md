## Question 1 [evidence]

> In udanax-green, what does the `citation.depends` emission produce for `(F, G, K)` — specifically the cardinalities and address kinds in F and G, and whether duplicate emissions with identical slot-sets are suppressed or admitted?

## KB Synthesis

Not answerable from the KB.

The KB contains no entry — under any heading — for `citation.depends`, an emission function with `(F, G, K)` parameters, or any operation described in those terms. The KB covers tumbler arithmetic, enfilade structure (GRAN/POOM/SPAN), the FEBE operation set (INSERT, DELETE, REARRANGE, VCOPY, VERSION, CREATELINK, FOLLOWLINK, etc.), SPORGL/endset mechanics, BERT access control, and the DOCISPAN index. None of those map to the vocabulary in your question.

If you can tell me which subsystem or source file `citation.depends` lives in, I may be able to reason from adjacent KB entries — but I won't speculate about cardinalities or duplicate-suppression behavior without a KB anchor.

---

## Code Exploration

I now have all the source material needed. Here is my complete answer.

---

## `citation.depends` for `(F, G, K)` — Source-Level Analysis

### Prefatory Note: Terminology

The term `citation.depends` does not appear anywhere in the udanax-green source code, findings, tests, or docs. It is not a function name, not a comment, not a constant. The operational counterpart in the implementation is `findlinksfromtothree` / `dofindlinksfromtothree` — FEBE command 30 (`fns.c:189-202`), which searches the spanfilade for links matching any combination of their three endsets. I will answer entirely from that code path.

---

### F, G, K — The Three Endset Slot Indices

Defined in `backend/xanadu.h:36-38`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

F = 1 (from/source endset), G = 2 (to/target endset), K = 3 (three/type endset).

When a link is created, `docreatelink` (`do1.c:195-219`) calls `insertendsetsinspanf` (`spanf1.c:116-128`), which calls `insertspanf` three times — once for each slot — recording `(endset I-span → link I-address)` entries in the spanfilade under prefixes 1, 2, and 3 respectively.

---

### The Call Path

```
fns.c:189  findlinksfromtothree
  → do1.c:348  dofindlinksfromtothree
      → spanf1.c:56  findlinksfromtothreesp
```

`fns.c:189-202` receives F (`fromvspecset`), G (`tovspecset`), K (`threevspecset`) as `typespecset` inputs. Note: `homeset` is parsed but then discarded — `(typeispan*)NULL` is passed as `orglrangeptr` at `fns.c:198`.

`findlinksfromtothreesp` (`spanf1.c:56-103`) is the core. Annotated:

```c
// spanf1.c:69-99
fromlinkset = tolinkset = threelinkset = NULL;
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // line 71
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);      // line 73
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED); // line 75

if (fromvspecset) {
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset,
                      orglrange, LINKFROMSPAN);           // line 77
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); }  // early-exit
}
if (tovspecset) {
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset,
                      orglrange, LINKTOSPAN);             // line 85
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }
}
if (threevspecset) {
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset,
                      orglrange, LINKTHREESPAN);          // line 93
    if (!threelinkset) { *linksetptr = NULL; return(TRUE); }
}
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr); // line 100
```

Each early-exit (`if (!fromlinkset)`) short-circuits if any provided spec matches zero links — the whole result is empty, no intersection computed.

---

### Address Kinds in F and G

**Input spec type** (`typespecset`, `xanadu.h:89`): a linked list of `typespec` items, each either:
- `VSPECID` (`typevspec`): a virtual-address spec — `docisa` (I-address of a document, `typeisa` = `tumbler`) + `vspanset` (V-spans within that document). These are **V-addresses**.
- `ISPANID` (`typeispan`): a raw I-span — **I-addresses** directly.

The `specset2sporglset` function (`sporgl.c:14-33`) routes `VSPECID` items through `vspanset2sporglset` (`sporgl.c:35-65`), which:
1. Calls `findorgl` to get the document's POOM (granfilade node).
2. Calls `vspanset2ispanset` to map V-spans → I-spans via the POOM.
3. Wraps each result as a `typesporgl` (SPORGLID): `sporglorigin` (I-address), `sporglwidth` (I-width), `sporgladdress` (home document I-address).

The sporgl therefore carries **I-space coordinates** (invariant/permascroll addresses), plus provenance (which document mapped them).

**Output type** (`typelinkset`, `xanadu.h:107`): a linked list of `typelink` = `typeaddress`, each containing a single `address` field of type `typeisa` = `tumbler`. These are **I-addresses** of matching links.

The query against the spanfilade (`sporglset2linksetinrange`, `sporgl.c:239-269`) uses `retrieverestricted` with SPANRANGE as the query axis (the endset I-span) and reads back ORGLRANGE (the prefixed link I-address). The prefix (`spantype` = 1, 2, or 3) is stripped by `beheadtumbler` (`sporgl.c:264`):

```c
// sporgl.c:263-265
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);
}
```

**Summary**: F and G specs are V-addresses at input; the emission produces a set of I-addresses (link addresses). The spanfilade encodes `(slot-prefixed link I-address) → (endset I-span)` in 2D (ORGLRANGE × SPANRANGE per `wisp.h:15-16`).

---

### Cardinalities of F and G (as intermediates)

`fromlinkset` = set of link I-addresses whose F-endset I-spans overlap the F spec. `tolinkset` = analogously for G. Both are `typelinkset` linked lists. Their cardinality before intersection = the number of distinct link addresses found by `sporglset2linkset` for that slot. After `intersectlinksets`, only addresses present in all non-null lists survive.

When only one slot is provided (say F only), `intersectlinksets` (`spanf2.c:64-79`) short-circuits:

```c
// spanf2.c:64-78
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;
// ...
if (*linkset4ptr) { return(0); }  // pass-through, no intersection
```

The F-list is returned verbatim with no further filtering.

---

### Duplicate Suppression — The Critical Finding

`onlinklist` (`spanf2.c:26-44`) accumulates each search's link list and is intended to deduplicate:

```c
// spanf2.c:26-44
bool onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr)
{
    linkset = makelinkitem(taskptr, linkisaptr);

    if (*linksetptr == NULL) {          // empty list: just prepend
        *linksetptr = linkset;
        return(0);
    }

    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq(&temp->address, linkisaptr))
            return(0);                  // found match: suppress
    }

    temp->next = linkset;               // no match: append
}
```

The loop condition `nextlink = temp->next` exits when `temp->next == NULL`. At that point `temp` is the **last element** of the list. The loop body executes for every element **except the last**. The last element is **never tested** against the incoming address.

Consequence:
- **1-element list**: `temp = list[0]`, `temp->next == NULL` → loop never runs → `list[0]` never compared → duplicate appended unconditionally.
- **N-element list**: elements `list[0]` through `list[N-2]` are tested; `list[N-1]` is skipped. If the incoming address equals `list[N-1]`, the duplicate is appended.

**Duplicates are admitted** whenever the same link address is returned by consecutive `retrieverestricted` results within a single `sporglset2linksetinrange` pass — specifically when that address has just been appended (making it the last element). This can happen when a link has a fragmented endset (multiple contiguous I-spans) all of which overlap the query range: each context entry calls `onlinklist` in sequence, and the second call against the last-added address slips through.

This is confirmed empirically by Finding 0019 (`findings/0019-endset-semantics.md`):
> "Creating a link with multiple source spans works, but `retrieve_endsets` sometimes returns duplicate spans: `1.16 appears twice`"

The intersection step (`intersectlinksets`, `spanf2.c:46-120`) does not re-deduplicate its inputs. It performs nested `tumblereq` comparisons:

```c
// spanf2.c:106-118 (three-way case)
for (; temp1; temp1 = temp1->next)
    for (temp2 = linkset2; temp2; temp2 = temp2->next)
        for (temp3 = linkset3; temp3; temp3 = temp3->next)
            if (tumblereq(&temp1->address, &temp2->address)
             && tumblereq(&temp2->address, &temp3->address)) {
                linkset4 = makelinkitem(taskptr, &temp1->address);
                *linkset4ptr = linkset4;
                linkset4ptr = &linkset4->next;
            }
```

If a link appears twice in `temp1` (fromlinkset) and once each in `temp2` and `temp3`, it matches the condition twice and is emitted twice. **No deduplication occurs at the intersection stage.**

---

### Final Answer

| Aspect | Finding | Source |
|---|---|---|
| `citation.depends` | Term absent from source. Closest equivalent: `find_links` FEBE cmd 30 | entire codebase search |
| F slot index | `LINKFROMSPAN = 1` | `xanadu.h:36` |
| G slot index | `LINKTOSPAN = 2` | `xanadu.h:37` |
| K slot index | `LINKTHREESPAN = 3` | `xanadu.h:38` |
| Input address kind (F, G) | V-addresses (`typevspec` with docisa + vspanset) | `xanadu.h:78-83`, `sporgl.c:14-33` |
| Conversion path | V-spans → I-spans via POOM → sporgls | `sporgl.c:35-65` |
| Output address kind | I-addresses (`typeisa` = `tumbler`) in `typelinkset` | `xanadu.h:98-107`, `sporgl.c:264` |
| Spanfilade axes | ORGLRANGE = 0 (link I-addr), SPANRANGE = 1 (endset I-span) | `wisp.h:15-16` |
| Cardinality of F result | Count of distinct link I-addresses with F-endset I-span ∩ query | `spanf1.c:77` + `sporgl.c:239-269` |
| Duplicate suppression | **Off-by-one bug in `onlinklist`**: last list element is never compared. Duplicates are ADMITTED when a link appears multiple times in sequence. | `spanf2.c:38-43` |
| Intersection deduplication | None. Intersection emits once per cross-product hit, not per unique address. | `spanf2.c:96-118` |

**The bottom line**: `(F, G, K)` intersection emits link I-addresses present in all three candidate sets. For each slot, the candidate set is built by `onlinklist` with a tail-skip deduplication flaw; a link appearing consecutively in a slot's results will appear twice in that slot's list. The intersection passes duplicates through. **Emissions with identical slot-sets (same link address) can and do appear multiple times in the output** when the link has fragmented endsets or when the spanfilade returns the same link via multiple matching intervals.
