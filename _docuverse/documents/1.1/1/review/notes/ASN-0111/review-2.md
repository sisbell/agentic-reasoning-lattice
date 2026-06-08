# Review of ASN-0111

## REVISE

### Issue 1: Worked example mislabels coverage (intervals) as finite I-address sets

**ASN-0111, "A worked read"**: "The first, of width-2, covers the content addresses `[1.0.1.0.1.0.1.1]` and `[1.0.1.0.1.0.1.2]`" and "So `coverage(F)` is three I-addresses lying in two documents."

**Problem**: This contradicts the coverage definition the ASN itself quotes from the foundation: `coverage(e) = ∪ {t ∈ T : s ≤ t < s ⊕ ℓ}`. The first span `([1.0.1.0.1.0.1.1], δ(2,8))` has `s ⊕ ℓ = [1.0.1.0.1.0.1.3]`, so its coverage is the half-open interval `[ [1.0.1.0.1.0.1.1], [1.0.1.0.1.0.1.3] )`. By T1 case (ii) this interval contains not two tumblers but the full subtrees of `…1.1` and `…1.2` (e.g. `[1.0.1.0.1.0.1.1.0]`, `[1.0.1.0.1.0.1.2.5]`, …) — an infinite tumbler set. The second (width-1) span likewise covers an interval, not one address. So `coverage(F)` is a union of two intervals, not "three I-addresses." The same conflation recurs in RL8's orphan instance ("the three I-addresses in `coverage(F)`").

**Required**: State precisely that coverage is the interval set; the three figures are the *element-level content addresses arranged within* coverage(F), not coverage(F) itself. Distinguish "coverage interval" from "the I-addresses in coverage that host content," since the projection/discoverability machinery the example contrasts against (RL1 vs. search, RL8 orphan) turns on exactly this distinction.

### Issue 2: RL2's "three-way grouping" prose assumes arity 3, but the model and RL-ARITY admit N > 3

**ASN-0111, RL2 and "A worked read"**: "preserving the three-way grouping"; "The from / to / type distinction is a primitive"; worked example exercises only arity 3.

**Problem**: The formal RL2 (`readlink(a,Σ).eᵢ = Σ.L(a).eᵢ` for `1 ≤ i ≤ |Σ.L(a)|`) is general, but the surrounding prose describes the result as a three-way (from/to/type) grouping, and RL-ARITY plus L3 permit `N > 3`. For `N > 3`, slots 4…N carry no role under the prose, yet the read returns them. The single worked example never exercises `N > 3`, so the key postconditions are verified only for the dominant case, not the general one the claims assert.

**Required**: Reconcile prose with the general claim — state that for `N > 3` the read returns all N endsets, slots 1–3 carrying the standard from/to/type roles and slots 4+ being additional endsets returned faithfully — and verify the completeness/role-preservation postconditions against at least one `N > 3` instance, or explicitly restrict the operation's prose to the standard triple.

## OUT_OF_SCOPE

### Topic 1: Semantics of supernumerary endset slots (N > 3)

**Why out of scope**: Assigning *meaning* to endsets beyond slot 3 is link-model territory, not read territory. The read's only obligation is faithful return (covered once Issue 2's prose is fixed); what those slots denote belongs elsewhere.

VERDICT: REVISE
