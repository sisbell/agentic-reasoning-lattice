## Question 1 [evidence]

> Does the consultation evidence or knowledge base synthesis (specifically the material behind Q17) use "F0" as a named designation for the cross-document frame property, and if so, what is its exact statement and citation?

## KB Synthesis

The KB does reference "F0" but does not formally define it with an explicit statement or dedicate a named entry to it.

The only appearances of "F0" in the KB occur in [EC-GHOST-LINK-ENDPOINT] (Finding 0067), used informally twice:

> "This is NOT a violation of F0: the other document's structure is unchanged, the target document's POOM is correctly updated..."

> "F0 NOT violated: Doc B's structure is identical before and after"

No KB entry provides a formal statement for F0, no dedicated entry exists (there is no `FC-F0` or `INV-F0`), and no citation anchors it to a specific finding where it is introduced.

The KB does contain what appears to be the property F0 is gesturing at — the cross-document frame condition for DELETE — stated formally in [FC-DELETE-CROSS-DOC] (Finding 0064):

> `∀ D' ≠ D : delete(D, vspan) ⟹ poom(D') = poom_before(D')`

And more expansively: "DELETE operates on a single document's POOM tree only... Other documents' trees are separate data structures and are not touched."

A closely related named axiom in the KB is the permanence axiom **P0** (used in [SS-THREE-LAYER-MODEL], Finding 0040): "Cannot be deleted (permanence axiom P0)" for link orgls, and **P0'** for spanfilade monotonicity. These are explicitly named but pertain to I-space permanence, not the cross-document frame property.

**Summary:** The KB uses "F0" as an unnamed shorthand in [EC-GHOST-LINK-ENDPOINT] without ever stating or citing it formally. The property it refers to is the cross-document POOM isolation invariant, whose canonical statement appears in [FC-DELETE-CROSS-DOC]. The reference to "Q17" is not present anywhere in this KB — if that designation appears in a consultation document, it is not represented here.

---

## Code Exploration

I now have a complete picture. Here is my answer.

---

## Answer

**"Q17" does not exist anywhere in the knowledge base or findings of this repository.** A systematic search across all files in `knowledge-base/`, `findings/`, and the full working tree found zero matches for `Q17` or `Q-17`. There is no Q-numbered query or question scheme in these materials:

- `knowledge-base/kb-formal.md` uses Finding-numbered sub-sections (e.g., `#### Finding 0017`) grouped under named semantic categories (`SS-*`, `PRE-*`, `ST-*`, `FC-*`, `EC-*`).
- `knowledge-base/kb-synthesis.md` uses named sections only (`FC-DOC-ISOLATION`, `FC-SUBSPACE`, etc.).
- Neither file uses a `Q17` designation.

**Finding 0017** (`kb-formal.md:613`, `SS-VSPAN-VS-VSPANSET`) — the closest numbered item — has nothing to do with cross-document frame properties. It describes the difference between `RETRIEVEDOCVSPAN` (opcode 14, lossy bounding-box) and `RETRIEVEDOCVSPANSET` (opcode 1, subspace-aware spanset).

---

## "F0" as a Named Designation — What Exists

**Yes, "F0" is used as a named designation for the cross-document frame property**, but it originates in **Finding 0067**, not any Q17 material.

### Source: `findings/0067-frame-axiom-f0-confirmed.md`

The exact statement given is [`findings/0067-frame-axiom-f0-confirmed.md:26-32`]:

```
F0: ∀d ∈ D, ∀op ∈ {INSERT, DELETE, COPY}, ∀d' ∈ D where d ≠ d':
    op(d, ...) → D_seq'(d) ≠ D_seq(d) ∧ D_seq'(d') = D_seq(d')

Translation: An operation on document d modifies only d's text span sequence.
Other documents d' remain unchanged.
```

The finding attributes this to "the formal specification (EWD-009, EWD-012)" [`findings/0067-frame-axiom-f0-confirmed.md:24`].

Extended claims stated alongside it [`findings/0067-frame-axiom-f0-confirmed.md:35-37`]:
- Operations on document A do not modify document B's POOM
- Operations in text subspace (1.x) do not modify link subspace (2.x)
- Operations do not corrupt the spanfilade's ability to track content identity

### Reflected in `kb-synthesis.md:FC-DOC-ISOLATION` (line 692):

> Document operations (INSERT, DELETE, COPY, REARRANGE) modify only the target document's POOM. No mutations occur to other documents' POOMs, to the granfilade (except appending new content for INSERT), or to any other document's state. **Frame axiom F0: cross-document side effects do not exist.**

The spec-level formal statement there [`kb-synthesis.md:696`]:

> `∀ op, ∀ doc ≠ op.target: POOM_doc' = POOM_doc`. This is the strongest frame condition in the system.

### Reflected in `knowledge-base/analyzed/0067.md:FC-DOC-ISOLATION` (line 11):

> This is the central frame axiom F0: `∀d ∈ D, ∀op ∈ {INSERT, DELETE, COPY}, ∀d' ∈ D where d ≠ d': op(d, ...) ⟹ D_seq'(d') = D_seq(d')`.

---

## Summary

| Question | Answer |
|---|---|
| Does Q17 exist in the KB or synthesis? | **No.** No Q-numbered scheme exists anywhere in this repository. |
| Is F0 used as a named designation? | **Yes** — in `findings/0067`, `kb-synthesis.md:FC-DOC-ISOLATION`, and `analyzed/0067.md`. |
| What is F0's exact statement? | `∀d ∈ D, ∀op ∈ {INSERT,DELETE,COPY}, ∀d' ≠ d: op(d,...) ⟹ D_seq'(d') = D_seq(d')` — operations on document d leave all other documents d' unchanged. |
| What does ENF0 refer to? | A distinct concept: the element-type modification guard (`may-modify(orgl) ≡ element-type(orgl) ≠ LINKATOM`), defined in `kb-formal.md:PRE-ENF0-PLACEMENT-GAP`. Not the same as F0. |
