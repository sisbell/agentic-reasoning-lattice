This is a strong, careful digest — accurate on the forced/conventional split, well-grounded in the note and the evidence answers, and at the right altitude throughout. I checked every Green source-level claim against the note + evidence and found none fabricated. Several sections are genuinely sharp and I'll call them out. I found no material defects — only precision improvements.

**Genuinely solid, no action needed:**
- *Design commitments* — the forced/conventional partition is right, and the qualifications are exactly the load-bearing ones (M3's "hint-status is a builder decision, not forced"; M16a's T10a/prefix precondition; M12 *merge*-order vs *edit*-order independence).
- *Merge/canonicalize* — "I-adjacency already subsumes both cross-origin (M16) and shared-I-extent (M14a)" is correct and the key simplification; the origin-prefix short-circuit is correctly grounded in evidence + the note's homedoc guard.
- *Resolution* — "clip + coalesce, with clip-alone as the eager-mode specialization, tied to canonicalization timing" is algorithmically correct (a sub-slice of a canonical decomposition is canonical; a lazy store's scan can surface mergeable pairs).
- *Persistence* — "replay must preserve journal order; M12 governs merge order, not edit order; insert/delete/copy don't commute" is an excellent, correct distinction.
- *Multi-subspace* — the observation that link-creation writes straddle two trees (so a unified document tree is *not* an atomicity device) is sharp and correctly cuts against an over-reading of the evidence.

---

# Revision list

**1. [SHARPENING] Guarantees → Resolution integrity (C1): "blocks never reference dead content" misframes S3 against the permanence model.** In this model content is permanent — the digest's own "Content permanence/immutability" commitment — so there is no "dead" content. What S3 (ReferentialIntegrity) forbids is a block naming an I-address *not in `dom(C)`* (an unallocated/dangling reference), not a deleted one. The S3 citation that follows is correct, so the build instruction survives; but reword the gloss to "blocks reference only addresses in `dom(C)` (no dangling/unallocated references)" so the prose doesn't import a content-death notion the model rejects.

**2. [SHARPENING] Width approach vs. Width-representation decision read as in tension on `#v` vs `#a`.** The *Width* approach asserts "`#v` need not equal `#a`" as settled, while *Decisions* flags the V-start/I-start depth relationship as "open per the note" (Open Q4). Both are individually correct — M0 couples the *count*, not the depths, and Green demonstrably encodes that count at each dimension's own depth, so inequality is permitted and is Green's actual encoding; what remains open is whether anything *further* constrains the relationship. Harmonize them: in the Width paragraph, note that while inequality is permitted (and is Green's encoding), the precise `#v`–`#a` constraint is open (Q4) — which is *why* the scalar form safely assumes nothing about it.

**3. [SHARPENING] Persistence + Upstream: tighten the permascroll/granfilade roles.** Both sections lump "permascroll/granfilade" as "the append-only substrate for the content." The permascroll is the append-only content substrate; the granfilade is the enfilade that *indexes/allocates* I-addresses into it (monotonic allocation, per evidence Q5). The persistence analogy (content has an append-only substrate → arrangement writes could have a journal) is unaffected, but the role distinction matters for a builder interfacing with content store `C`.

**4. [SHARPENING] Store approach: "adjusting one ancestor's displacement" is inconsistent with the same sentence's "O(log n) bulk address-shifting."** A cumulative enfilade shifts a downstream region by adjusting displacement at the O(log n) right-of-path nodes, not literally one ancestor. Say "O(log n) displacement adjustments along the path" to match the stated bound.

VERDICT: CONVERGED
