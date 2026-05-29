# Review of ASN-0040

## REVISE

### Issue 1: B8's proof rests on an unjustified — and false — "linear history" premise

**ASN-0040, B8 (Uniqueness), proof**: "This model admits only linear history — every reachable state extends one transition path from s_init — so both acts lie on a single transition path s_init →* s."

**Problem**: This claim is load-bearing for Case 1 (same namespace) and it is neither in B8's precondition list ("conforming to B0★, B0a, B1, B4, B7" — no linearity) nor derivable from the model. The foundation's transition framework (AllocatedSet/NoDeallocation, ASN-0034) makes Σ a *set* of partial functions and reachability the reflexive-transitive closure of the induced relation. At any state where more than one operation is defined — e.g. `baptize(p,d)` for several distinct B6-valid `(p,d)` — multiple successors exist, so the reachability relation **branches**. The assertion that the model "admits only linear history" therefore contradicts the very state-space framework this ASN imports.

The consequence is a genuine counterexample to B8 as stated. Take `s_init → s_A` (baptize namespace X) and `s_init → s_B` (baptize namespace Y), then `s_A → s_A'` and `s_B → s_B'` each baptizing a third namespace Z whose registry is empty in both `s_A` and `s_B`. Both acts compute `next = inc(p_Z, d_Z) = c₁` and produce the *same* address. These are distinct baptismal acts (distinct edges), so B8's unconditional "a ≠ b" fails. Case 2 survives (B7 is order-independent), but Case 1 does not.

**Required**: Either (a) add linearity as an explicit model axiom/precondition and justify why the single-server baptism model is sequential (a derivation, not an assertion — the current sentence claims it as a fact about "this model" with no support), or (b) restrict B8's claim to acts on a common transition path / single execution and state that precondition in the contract. The cross-replica generalization can remain in Open Questions, but the within-model premise B8 actually uses must be discharged here.

## OUT_OF_SCOPE

### Topic 1: Cross-replica / concurrent baptism ordering
**Why out of scope**: The distributed coordination needed to keep same-namespace baptisms collision-free across replicas is correctly deferred (Open Questions, last bullet). Note this is distinct from Issue 1: Issue 1 is about the *single* model's branching, which B8 must handle within this ASN; the multi-replica protocol is future territory.

### Topic 2: Parent-baptized prerequisite (Bop PRE "no parent-baptized prerequisite is imposed")
**Why out of scope**: Whether a parent must be baptized before its children is explicitly tied to the ownership model (Scope list, Open Questions bullet 1). The bare statement that no such precondition is imposed is an appropriate framing note, not a claim requiring proof here.

Minor note (not blocking): the S(p,d) preamble parenthetical "(the strict ordering is proved separately at S0 below)" is a stray forward pointer that adds nothing — the table and S0's own slot already carry this. Drop it. This is the only residual forward-reference noise I found; the note is otherwise clean of the anti-bloat patterns.

VERDICT: REVISE
