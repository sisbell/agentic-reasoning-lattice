## Question 2 [evidence]

> Does ASN-0036 export claims for element-field depth and for two-stream (content/arrangement) separation, and is S7 (StructuralAttribution) defined over exactly S7a, S7b, S7d with no S7c?

## KB Synthesis

The KB provided does not contain information about ASN-0036 as a named specification unit, nor does it reference "S7", "StructuralAttribution", or any sub-claim identifiers (S7a, S7b, S7c, S7d).

**What the KB does cover that is adjacent to your question:**

**Element-field depth** is addressed in [SS-ADDRESS-SPACE] (Finding 0065), which defines the address structure `account.0.document.0.element_field.element_number` where element_field=2 for links and element_field=3 for text, with monotonic allocation scoped per-document.

**Two-stream separation** is addressed in [SS-POOM-MUTABILITY] and [SS-DUAL-ENFILADE], which distinguish the immutable/append-only granfilade (content identity, I-addresses) from the mutable POOM (arrangement, V-to-I mapping). These are the two streams: content permanence vs. current arrangement.

**However**, whether ASN-0036 exports claims for these specific properties, and whether S7 (StructuralAttribution) is defined over exactly {S7a, S7b, S7d} omitting S7c, cannot be answered from this KB. Those are claims about a specification document's structure that is not present in the findings.

---

## Code Exploration

The search is complete. Here is my full answer:

---

## Answer

**Neither "ASN-0036", "S7/StructuralAttribution", "element-field depth" (as a phrase), nor "two-stream" appear anywhere in this repository.**

### What "ASN-0036" maps to (if anything)

There is no label "ASN-0036" in the codebase. The nearest item is **Finding 0036**, documented in:
- `findings/0036-insert-creates-docispan.md`
- `knowledge-base/analyzed/0036.md`

Finding 0036 is about **DOCISPAN insertion** — the fact that `doinsert` → `docopy` → `insertspanf(..., DOCISPAN)` (at `do1.c:62`) creates reverse-index entries in the spanfilade, making inserted content discoverable via `find_documents`. APPEND does not (`do1.c:25-31`, commented-out call).

The entries exported from `knowledge-base/analyzed/0036.md` are:
- `SS-DOCISPAN` — spanfilade type 4 reverse index
- `ST-INSERT` — INSERT postcondition on granf and spanf
- `ST-INSERT-ACCUMULATE` — DOCISPAN entries accumulate monotonically
- `PRE-INSERT` — INSERT precondition chain
- `EC-APPEND-NO-DOCISPAN` — APPEND frame condition (spanf unchanged)
- `FC-CONTENT-SPANF-ISOLATION` — refinement of granf/spanf access pattern from Finding 0012

**None of these are claims about "element-field depth" or "two-stream (content/arrangement) separation."** Those terms do not appear in Finding 0036 or anywhere else in this repository.

### S7 / StructuralAttribution

The labels `S7`, `S7a`, `S7b`, `S7c`, `S7d`, and `StructuralAttribution` appear **nowhere** in this repository — not in `kb-formal.md` (8,714 lines), `kb-synthesis.md`, any `knowledge-base/analyzed/*.md` file, any finding, or any source file.

### Conclusion

ASN-0036 does not exist in this repository; S7 (StructuralAttribution) does not exist in this repository. The question cannot be answered from the current codebase — the identifiers and schema it references have no presence here. If these come from an external spec or document, that document needs to be provided before the question can be evaluated.
