# Review of ASN-0069

## REVISE

### Issue 1: V8b monotonicity is incorrect — counterexample via K.μ⁻ + K.μ⁺ round-trip

**ASN-0069, V8b**: "The set Π_g is monotonically non-increasing in g: for any subsequent state Σ_h reached from Σ_g by a further sequence of valid composite transitions, Π_h ⊆ Π_g."

**Problem**: Π can grow between consecutive states. Scenario: at Σ', both d_src and d_new have v = [s_C, n_max] ↦ a (so v ∈ F). At Σ_g, K.μ⁻ on d_src retains n'_{s_C} = n_max − 1, removing v from d_src's arrangement. Now v ∉ Corr_g (condition (a) fails: d_src doesn't have v), so v ∉ Π_g. At Σ_h, K.μ⁺ on d_src extends with v ↦ a — admissible because a ∈ dom(C) by P0, D-CTG★ is preserved (re-adding the suffix), and J1★ is satisfied (since (a, d_src) already in R by P2 from the original arrangement). Both sides now have v ↦ a, so v ∈ Corr_h. Since v ∈ F, v ∈ Π_h. Therefore Π_h ⊋ Π_g, contradicting the claimed inclusion.

**Required**: Either restrict V8b to scenarios excluding restoration (e.g., "in the absence of further K.μ⁺ on either side") and weaken the claim accordingly, or replace monotonicity with a different invariant the operation actually guarantees (e.g., Π_g ⊆ F at all times, which is trivially true by definition).

### Issue 2: V8b's proof cites P3 for a property P3 does not provide

**ASN-0069, V8b derivation**: "In the first case, P3 (ArrangementMutabilityOnly, ASN-0047) across Σ_g →* Σ_h does not restore a removed V-position to either arrangement"

**Problem**: P3 of ASN-0047 conjoins P0 ∧ P1 ∧ P2 ∧ L12 — monotonicity for C, E, R, L. P3 says nothing about M; M is explicitly the "only component that can lose information." So P3 cannot exclude K.μ⁺ from re-adding removed V-positions. The subsequent argument "K.μ⁺ could re-add v to one side, but per V5a only one side can be modified per transition" doesn't help either: sequencing across multiple transitions can re-add v on both sides (or re-add on one side while the other never lost it). The second case appeal — "K.μ~ on either side cannot restore equality (it only re-permutes existing images)" — also fails, because permutation changes which I-address sits at v, and a permutation can restore the fork-time pairing at v.

**Required**: Drop the P3 citation; either supply a correct argument for whatever weakened monotonicity claim survives, or excise V8b entirely.

### Issue 3: V11 inductive step relies on inclusion not justified by V4

**ASN-0069, V11 derivation, inductive step**: "V4 applied at each prior step propagates V_{s_C}(d_src) forward into each V_{s_C}(dⁱ_new), justifying the inclusion V_{s_C}(d_src) ⊆ V_{s_C}(d^{k-1}_new) that the hypothesis names."

**Problem**: V4 at step i gives V_{s_C}(d_src) ⊆ V_{s_C}(dⁱ_new) *immediately after* fork i. Between fork i and fork i+1, K.μ⁻ on dⁱ_new can remove inherited positions, and K.μ~ on dⁱ_new can rebind values. The IH as written ("v ∈ dom(M^{k-1}(d^{k-1}_new))") is the conditional surviving such operations, not an unconditional consequence of V4-at-prior-steps. The parenthetical assumes propagation but does not establish it; the chain definition doesn't forbid intermediate non-fork operations.

**Required**: Either (a) restrict V11 to chains with no intermediate non-fork transitions between consecutive forks, making V_{s_C}(d_src) ⊆ V_{s_C}(dⁱ_new) follow from frame composition; or (b) rewrite the IH and proof in terms of "v propagated through the chain" as a primitive, deriving the chain-survival condition cleanly rather than assuming it.

### Issue 4: V2 derivation uses unintroduced notation

**ASN-0069, V2 derivation, inductive step**: "From the base case `#d¹ = #d_src + 1` combined with TA5(c)..."

**Problem**: `d¹` is never introduced. The base case proves the length identity for `d_new` (the first fork). The inductive step's `d¹` presumably refers to this same first-fork output, but the symbol switch is jarring and the antecedent is ambiguous in a proof that already uses `d_new`, `d_prev`, and `d_src` for distinct roles.

**Required**: Either introduce `d¹` explicitly (e.g., "let `d¹` denote the first-fork output `inc(d_src, 1)`"), or use `d_new` of the first fork consistently with the base case.

### Issue 5: V4b's derivation appeals to J4 for a domain restriction J4 does not provide

**ASN-0069, V4b derivation**: "K.δ initialises M'(d_new) = ∅ ... K.μ⁺ adds exactly the positions of V_{s_C}(d_src) per J4's clause (ii)"

**Problem**: J4 clause (ii) of ASN-0047 constrains only the *range*: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`. It does not say K.μ⁺ adds *exactly* V_{s_C}(d_src) to the domain. The "exactly" comes from V0's specification (the ASN's design commitment), not from J4. The derivation as written is circular: V4b is derived from V0's effects, but the citation pretends to extract it from J4.

**Required**: Cite V0 (or V4) as the source of literal domain inheritance rather than J4. Be explicit that V4b strengthens the foundation in the same way V4 does.

### Issue 6: V0's first-fork freshness verification chain has a redundant step

**ASN-0069, "Composite validity verification", K.δ sub-case A**: "*T10a's at-most-once-per-(t, k') child-spawning constraint* ... combined with sub-case A's predicate that A_v(d_src) has emitted no prior version (so no prior K.δ event has fired with operand `t = d_src` and parameter `k = 1`), forces that `inc(d_src, 1)` has not been previously placed into E by any spawning of A_v(d_src)."

**Problem**: The phrase "by any spawning of A_v(d_src)" is muddled — A_v(d_src) is itself a sub-allocator whose first emission is inc(d_src, 1). What "no prior K.δ event with `t = d_src` and `k = 1`" actually rules out is the *parent allocator's* prior spawning of inc(d_src, 1); A_v(d_src) doesn't "spawn" inc(d_src, 1) — that emission *is* A_v(d_src)'s base address, emitted under K.δ with `t = d_src`. The conflation of "spawning event from d_src" with "emission by A_v(d_src)" obscures which T10a constraint is doing the work.

**Required**: Clarify which K.δ event is bounded by the at-most-once constraint (the parent's emission of A_v(d_src)'s base) versus which is bounded by enumeration injectivity (subsequent emissions inside A_v(d_src)'s sibling stream).

## OUT_OF_SCOPE

### Topic 1: Concurrent fork while source is being edited

**Why out of scope**: Beyond SequentialTransitionAxiom (which the ASN correctly invokes), concurrency semantics are a transition-model concern. Listed in Open Questions.

### Topic 2: Snapshot vs. living-fork distinction

**Why out of scope**: This is a design alternative not chosen by this ASN; would belong in a separate ASN positing a different inheritance discipline.

### Topic 3: Fork of a transcludent source

**Why out of scope**: Transclusion mechanics require their own operation specification; the fork operation on any d_src ∈ E_doc is well-defined regardless.

VERDICT: REVISE
