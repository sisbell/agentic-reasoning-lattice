# Review of ASN-0131

## REVISE

### Issue 1: RE-RET's core stability result is overclaimed as unconditional — the type-slot re-witnessing case breaks it

**ASN-0131, "Under retraction" / RE-RET**: "But the hypothesis governs only this net-removal-only flavour. **The core stability result below does not rest on it**: the emitter's only possible content-region contribution is the single pair `(3, Θ)`, carrying the retraction type — **a value distinct from any anchoring endset a retracted link bears** — so `b` can re-witness no pair `(i, e)` that `ℓ` itself bore." And the claims table, RE-RET row: "**Core result (unconditional)**: … a pair `(i, e)` that `ℓ` bore drops **iff `ℓ` was its sole addressable bearer in `Σ`**."

**Problem**: The forward direction (sole addressable bearer ⟹ the pair drops) fails for the type-slot pair `(3, Θ)`, and it fails in exactly the regime the note itself admits is reachable.

RE-DEF ranges `i` over **all** slots `1 ≤ i ≤ |Σ.L(a)|`, type slot included (RE-OVL: "no per-slot request differentiation"; the worked instance tests `e₃` directly). So `(3, Θ)` is a legitimate RE pair. Now construct the counterexample:

- Drop the net-removal-only hypothesis, i.e. `coverage(Θ) ∩ dom(Σ.C) ≠ ∅` — the note grants this is possible ("absent that hypothesis, a `Θ` meeting the image would surface the emitter as the fresh pair `(3, Θ)`").
- Let the retracted link `ℓ` be itself a retraction link (P-tgt admits any `a ∈ A_rel^Σ`; R6b/R6c, ASN-0086, treat retraction-of-retraction). Then `ℓ.e₃ = Θ` (the canonical representative Emit_R always deposits), so `ℓ` bears `(3, Θ)`. Suppose `coverage(Θ)` meets the region image, so `touch_W(Θ)` holds and `(3, Θ) ∈ RE(W, d, Σ)` witnessed by `ℓ`; let `ℓ` be the **sole addressable bearer** of `(3, Θ)`.

Retract `ℓ`. The same step emits `b` with `b.e₃ = Θ`, `b ∈ addressable(Σ')`, and `touch_W(Θ)` is unchanged (coverage is permanent), so `(3, Θ) ∈ RE(W, d, Σ')` re-witnessed by `b`. The pair does **not** drop, although `ℓ` was the sole addressable bearer in `Σ`. The "distinct from any **anchoring** endset" justification silently narrows to from/to slots; but a retraction link's *type* slot is `Θ`, and the type slot is surfaced.

This is precisely the type-slot-against-content-region territory the note already flags as semantically open in Open Question 6 — yet RE-RET quantifies over it and asserts unconditionality.

**Required**: Either (a) attach the net-removal-only hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` to the core result — under it `touch_W(Θ)` is always false since `I ⊆ dom(Σ.C)`, so `(3, Θ)` is never an RE pair and the gap closes; or (b) restrict the "drops iff sole addressable bearer" claim to anchoring slots `i ∈ {1, 2}` and explicitly route the `(3, Θ)` type-slot case to Open Question 6. Delete the sentence "The core stability result below does not rest on it" — as written it is false.

### Issue 2: RE-WHOLE's provisionality is deferred to Open Question 1 in three separate places

**ASN-0131, "Faithfulness…" / "A worked instance" / Claims table**: the provisional status of RE-WHOLE pending Open Question 1 is stated three times — "reopened as Open Question 1; we therefore hold RE-WHOLE **provisional** pending its resolution" (faithfulness); "is precisely the volunteered out-of-region anchoring Open Question 1 weighs; **we report it provisionally with RE-WHOLE**" (worked instance); "**Held provisional pending Open Question 1**" (table).

**Problem**: Matches the anti-bloat pattern "multiple paragraphs in different sections defer to the same downstream location." The worked-instance restatement in particular re-litigates a status already fixed at RE-WHOLE's definition; the instance only needs to *exhibit* the two readings' outputs (`{(a₂,δ(2,#a₂))}` vs. the full two-span endset), which it does, without re-announcing the deferral.

**Required**: State RE-WHOLE's provisionality once (at its definition), let the table carry the status tag, and drop the worked-instance deferral sentence.

### Issue 3: The Stability "full taxonomy" paragraph accretes forward-reference navigation and vocabulary asides

**ASN-0131, "Stability…", the "full taxonomy" paragraph**: it carries "made exact in RE-CWP below" (twice), "shown under *Under retraction*, below," "the deletion motion above," plus a vocabulary aside that does not advance the classification: "(… **Where the extension side divides into two transition kinds — K.μ⁺ for content, K.μ⁺_L for link — contraction handles both subspaces within the one per-subspace K.μ⁻.**)".

**Problem**: The reader must skip the inline pre-announcements of RE-CWP and the retraction subsection (which follow immediately) to follow the transition classification, and the parenthetical's second sentence is commentary on the transition-vocabulary's shape, not part of the stability argument — "essay content in a structural slot." Both compound the "multiple deferrals to the same downstream location" pattern.

**Required**: Reduce the taxonomy paragraph to the classification itself (which transition moves the answer through which channel). RE-CWP and RE-RET are the very next subsections; they need no inline forward pointer. Drop the extension-splits-into-two vs. contraction-is-one aside.

### Issue 4: The s_C-restriction justification enumerates its downstream consumers

**ASN-0131, "The region, and what it resolves to"**: "Confining `W` to `s_C` keeps 'content-image' literally accurate and **keeps the whole development — the worked instance, the exactness of retraction stability (below), the completeness phrasing — on content.**"

**Problem**: This is a use-site inventory ("enumerates downstream consumers") attached to a precondition's justification. The actual reason `W ⊆ s_C` is the right domain is the prior sentence's content (the image then lies in `dom(Σ.C)` by S3★); listing which later passages benefit from it is meta-prose the reader works around.

**Required**: Keep the substantive reason (the image is content-valued); drop the enumeration "the worked instance, the exactness of retraction stability, the completeness phrasing."

## OUT_OF_SCOPE

### Topic 1: Type-slot matches against a content region
**Why out of scope**: The note correctly routes the *semantics* of a type-slot match against a content region to Open Question 6, and the link-subspace region to Open Question 7; intersection-distributivity to Open Question 4; non-co-resident link stores to Open Question 5. These deferrals are appropriately scoped and need no new claims here. (Note, however, that Issue 1 is *not* covered by OQ6: OQ6 asks what such a match *means*, whereas RE-RET makes a definite — and incorrect — stability *claim* that quantifies over the type slot. The OQ6 deferral does not license the unconditional RE-RET claim.)

META: The ASN is squarely in specification territory — it defines a state query, its read-set, its boundary behavior, and its invariants under the transition vocabulary, all stated abstractly enough that any implementation would have to satisfy them; it has not drifted to implementation mechanics.

VERDICT: REVISE
