# Review of ASN-0117

I read the full ASN, checked each P-claim and DEL-clause against its cited foundation lemma (ASN-0082's contraction family, ASN-0098's projection/discoverability lemmas), and verified the worked example and the discoverability wp. The two-layer discipline, the gap-closure arithmetic (`σ(q_k) = q_{k−c}`, `ord(r) ⊖ w_ord = ord(p)`), the boundary cases (suffix delete with `R = ∅`, full delete `N' = 0`, within-document sharing), the count-based statement of DEL-REMOVE, and the per-link existential wp are all handled correctly and rigorously. One derivation gap and one example-depth point remain.

## REVISE

### Issue 1: `ran(M'(d)) ⊆ ran(M(d))` is derived only over the text subspace

**ASN-0117, "Link survival, and discoverability across documents" (P4 paragraph)**: "DELETE shrinks `d`'s range — `ran(M'(d)) ⊆ ran(M(d))` — directly from its own clauses: DEL-LEFT and DEL-SHIFT preserve every surviving position's I-address value ... so every I-address in `ran(M'(d))` already appears in `ran(M(d))`, while DEL-REMOVE drops the deleted correspondences and DEL-DOM fixes the surviving domain to `L ∪ σ(R)`."

**Problem**: `dom(M'(d))` is not `L ∪ σ(R)` — that is only the *text-subspace* surviving domain (DEL-DOM is explicitly scoped `{v ∈ dom(M'(d)) : subspace(v) = S} = L ∪ {σ(v) : v ∈ R}`). The full `dom(M'(d))` also contains the link-subspace positions `V_{s_L}(d)`, whose images contribute to `ran(M'(d))`. The justification offered ("every I-address in `ran(M'(d))` already appears in `ran(M(d))`") is established only for the text images on `L` and `σ(R)`; the link-subspace images are never accounted for in this derivation. The inclusion is in fact true — link positions are carried verbatim by DEL-FSUB, so their images lie in `ran(M(d))` — but that step is exactly the one omitted. This is the same two-subspace link-range subtlety that forced the recent lift of S3-post to S3★; it has not been propagated to the P4 range-inclusion derivation, which is load-bearing for the "deletion can only orphan, never resurrect" claim.

**Required**: Complete the derivation by citing DEL-FSUB: `ran(M'(d)) = M(d)(L) ∪ M(d)(R) ∪ ran(M(d)↾V_{s_L}(d))`, each summand ⊆ `ran(M(d))` (text via DEL-LEFT/DEL-SHIFT, link via DEL-FSUB), hence the inclusion. (The wp section later does this correctly; the same accounting is needed where the inclusion is first used.)

### Issue 2: the worked example never exercises a multi-position suffix shift

**ASN-0117, "A worked deletion"**: the primary scenario deletes `q_3, q_4` (`c = 2`) from `N = 5`, leaving `R = {q_5}` — a single suffix position.

**Problem**: DEL-SHIFT's signature behavior is the *uniform* left-shift of the entire suffix (`σ(q_k) = q_{k−c}` applied across `R`, order-preserving by D-BJ). With `|R| = 1` only one position moves, so the concrete check verifies gap closure (`σ(q_5) = q_3`) but never demonstrates that two or more following positions all shift by the same `c` while preserving their relative order — the operation's defining effect. The guideline requires the key postcondition to be verified against a specific scenario; the key postcondition here is multi-position uniform shift.

**Required**: Add (or extend) a scenario with `|R| ≥ 2` — e.g. delete `q_2` of width `c = 1` from `N = 5`, showing `q_3 → q_2, q_4 → q_3, q_5 → q_4` all shifting by 1 with order preserved — so the uniform-shift postcondition is concretely exercised.

## OUT_OF_SCOPE

### Topic 1: generalization beyond depth `m = 2`
**Why out of scope**: The ASN inherits the depth-2 text-case restriction directly from the foundation contraction (ASN-0082, `#p = 2`). Lifting DELETE to depth `m > 2` requires the foundation displacement work to generalize first; it is not an error in this ASN.

### Topic 2: concurrent deletion without a serializing authority, and exact backtrack reconstruction
**Why out of scope**: These are correctly deferred to the Open Questions — concurrency control and the backtrack/version-graph state needed for exact reconstruction are new territory beyond a single-document DELETE specification.

VERDICT: REVISE
