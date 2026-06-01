# Review of ASN-0047

## REVISE

### Issue 1: D-CTG★/D-MIN★ adopted on the link subspace despite the ASN's own admission that they contradict the design

**ASN-0047, *Amendments to existing transitions*, "Modeling choice (provisional, in tension with the design intent)"**: "D-CTG★/D-MIN★ ... are *incompatible* with that intent ... The strengthening is therefore not justified against Nelson's design — it contradicts it," and the reconciliation "is **unresolved at the point this invariant is introduced**, not merely a downstream open question."

**Problem**: D-CTG★/D-MIN★ on `s_L` are not isolated — they are load-bearing. D-SEQ★ is *derived* from them; K.μ⁻'s per-subspace suffix-removal admissibility for links depends on them; the link-allocation worked example (Step 5, and its "interior withdrawal is excluded" claim) depends on them; CL-UNIQ/Link-subspace-fixity reasoning rides on the resulting canonical shape. An invariant cannot be simultaneously declared "not justified ... it contradicts [the design]" / "unresolved" and used as a foundation for downstream proofs. If the eventual tombstoning reconciliation admits interior gaps in `V_{s_L}(d)`, D-CTG★ for links is false and the dependent results collapse. The accompanying two-paragraph essay (including the udanax-green `edit.c` code archaeology — "case 1 `disown`/`subtreefree`, case 2 `tumblersub`, then `recombine`") is defensive justification prose in a structural slot, signalling the unresolved status rather than discharging it.

**Required**: Either (a) retain the foundation's link-subspace exemption (inherit D-CTG/D-MIN unstrengthened for `s_L`, decoupling the link-subspace proofs and K.μ⁻'s link contraction from the dense-contiguous shape and allowing interior withdrawal/tombstoning), or (b) supply the missing justification that the arrangement layer *requires* a gap-free, minimum-anchored link subspace, discharging the "unresolved" status before building D-SEQ★ and the Step-5 contraction claims on it. Trim the provisional essay once resolved.

### Issue 2: K.δ case (ii) freshness for k ∈ {1,2} is claimed "discharged by an axiom" when it is in fact a caller-checked guard

**ASN-0047, K.δ, case (ii), "Per-k freshness mechanism (stated once here)"**: "at k = 0 the frontier check `inc(t, 0) ∉ E` is a caller-checked guard ... at k ∈ {1, 2} the conjunct `e ∉ E` is discharged by T10a's *direct* per-`(t, k')` uniqueness axiom, which fires each `(t, k')` child-spawn at most once."

**Problem**: The asymmetry is backwards. T10a's "each `(t, k')` yields at most one child-spawning event" is a property *maintained by conforming executions*, not a fact that establishes `e ∉ E` at an arbitrary firing. Nothing intrinsic prevents a caller from versioning the same document `t` twice (k=1) or descending from the same `t` twice (k=2); the only thing that prevents a duplicate `inc(t,k')` from entering E is the precondition `e ∉ E` being checked — exactly as at k=0. So `e ∉ E` at k ∈ {1,2} is a caller-checked guard that *enforces* the at-most-once discipline, not a consequence of it. The current framing points to a discipline property that presupposes the conclusion, leaving freshness at k ∈ {1,2} not actually discharged.

**Required**: State `e ∉ E` at k ∈ {1,2} as a caller-checked guard (parallel to the k=0 frontier check), with T10a's per-`(t,k')` uniqueness named as the discipline property that guard *maintains*, not as the discharge of freshness.

## OUT_OF_SCOPE

### Topic 1: Tombstoning / link-withdrawal mechanism
**Why out of scope**: A separate withdrawal mechanism (status flag, tombstone, retraction link) reconciling Nelson's tombstoning with presentational removal is genuinely new territory and is correctly listed under Open Questions. Note this is distinct from Issue 1 — Issue 1 is that the *current* ASN adopts a self-contradicting load-bearing invariant, not that the future mechanism is missing.

VERDICT: REVISE
