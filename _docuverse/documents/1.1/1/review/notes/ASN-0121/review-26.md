# Review of ASN-0121

## REVISE

### Issue 1: FL-WP case (b) — the "full post-state index" exact-increment equation is not exact

**ASN-0121, FL-WP case (b) derivation (parenthetical)**: "(Over the full post-state index `dom(Σ'.L)` the exact increment is `nullified(Σ') = nullified(Σ) ∪ {t ∈ dom(Σ'.L) : t ∈ coverage(G')}`, which the singleton-extension premise `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}` discharges alongside R6b; on the `dom(Σ.L)` slice the two index sets agree.)"

**Problem**: The equation, stated as "exact" over the full index `dom(Σ'.L)`, is false. The fresh retractor address `b ∈ dom(Σ'.L) \ dom(Σ.L)` may be covered by a *pre-existing* retraction tuple `(c, F'', G'') ∈ L_R^Σ` (the ghost-pre-coverage mechanism the ASN itself endorses in case (a) and Trace 7). In that scenario `b ∈ nullified(Σ')` via the pre-existing tuple, yet `b ∉ nullified(Σ)` (b is fresh) and `b ∉ {t ∈ dom(Σ'.L) : t ∈ coverage(G')}` whenever `b ∉ coverage(G')` (b does not self-retract). So the RHS omits `b` while the LHS contains it: the two sets disagree on `b`, and the displayed equation is wrong over the full index. The newly-nullified set is `(dom(Σ.L) ∩ coverage(G') \ nullified(Σ))` plus the fresh `b` nullified by *either* `G'` *or* a pre-existing tuple — the latter term is missing.

**Required**: Either restrict the parenthetical to the `dom(Σ.L)` slice (where it is correct, and which is all case (b) actually uses), or add the missing `b`-by-pre-existing-coverage term. The main case-(b) equation on the existing-link slice (`a ∈ nullified(Σ') ⟺ a ∈ nullified(Σ) ∨ a ∈ coverage(G')`) is correct and load-bearing; only this "full index … exact" aside is defective.

### Issue 2: FL-WP — "weakest precondition" stated without the K.λ enabledness conjunct

**ASN-0121, FL-WP cases (a)/(c)**: each is introduced as "Let `Σ → Σ'` be a K.λ step that allocates a fresh address …", and the displayed conjunction is called the weakest precondition.

**Problem**: The displayed wp is the weakest precondition *conditional on the K.λ step occurring with those arguments*; it omits the operation's own applicability predicate (freshness `ℓ ∉ dom(Σ.L)`, L3 well-formedness, `home(ℓ) ∈ dom(Σ.M)`). The foundation's analogous treatment (ASN-0086 wp Case 2) explicitly carries `enabled(K.μ⁻[d, R])` as a wp conjunct. As written, FL-WP's "weakest precondition" terminology is stronger than what is established.

**Required**: Either fold the K.λ enabledness/applicability predicate into the displayed wp (matching ASN-0086's precedent), or state explicitly that FL-WP gives the weakest *additional* precondition given the step is enabled.

## OUT_OF_SCOPE

(none — the open questions on version-qualified inquiry, V-spec/I-address agreement, and federation are correctly marked as open questions, not claims; no excluded-operation claims appear)

VERDICT: REVISE
