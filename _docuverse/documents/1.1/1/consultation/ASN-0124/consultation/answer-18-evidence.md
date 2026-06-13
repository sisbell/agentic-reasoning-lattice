## Question 18 [evidence]

> In a transclusion chain where doc A's content is copied to B and B's copy is copied to C, do A, B, and C all carry DOCISPAN entries pointing at the same I-addresses, so that querying A's span returns C directly without any iterative chain-following?

## KB Synthesis

Yes — all three documents carry independent DOCISPAN entries pointing to the same I-addresses, and the query returns all three in a single pass.

## How DOCISPAN entries accumulate through the chain

When A inserts content, `doinsert` → `docopy` → `insertspanf(..., DOCISPAN)` runs with `docisaptr = A` and the fresh I-addresses. The spanfilade gains: `{α₁..αₙ} → A`. [ST-INSERT, Finding 0036]

When B vcopies from A, `docopy` is called again — this time with `docisaptr = B` and the *same* I-addresses (vcopy shares existing I-addresses, it does not allocate new ones). The spanfilade gains: `{α₁..αₙ} → B`. [ST-VCOPY, Finding 0002; ST-COPY, Finding 0047]

When C vcopies from B, B's V-stream maps to the same I-addresses α₁..αₙ (because B itself preserved them from A). So `docopy` runs with `docisaptr = C` and `ispanset = {α₁..αₙ}`, adding: `{α₁..αₙ} → C`. [INV-TRANSITIVE-IDENTITY, Finding 0018]

## The spanfilade is a flat multi-valued index

The spanfilade is not a linked chain — it is a direct index from I-address ranges to document sets. After the three operations above, the spanfilade holds three independent DOCISPAN entries, all keyed on the same I-address range:

```
α₁..αₙ → A   (from A's original INSERT)
α₁..αₙ → B   (from B's vcopy of A)
α₁..αₙ → C   (from C's vcopy of B)
```

`FINDDOCSCONTAINING` queries the spanfilade directly. It finds all three entries in one pass and returns {A, B, C}. No chain traversal, no recursive lookup. [SS-DOCISPAN, Findings 0036/0047; INV-IADDRESS-PERMANENT, Finding 0023]

This is confirmed experimentally by Finding 0018: "find_documents('DEF' from C) → [A, B, C]" where C transcluded from B which transcluded from A — all three returned without any iterative following.

## Why each COPY registers independently

Each call to `docopy` passes its own destination's `docisaptr` to `insertspanf`. The function signature at `do1.c:62` is `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` — the destination document is an explicit parameter per call. There is no mechanism that would "inherit" or skip the registration because the I-addresses are already indexed for a different document. [FC-CONTENT-SPANF-ISOLATION, Finding 0036]

The spanfilade is also write-only — entries are never removed even after DELETE — so the full set {A, B, C} persists indefinitely. [INV-SPANF-WRITE-ONLY, Finding 0057]

**Bottom line:** The transitivity emerges structurally from each COPY registering its own destination. The result is a flat, multiply-valued spanfilade index where querying any I-address in the chain returns all participating documents simultaneously, not by following pointers from one to the next.

---

## Code Exploration

I now have everything needed. Let me write the complete answer.

---

## Answer: Transclusion Chain I-Address Sharing in udanax-green

**Yes — A, B, and C all carry DOCISPAN spanfilade entries pointing at the same permascroll I-addresses.** No iterative chain-following is needed: a single `retrieverestricted` call on the spanfilade returns all three documents at once.

Here is the full trace through the code.

---

### 1. Data Model Dimensions

**wisp.h:15-21** establishes three independent coordinate spaces, each using a different pair of dimension indices in `typewid` / `typedsp`:

```
POOM (doc's V↔I mapping):
    I = 0    ← permascroll (I-space) address
    V = 1    ← virtual (V-space) address within the document

Spanfilade:
    ORGLRANGE = 0    ← doc ISA prefixed with span-type tag
    SPANRANGE = 1    ← permascroll I-address
```

**xanadu.h:39**: `DOCISPAN = 4` — the tag that classifies a spanfilade entry as "this document contains this I-span."

---

### 2. Inserting Content Into Doc A

`doinsert` (do1.c:87-123) first calls `inserttextingranf`, which allocates a new permascroll address and returns it as `ispanset` (an ISPANID). It then calls `docopy`.

**`docopy`** (do1.c:45-65):
```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // line 54
insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // line 60
insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)       // line 62
```

`insertpm` (orglinks.c:75-134) stores a POOM crum in A's POOM:
```c
movetumbler (&lstream, &crumorigin.dsas[I]);    // line 105: permascroll I-addr
movetumbler (vsaptr, &crumorigin.dsas[V]);       // line 113: A's V-addr
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
```

`insertspanf` with `DOCISPAN` (spanf1.c:15-54):
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);   // line 22
                                          // = 4.docisa_A in ORGLRANGE
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);              // line 49
                                          // = original permascroll I-addr
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);  // line 51
```

After Step 1, the spanfilade has one crum: **(4.docisa\_A, I\_perm)**.

---

### 3. Copy A → B: What `specset2ispanset` Extracts

When copying A's V-range into B, the specset is a `VSPECID` for doc A. **`specset2ispanset`** (do2.c:14-46):

```c
} else if (((typeitemheader *)specset)->itemid == VSPECID) {       // line 27
    findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // line 35: get A's POOM
    && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))  // line 36
```

**`vspanset2ispanset`** (orglinks.c:397-402) calls `permute(taskptr, orgl_A, vspan, V, ispansetptr, I)` — walks A's POOM, restricted to the given V-range, returning the **I-dimension** values.

**`span2spanset`** (orglinks.c:425-454) calls `retrieverestricted` on A's POOM, then `context2span` (context.c:176-212) to extract the I-coordinate:

```c
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);    // line 206: dsas[I]
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);  // line 207
```

`grasp.dsas[I]` is exactly the I-address stored in A's POOM crum — the **original permascroll I-address**. The V-range restriction is accounted for proportionally, so a partial copy extracts the correct sub-range of the I-span.

`insertpm` stores that same permascroll I-address in **B's POOM** at B's own V-position. `insertspanf` writes a new spanfilade crum: **(4.docisa\_B, I\_perm)**.

After Step 2, the spanfilade has: **(4.docisa\_A, I\_perm)** and **(4.docisa\_B, I\_perm)**.

---

### 4. Copy B → C: The Chain Does Not Lengthen

When copying B's V-range into C, `specset2ispanset` is called with a `VSPECID` for doc B. It finds B's POOM with `findorgl`, then calls `vspanset2ispanset(taskptr, docorgl_B, vspan_in_B, ispansetptr)`.

B's POOM has a crum with `dsas[I]` = the original permascroll I-address (stored in Step 3's `insertpm`). `context2span` reads `grasp.dsas[I]` out of B's POOM — **the same original permascroll I-address**. No new I-address is generated; no pointer to B's address is created.

`insertpm` stores that address in C's POOM. `insertspanf` writes **(4.docisa\_C, I\_perm)** into the spanfilade.

After Step 3: **(4.docisa\_A, I\_perm)**, **(4.docisa\_B, I\_perm)**, **(4.docisa\_C, I\_perm)**.

---

### 5. Querying — All Three Returned Without Chain-Following

**`dofinddocscontaining`** (do1.c:15-23) → **`finddocscontainingsp`** (spanf1.c:151-188):

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  // line 168: stream = 4
tumblerincrement (&docspace.width, 0, 1, &docspace.width);           // line 169: width = 1

context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);  // line 171
```

`retrieverestricted` (retrie.c:56-85) issues a single 2D range query on the spanfilade:
- ORGLRANGE constrained to the DOCISPAN band (`4.x` for all x)
- SPANRANGE constrained to the queried I-span

This finds all three crums — for A, B, and C — in one pass. The doc ISA is recovered from the ORGLRANGE coordinate by `beheadtumbler` (spanf1.c:174):

```c
movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);  // line 173
beheadtumbler (&docid, &document.address);               // line 174: strips DOCISPAN prefix
```

---

### 6. Summary

| Step | Operation | Spanfilade entry written | I-address used |
|------|-----------|--------------------------|----------------|
| Insert text into A | `doinsert` → `docopy` | `(4.docisa_A, I_perm)` | new permascroll I-addr |
| Copy A→B | `docopy` with A's V-spec | `(4.docisa_B, I_perm)` | **same** `I_perm` from A's POOM |
| Copy B→C | `docopy` with B's V-spec | `(4.docisa_C, I_perm)` | **same** `I_perm` from B's POOM |
| Query | `finddocscontainingsp` | — | returns A, B, C in one lookup |

The invariant is structural: `insertpm` always stores the **source I-address** (permascroll address) in the I-dimension of the POOM crum [orglinks.c:105]. `specset2ispanset` always walks the source doc's POOM to retrieve that stored I-address [do2.c:36]. It never creates a new one. The permascroll address therefore propagates unchanged through any depth of copy chain, and all documents in the chain accumulate DOCISPAN entries in the spanfilade pointing at the same permascroll coordinates.

`finddocscontainingsp` (spanf1.c:171) issues **one** `retrieverestricted` call and returns all matching documents. There is no chain-following — neither in the implementation nor in the design. The transclusion graph is implicitly encoded in the flat spanfilade, not in any linked-list of copy records.
