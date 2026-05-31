# Review of ASN-0084

I read the ASN in full, checked every lemma proof against its cited preconditions, traced all six worked examples arithmetically, and audited the foundation-invariant discharge and the anti-bloat patterns flagged by the classifier.

## Correctness audit (no issues found)

- **R-PIV / R-SWP totality and coverage**: ordinal-range tiling `[p, p+w_β) ⊎ [p+w_β, …)` is verified disjoint and exhaustive against `ord(c_{n-1})`; right-hand sides land in `[c₀, c_{n-1}) ∩ V_S(d) ⊆ dom(M(d))` via R-PRE(iv). Sound.
- **R-PPERM / R-SPERM bijectivity**: image ⊆ `dom(M(d))`, per-branch injectivity, cross-branch image-disjointness, and finite self-injection ⇒ surjection. Sound.
- **R-CANON forward/backward extension**: the `i ≥ 1` (resp. `j < n''−1`) branches correctly force a shared position, hence run-identity by B′ disjointness, then contradict shift-amount injectivity; the `i = 0` (resp. `j = n''−1`) branches expose a mergeable pair. The reduction to S8(c)'s uniqueness of the maximal-run partition is valid. Sound.
- **R-BLK run-partition**: Phase-1 split-at-cuts keeps each run within one region; reassembled V-extents `π(V(R)) = {π(v)+k}` (via R-COMM, same-region precondition discharged) partition `π(V_S(d)) = V_S(d)`; cross-group disjointness rests correctly on T10 (ASN-0034). S8-cons re-derivation uses the permutation defining equation plus R-COMM. Sound.
- **Worked examples**: I recomputed example 2 (`w_α=2, w_μ=1, w_β=3`) including the B+2=H merge to `([1,6],B,3)`; all six examples' postcondition values, π-checks, displacements, and merge decisions are correct and exercise distinct sub-cases (forward/fixed/backward μ, minimum-width boundary with empty exteriors, non-S pass-through).
- **Foundation discipline**: only ASN-0034 and ASN-0036 (the listed foundations) are referenced; `ord` is genuinely new notation (the complement of SubspaceProjection), not a reinvention. The depth-2 text-subspace scope restriction is stated and consistently applied; `D-CTG-depth` is correctly noted vacuous.
- **Anti-bloat pass**: I examined the "Post-state S8 discharge" non-circularity remark, the REARRANGE_K single-operation framing, the "R-S2 is not vacuous" note, and the Extended-Associativity-on-I-addresses step. Each is load-bearing — S8 is the one invariant not preserved by domain-equality alone and needs the fresh-application argument; the I-address associativity is explicitly justified "per the preamble" and rests on the depth-general TS3. No prose obstructs the claims, and the prior declined findings (OrdShiftHom (a)/(b); Phase-3 content in Phase-1) are genuinely absent.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The ASN fixes n ∈ {3,4} (CS1) and explicitly raises generalization as an open question. Extending the displacement structure to arbitrary cut counts is new territory.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: This ASN specifies a single REARRANGE_K transition. Whether composed rearrangements collapse to one is a sequencing property belonging to a later ASN.

### Topic 3: Cross-subspace transposition and m₁ > 2 documents
**Why out of scope**: Both are excluded by explicit scope restrictions (text subspace only, depth 2). They are deliberately deferred, not gaps in this ASN.

VERDICT: CONVERGED
