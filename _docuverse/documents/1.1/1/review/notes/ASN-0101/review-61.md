# Review of ASN-0101

I checked the formal content — the operation specification (D0), the gap-closure bijection (D1), the preservation theorems (D2–D8), the projection characterisation (D9), the composite extension (D10), and the wp calculations (D11). The mathematics is sound: the region partition `Λ ⊎ X ⊎ Π`, the shift-inverse `σ_d`, the source-correspondence discharge of S3★/CL-OWN/CL-UNIQ at re-mapped positions, and the three worked examples all hold up under checking. The boundary-case enumeration is genuinely exhaustive (empty post-state, start, end, singleton, interior, cross-subspace).

The findings below are confined to the accreted meta-prose that the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Cross-ASN naming-reconciliation parenthetical in a structural enumeration slot
**ASN-0101, D8 Group (ii)**: "SD (store disjointness — ASN-0093's name for the invariant that ASN-0047's ExtendedReachableStateInvariants theorem lists as L14)"

**Problem**: This parenthetical is pure cross-reference bookkeeping embedded in an invariant-name list. The enumeration's job is to name the frame-preserved invariants; the genealogy of which foundation ASN calls the invariant "SD" versus "L14" advances no part of the preservation argument. It is exactly the kind of naming-reconciliation noise the precise reader must skip past.

**Required**: Drop the parenthetical; cite the invariant by a single name (`SD`) consistent with the rest of the list.

### Issue 2: Roadmap pre-announcement in D10's "Neutrality" paragraph
**ASN-0101, D10, Neutrality**: "What the three bullets below establish is only that a DEL step cannot *break* any of P4★, P4a, P7a — not that they *hold* at `Σ'`."

**Problem**: This sentence narrates what the following bullets will and will not do rather than doing it. The load-bearing distinction (these are boundary properties, not per-state invariants, so DEL needn't preserve them per-state) is already made by the two preceding sentences and the concrete K.μ⁺/K.ρ example; the pre-announcement is scaffolding. This is the "explains why the argument is needed rather than what it says" pattern.

**Required**: Delete the roadmap sentence. The bullets and the subsequent "Boundary derivation" paragraph already make the per-state-vs-boundary split clear.

### Issue 3: Restatement of the no-reclamation consequence
**ASN-0101, D2**: the bullet "No I-address space is reclaimed. ..." followed by "The cardinality consequence is that `|dom(C)|` is unchanged across every DELETE transition. The implication for resource accounting is intentional: DELETE frees no storage."

**Problem**: The third bullet already states reclamation requires a separate operation and "DELETE itself does not provide one." The trailing two sentences restate the same point as a cardinality remark plus an essay aside ("The implication for resource accounting is intentional"). Two adjacent passages carry one claim.

**Required**: Fold the cardinality fact into the bullet or drop the trailing sentences; keep one statement of "DELETE frees no storage."

### Issue 4: Contrapositive restatement after D11
**ASN-0101, paragraph after D11**: "The opposite direction is also informative. Suppose we wish to ensure that DEL[d, σ] does *not* affect `ℓ`'s discoverability from `d`. By the contrapositive of D11's cardinality-preservation bullet, we require `project(L(ℓ).eᵢ, d, Σ) ∩ X = ∅` for every slot `i`. The slot-wise emptiness check is a per-slot, per-V-position test ... local in both the link and the deletion."

**Problem**: D11's cardinality-preservation bullet already states `wp(...) ≡ enabled ∧ project ∩ X = ∅`. This paragraph re-derives the same condition by contrapositive and closes with essay content ("local in both the link and the deletion") that adds no guarantee. It is a restatement of the bullet the reader just read.

**Required**: Remove the paragraph, or compress to a single clause appended to D11's diagnostic discussion if the "local test" framing is judged worth keeping.

## OUT_OF_SCOPE

None. The ASN correctly defers versioning/reconstruction (Open Question 1), DEL-then-INSERT recovery (Open Question 2), and orphan-enumeration mechanism (Open Question 4) rather than specifying them.

VERDICT: REVISE
