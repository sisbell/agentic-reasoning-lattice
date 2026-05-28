## Question 2 [evidence]

> What is the complete, exhaustive set of state-transition kinds across the foundation (ASN-0047 plus ASN-0098 and any others), and is `{K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ} ∪ {K.σ}` the full vocabulary with no further transitions modifying `Σ`?

## KB Synthesis

Synthesizing across the KB, here is the complete picture.

## Transition kinds on Σ

The proposed vocabulary covers the core content-state layer well, but several nuances and at least one gap deserve examination.

### What each kind covers

**K.α** — granfilade allocation. Fires on INSERT (fresh text I-addresses via `findisatoinsertmolecule`), CREATE_DOCUMENT, and VERSION (new document address via `findisatoinsertnonmolecule`). Does NOT fire on VERSION for content — VERSION copies existing I-addresses without allocating new text content [ST-VERSION, INV-MONOTONIC].

**K.λ** — link-orgl allocation. Fires only on CREATE_LINK, allocating the link object in the link element subspace of the granfilade (`docISA.0.2.N`) [SS-ADDRESS-SPACE, SS-ADDRESS-ALLOC]. This is structurally distinct from K.α: different hint depth, different element type (LINKATOM vs TEXTATOM), and sits in a separate tumbler range that breaks I-address contiguity for subsequent text INSERTs [INT-LINK-INSERT, EC-GRAN-MB-ONE].

**K.μ⁺** — POOM insert-and-shift. Covers INSERT (with fresh I-addresses from K.α), COPY/VCOPY (with shared I-addresses, no preceding K.α), and the text-subspace copy that VERSION performs on the new POOM. The shift is bounded to the current subspace by the two-blade knife [SS-TWO-BLADE-KNIFE, FC-SUBSPACE]. Coalescing via `isanextensionnd` [ST-INSERT, Finding 0062] is a structural optimization inside K.μ⁺, not a separate kind.

**K.μ⁻** — POOM shift-left after deletion. Fires as part of DELETE on entries whose exponent matches the deletion width; cross-subspace entries are immune via `strongsub` [INT-DELETE-SUBSPACE-ASYMMETRY]. Always co-occurs with K.δ in practice.

**K.δ** — POOM mapping removal. Fires on DELETE and DELETEVSPAN(2.x). Removes bottom crums via `disown`+`subtreefree`. Never touches granfilade or spanfilade [ST-DELETE, INV-SPANF-WRITE-ONLY].

**K.μ~** — POOM V-address permutation. REARRANGE only. Pure displacement arithmetic on `cdsp.dsas[V]`, no I-address changes, no granfilade or spanfilade effects [ST-REARRANGE, INV-REARRANGE-IDENTITY].

**K.μ⁺_L** — link-reference append in POOM 2.x. Fires on CREATE_LINK: `findnextlinkvsa` computes the current document end, `insertpm` places the link orgl ISA there. Always an append (no entries beyond `vspanreach` to shift) [SS-LINK-SUBSPACE, ST-CREATE-LINK]. Structurally isomorphic to K.μ⁺ but restricted to subspace 2 and guaranteed append-only in sequential operation.

**K.ρ** — tree structural maintenance: `splitcrumupwards`/`levelpush` on overflow, `recombinend`/`takeovernephewsnd` on underflow. Critical asymmetry: `levelpull` is disabled, so K.ρ is **monotone-height** — it can only increase enfilade height, never decrease it [SS-ENFILADE-TREE, INV-ENFILADE-MINIMALITY]. Preserves the abstract V→I mapping; changes only the physical tree shape.

**K.σ** — spanfilade write. Fires on INSERT and COPY (DOCISPAN entries), and on CREATE_LINK (link-endpoint entries tagged LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN). Strictly append-only; no deletion path exists anywhere in `spanf1.c` or `spanf2.c` [INV-SPANF-WRITE-ONLY]. The DOCISPAN and link-endpoint writes share the same `insertspanf`/`insertnd` mechanism but target different orgl-range subspaces in the 2D spanfilade [SS-DOCISPAN, SS-SPORGL, INT-SPORGL-LINK-INDEX].

---

## Gaps and refinements

### Gap 1: APPEND is K.α + K.μ⁺ without K.σ

APPEND [EC-APPEND-NO-DOCISPAN] allocates I-addresses and updates the POOM but has the DOCISPAN `insertspanf` call commented out. It is the composition K.α ∘ K.μ⁺ with K.σ explicitly absent. If the vocabulary is intended to generate all composed operations, this is not a new primitive kind but it is an observable variant that breaks the rule "INSERT = K.α + K.μ⁺ + K.σ always."

### Gap 2: K.σ has two structurally independent sub-kinds

The DOCISPAN write `insertspanf(..., DOCISPAN)` and the link-endpoint write `insertendsetsinspanf(...)` use different ORGLRANGE dimension prefixes in the 2D spanfilade [SS-DOCISPAN, INT-SPORGL-LINK-INDEX]. Their frame conditions differ: DELETE is a frame for the link-endpoint sub-index but not for DOCISPAN (which accumulates stale entries), and DOCISPAN granularity is per-I-span while link entries are per-sporgl. Whether K.σ should be split into K.σ_D (DOCISPAN) and K.σ_L (link index) depends on how fine-grained the spec needs to be for the spanfilade invariants.

### Gap 3: K.δ and K.μ⁻ always co-occur but are logically independent

K.δ removes the (V, I) entries that fall within the deletion range. K.μ⁻ shifts the entries after the range. Both fire on every DELETE that has anything after the deletion point, but [PRE-DELETE, Finding 0075] the boundary-cut optimization means K.δ can fire without splitting crums (when boundaries align), and K.μ⁻ can fire with zero shift (when deletion is at document end). Keeping them separate is correct; they are not always paired.

### Gap 4: Session-state transitions absent

If Σ includes BERT table state [SS-BERT, PRE-OPEN-DOC], there are at least two additional kinds: OPEN (acquires READBERT or WRITEBERT entry) and CLOSE (releases the entry). These modify no content, but `checkforopen` preconditions gate whether K.δ/K.μ⁺ etc. actually execute [PRE-INSERT, EC-RESPONSE-BEFORE-CHECK]. If Σ is defined as document content state only (granfilade + spanfilade + POOMs), these are out of scope and the vocabulary is complete on that layer.

### Non-issue: VERSION

VERSION uses K.α (doc address) + K.μ⁺ (POOM copy via `docopyinternal`) + K.σ (DOCISPAN for new doc). No new kind needed [ST-VERSION, FC-GRANF-ON-VERSION]. The key fact is that VERSION does not invoke K.α for content — only for the document address — which is why it does not break I-address contiguity for subsequent INSERTs [INV-MONOTONIC, Finding 0077].

---

## Verdict

For Σ = {granfilade, spanfilade, POOMs}, the vocabulary `{K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ} ∪ {K.σ}` is **complete** subject to two open decisions:

1. Whether K.σ is treated as a single kind with a sub-index parameter, or split into K.σ_D / K.σ_L. The frame conditions differ between them, so the split is defensible.

2. Whether K.ρ needs to be qualified as **monotone-only** (levelpull disabled) to avoid giving the impression that tree height can decrease. It cannot, under the current implementation.

No additional primitive kinds modify Σ beyond these nine. APPEND and COPY are compositions of existing kinds, not new primitives.

---

## Code Exploration

I now have the complete picture from the source code. Let me compile the authoritative answer.

---

## Complete Enumeration of State-Transition Kinds

### Σ — System State Components

From the code, Σ decomposes into four independently mutable layers:

| Layer | Contents | Mutating mechanism |
|-------|----------|-------------------|
| Σ₁ | Granfilade — immutable content + orgl structures | `createorglingranf`, `insertseq` |
| Σ₂ | POOMs — per-document V→I mappings | `insertpm`, `deletend`, `rearrangend` |
| Σ₃ | Spanfilade — DOCISPAN + SPORGL + link-endset index | `insertspanf` |
| Σ₄ | BERT — open-document access registry | `addtoopen`, `removefromopen` |

---

### All State-Mutating FEBE Operations (from `fns.c`)

**Content mutations:**

```
insert           → doinsert      [do1.c:87]
copy             → docopy        [do1.c:45]
rearrange        → dorearrange   [do1.c:34]
deletevspan      → dodeletevspan [do1.c:158]
createlink       → docreatelink  [do1.c:195]
createnewversion → docreatenewversion [do1.c:260]
createnewdocument → docreatenewdocument [do1.c:234]   ← note
createnode_or_account → docreatenode_or_account [do1.c:243]
myopen           → doopen        [fns.c:388]
myclose          → doclose       [fns.c:404]
```

---

### Mapping Proposed K.* to Code

| K.* | Code entry | Σ effects | Notes |
|-----|-----------|-----------|-------|
| K.α | `doinsert` [do1.c:87] → `inserttextingranf` + `docopy` | Σ₁ + Σ₂ + Σ₃ | New I-addresses allocated; text in granf; POOM entry; DOCISPAN in spanf |
| K.δ | `dodeletevspan` [do1.c:158] → `deletend` [edit.c:31] with V ∈ 1.x | Σ₂ only | POOM entries removed + shifted left; granf/spanf frozen |
| K.μ⁺ | `docopy` [do1.c:45] → `insertpm` + `insertspanf(DOCISPAN)` | Σ₂ + Σ₃ | Reuses existing I-addresses; no granf write |
| K.μ⁻ | `dodeletevspan` [do1.c:158] with V ∈ 2.x | Σ₂ only | Link-subspace POOM removal; same code path as K.δ but semantically distinct — link orgl persists in Σ₁/Σ₃ |
| K.μ~ | `dorearrange` [do1.c:34] → `rearrangend` [edit.c:78] | Σ₂ only | Pure V-address permutation; `tumbleradd` on POOM displacements; no I-address change |
| K.λ | `createorglingranf` [do1.c:209] + `insertendsetsinorgl` [do2.c:130] | Σ₁ | Allocates link orgl; populates its internal 2D enfilade with endset I-spans |
| K.μ⁺_L | `docopy(docisaptr, linkvsa, ispanset)` [do1.c:212] | Σ₂ + Σ₃ | Inserts link ISA into document POOM at 2.x subspace; also creates DOCISPAN via `insertspanf` inside `docopy` |
| K.ρ | `docreatenewversion` [do1.c:260-298] | Σ₁ + Σ₂ + Σ₃ + Σ₄ | `createorglingranf` + `addtoopen` + `docopyinternal` (text only) + `logbertmodified` + `doclose` |
| K.σ | `insertspanf` [spanf1.c:15] → `insertnd` on spanf | Σ₃ | Sub-operation embedded in K.α, K.μ⁺, K.μ⁺_L, K.ρ; also `insertendsetsinspanf` [do2.c:116] for K.λ |

---

### Gaps: Transitions Modifying Σ Not Covered

**Gap 1: `docreatenewdocument` [do1.c:234-241]**

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr) {
    typehint hint;
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));  // line 240
}
```

This is invoked by the FEBE `createnewdocument` handler [fns.c:276-286]. It calls **only** `createorglingranf` — no `docopyinternal`, no `addtoopen`, no `insertspanf`. It modifies Σ₁ (creates an empty orgl in granfilade) but touches no other Σ layer.

**K.ρ as documented in `ST-VERSION-CREATE` (kb-synthesis.md:604) copies text content and creates DOCISPAN entries. `docreatenewdocument` does neither.** These are structurally distinct:

| | `docreatenewdocument` | `docreatenewversion` (K.ρ) |
|-|----------------------|--------------------------|
| `createorglingranf` | ✓ [do1.c:240] | ✓ [do1.c:277] |
| `doretrievedocvspanfoo` | ✗ | ✓ [do1.c:281] |
| `addtoopen` | ✗ | ✓ [do1.c:292] |
| `docopyinternal` | ✗ | ✓ [do1.c:293] |
| `logbertmodified` / `doclose` | ✗ | ✓ [do1.c:295-296] |
| Σ₃ DOCISPAN created | ✗ | ✓ |

**Verdict**: If K.ρ is generalized to "any new document-orgl allocation", it subsumes `docreatenewdocument` as the degenerate K.ρ with empty source. If K.ρ strictly means "version-fork from existing content", `docreatenewdocument` is an unaccounted-for transition — call it **K.ρ₀** or **K.ν**.

**Gap 2: K.σ has two sub-types**

`insertspanf` is called with two different `spantype` values, writing structurally different entries:

- **DOCISPAN** writes: from `docopy` [do1.c:62] — `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)`. Maps document ISA → I-address range. Subject of ASN-0047.
- **SPORGL/LOCID** writes: from `insertendsetsinspanf` [do2.c:116-128] — `insertspanf(taskptr, spanf, linkisaptr, fromsporglset, ...)`. Maps link ISA → endpoint I-span for link discovery.

These are written to the same spanfilade but represent different entry types (DOCISPAN for content discovery, SPORGL for link search). If K.σ covers both, it is complete. If K.σ specifically means the DOCISPAN write (as suggested by its connection to ASN-0047), then link-endset spanfilade writes need their own symbol.

**Gap 3: BERT mutations (Σ₄)**

`myopen` [fns.c:388] → `doopen` and `myclose` [fns.c:404] → `doclose` modify the BERT access table. These are not K.ρ sub-operations — they are independently callable FEBE operations. `docreatenewversion` happens to call `addtoopen` + `doclose` internally [do1.c:292-296], but `myopen`/`myclose` are also standalone FEBE operations that modify Σ₄ without touching Σ₁–Σ₃.

**If Σ includes Σ₄ (BERT state), two transitions are missing from the vocabulary.** If Σ is defined as content-layer state only (Σ₁ + Σ₂ + Σ₃), this gap is excluded by scope.

**Gap 4: Enfilade structural height (sub-transition of K.μ⁺/K.α)**

`levelpush` [genf.c:263-294] is "the only transition that modifies height, and it only increments" [kb-formal.md:1222]. It modifies a field in Σ₁/Σ₂ (the fullcrum's `height` counter). However, it is always triggered internally by `splitcrumupwards` which is itself a sub-operation of `insertseq` (part of K.α) or `insertnd` (part of K.μ⁺). It is never a standalone transition. This is a sub-operation of existing K.* kinds, not a gap.

---

### Is {K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ} ∪ {K.σ} Complete?

**At the FEBE semantic level (Σ = Σ₁ + Σ₂ + Σ₃), with two caveats:**

**The vocabulary is complete with these resolutions:**

1. **K.ρ must cover both `docreatenewversion` and `docreatenewdocument`**: The FEBE exposes both. If K.ρ is "new document-orgl allocation" (possibly with content copy), it covers both. The synthesis entry [kb-synthesis.md:604] describes `ST-CREATENEWVERSION`; the `createnewdocument` FEBE call [fns.c:276] has no equivalent ST-* entry in the KB — this is an existing gap in the formal KB documentation.

2. **K.σ must cover SPORGL writes as well as DOCISPAN writes**: `insertendsetsinspanf` [do2.c:116] creates SPORGL entries distinct from the DOCISPAN entries covered by ASN-0047. If K.σ = "any `insertspanf` call", it is complete. If K.σ = "DOCISPAN write only", link-endset writes lack a label.

3. **K.δ and K.μ⁻ are genuinely distinct** despite using the same `dodeletevspan` [do1.c:158] / `deletevspanpm` [orglinks.c:145] / `deletend` [edit.c:31] code path: K.δ removes from subspace 1.x (text, with semantic content loss); K.μ⁻ removes from subspace 2.x (link reference, with link-orgl surviving in Σ₁). The `strongsub` exponent guard [tumble.c:534-547] that isolates subspaces [kb-synthesis.md:656-668] makes these structurally separate even though the code path is shared.

**If Σ also includes Σ₄ (BERT/session state), the vocabulary is incomplete**: `myopen`/`myclose` [fns.c:388, 404] are standalone Σ₄-modifying FEBE operations not covered by any K.* kind.

---

### The Unaccounted Transition: `docreatenewdocument` [do1.c:234]

The single most significant gap vs. what the KB currently documents is that **`createnewdocument`** as a FEBE operation [fns.c:276] has no ST-* entry and maps only ambiguously to K.ρ. It is the call that initializes an empty document before any content exists — it is how the system creates the root document before `insert` can be called. Its postcondition is simply:

```
Σ₁' = Σ₁ ∪ { new empty orgl at hint(ACCOUNT, DOCUMENT, account) }
Σ₂' = Σ₂   (no POOM content)
Σ₃' = Σ₃   (no spanfilade entry)
```

K.ρ's postcondition as documented involves `docopyinternal` which creates POOM entries and DOCISPAN records. That postcondition does not apply to `docreatenewdocument`. **This is a transition modifying Σ that requires either expanding K.ρ's definition or adding a distinct symbol.**

---

### Verdict

`{K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ} ∪ {K.σ}` covers all state transitions for the content-layer (Σ₁–Σ₃) **if**:
1. K.ρ is defined as "new document-orgl allocation (with optional content copy from source)" — covering both `docreatenewdocument` [do1.c:234] and `docreatenewversion` [do1.c:260]
2. K.σ is defined as "any `insertspanf` call" — covering DOCISPAN writes from K.α/K.μ⁺/K.μ⁺_L/K.ρ and SPORGL writes from K.λ's `insertendsetsinspanf` [do2.c:116]

**The vocabulary is NOT complete as a standalone account if Σ includes Σ₄ (BERT state)**: `myopen`/`myclose` [fns.c:388, 404] are independently-invocable FEBE operations modifying only Σ₄ with no K.* label.

ASN-0098, if written, should cover: (a) the K.ρ definition disambiguation, (b) K.σ's two sub-types (DOCISPAN vs. SPORGL), and (c) whether BERT mutations are inside or outside Σ.
