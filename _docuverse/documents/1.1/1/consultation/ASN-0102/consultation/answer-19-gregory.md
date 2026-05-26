## Question 19 [gregory]

> If the source V-span maps to I-addresses that were originally created in a third document (the source document itself acquired them via an earlier copy), does the DOCISPAN entry in the spanfilade record the immediate source document or the original creating document as the document component of the indexed I-span?

## KB Synthesis

The DOCISPAN entry records the **destination document** — neither the immediate source nor the original creator.

The mechanism is in `docopy()` at `do1.c:45-65`, which contains the call:

```c
insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The `docisaptr` parameter is the ISA of the document being **written into** (the copy destination). [SS-DOCISPAN, Finding 0036] makes this explicit:

> `do1.c:62` — `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` in `docopy()`

So for a transclusion chain A → B → C:

1. A inserts content (INSERT): DOCISPAN records `I-spans → A`
2. B copies from A (VCOPY): DOCISPAN records `I-spans → B`
3. C copies from B (VCOPY): DOCISPAN records `I-spans → C`

After step 3, `FINDDOCSCONTAINING(I-spans)` returns `{A, B, C}`. Each document accumulated its own DOCISPAN entry at the time it received the content — regardless of where the content originally came from. The spanfilade is append-only [INV-SPANF-WRITE-ONLY], so all three entries persist indefinitely.

This is why [FC-CONTENT-SPANF-ISOLATION, Finding 0018] observes that deleting content from source document A doesn't remove A from `FINDDOCSCONTAINING` results — each DOCISPAN entry is independent and permanent, tied to the destination at copy time. [INV-IADDR-PROVENANCE] separately tracks the *native* (creating) document via the `homedoc` field in POOM crums, but that is distinct from the DOCISPAN index.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Answer

The DOCISPAN entry records **the destination document** (the document receiving the copy) — not the immediate source document, and not the original creating document.

This is not a choice between two alternatives the question offers; the code shows a third answer.

---

### The Full Trace

Call the three documents:
- **A** — the original creator of the content
- **B** — copied from A (immediate source in our scenario)
- **C** — now copying from B (`docisaptr = C`)

#### 1. `docopy` dispatches two operations [`do1.c:53–64`]

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && ...
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // line 62
    );
}
```

`docisaptr` is C throughout. `specset` describes content in B (a V-spec with `docisa = B`).

#### 2. `specset2ispanset` looks up B's POOM to resolve I-addresses [`do2.c:27–38`]

```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {
    findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
    && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
}
```

`((typevspec *)specset)->docisa` is B. `findorgl` opens **B's granfilade (POOM)**. `vspanset2ispanset` → `permute` → `span2spanset` walks B's POOM and produces a set of `ISPANID` spans — raw permascroll I-addresses. These are the same addresses A originally allocated; B's POOM maps B's V-space to them. The returned `ispanset` carries `ISPANID` items — there is no document tag on them, only the permascroll stream/width coordinates.

#### 3. `insertspanf` stores the entry in the spanfilade [`spanf1.c:22–53`]

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
    prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22: ORGLRANGE key = C + DOCISPAN
    ...
    for (; sporglset; ...) {
        if (((typeitemheader *)sporglset)->itemid == ISPANID) {
            movetumbler (&((typeispan *)sporglset)->stream, &lstream);
            movetumbler (&((typeispan *)sporglset)->width, &lwidth);
            movetumbler (isaptr, &linfo.homedoc);                   // line 29: homedoc = C
        }
        ...
        insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
    }
}
```

`isaptr` is the `docisaptr` passed in from `docopy` — it is **C**. Two fields are set from it:

- **`crumorigin.dsas[ORGLRANGE]`** — the enfilade key in the document-ISA dimension, set by `prefixtumbler(isaptr, DOCISPAN, ...)` to C's ISA under the DOCISPAN prefix. This is what `finddocscontainingsp` queries to enumerate documents containing an I-span.
- **`linfo.homedoc`** — the bottom-crum payload field (defined in `wisp.h:108` as `tumbler homedoc` inside `type2dbottomcruminfo`), also set to C's ISA.

The SPANRANGE key (`lstream`/`lwidth`) is the permascroll I-address — the one that A originally allocated when it created the content.

---

### What This Means

The spanfilade records the chain of custody this way:

| When | Spanfilade entry (DOCISPAN) |
|------|----------------------------|
| A inserts content | `(DOCISPAN:A, permascroll-P)` — homedoc = A |
| B copies from A | `(DOCISPAN:B, permascroll-P)` — homedoc = B |
| C copies from B | `(DOCISPAN:C, permascroll-P)` — homedoc = C |

Every document in the copy chain gets its own independent DOCISPAN entry, all pointing to the same permascroll I-address range. The `homedoc` field does not track provenance; it records the receiving document.

The copy provenance (A→B→C) is **not preserved in the spanfilade** at all. What is preserved is the identity of the content itself: the permascroll I-address is invariant across all copies, which is what allows `finddocscontainingsp` to discover every document that includes a given piece of content — they all share the same SPANRANGE key while each has a distinct ORGLRANGE (DOCISPAN) key derived from their own ISA.
