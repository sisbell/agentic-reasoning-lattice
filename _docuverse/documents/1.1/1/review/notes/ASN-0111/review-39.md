# Review of ASN-0111

This ASN is in good shape: the operation is honestly minimal, the totality decision is argued rather than assumed, RL4's two-state witness is constructed in full rather than waved at, and the worked read actually exercises the load-bearing postconditions (including the coverage-is-a-subtree subtlety that a careless example would have gotten wrong). Two precision defects remain, both fixable in place.

## REVISE

### Issue 1: Evaluability of the structural screen rests on an undischarged step
**ASN-0111, "Deriving the read" (structural screen paragraph)**: "It also guards the well-definedness of what follows: `subspace_I(·)` and the element-field projection `E(·)` are defined only on T4-valid tumblers (T4b, ASN-0034; SubspaceI, ASN-0043), so under the left-to-right reading the screen is evaluable on all of `T`..."

**Problem**: The cited domain condition for `subspace_I` (SubspaceI, ASN-0043) is `T4-valid(a) ∧ zeros(a) = 3 ∧ #E(a) ≥ 1` — T4-validity is necessary but not sufficient, yet the prose credits the *leading conjunct alone* with guarding what follows ("defined only on T4-valid tumblers" is a necessary-condition statement doing duty for a sufficiency claim). At the point where the third conjunct `subspace_I(a) = s_L` is evaluated, the first two conjuncts have supplied T4-validity and `zeros(a) = 3`, but `#E(a) ≥ 1` — required for `E(a)₁` to exist — is nowhere discharged. It does follow: T4-validity includes the field-segment constraint, T4a converts that constraint into "every field segment is non-empty," and with `zeros(a) = 3` the element field is present (T4c) and hence non-empty. But that inference is exactly the load-bearing step behind "the screen is evaluable on all of `T`," and this corpus's convention (see the per-step T0 discharges throughout ASN-0034) is that such steps are cited, not absorbed into a necessary-condition gloss.

**Required**: Attribute the guard to conjuncts 1–2 jointly, and discharge `#E(a) ≥ 1` explicitly: T4-valid(a) ∧ zeros(a) = 3 ⟹ the element field exists and is non-empty, by T4a's field-segment equivalence (with T4b/T4c fixing that the fourth field is the element field). One sentence suffices.

### Issue 2: "Only success-branch results are permanent" contradicts RL0's own screen-necessity claim
**ASN-0111, RL5, failure-branch paragraph**: "Only success-branch results are permanent; a caller must not cache `⊥`."

**Problem**: This is false as stated, and the ASN itself supplies the counterexample. RL0 establishes that every screen conjunct is *necessary* for membership in `dom(Σ.L)` — and the underlying invariants (L0b, L1, L0, L1b) hold at every reachable state, so an address that fails the screen satisfies `a ∉ dom(Σ'.L)` at *every* reachable `Σ'`, making `readlink(a, Σ') = ⊥` permanent. Indeed RL0 advertises exactly this use ("a failed screen guarantees `⊥` without an invocation"), so a caller who has evaluated the screen and seen it fail may cache `⊥` forever. The genuine instability is confined to screen-passing addresses (the parenthetical's frontier candidates), and the blanket "only success-branch results are permanent" / "must not cache `⊥`" overstates, putting RL5 in internal tension with RL0.

**Required**: Qualify the claim. For example: success-branch results are always permanent (RL5); `⊥` carries no stability guarantee *in general* — for a screen-passing address, a subsequent K.λ at the appropriate chain frontier can allocate `a` — but `⊥` at a screen-failing address is permanent, by the necessity of each screen conjunct at every reachable state. The caching advice should distinguish the two cases accordingly.

## OUT_OF_SCOPE

### Topic 1: Exact characterization of when `⊥` is permanent for screen-passing addresses
**Why out of scope**: Issue 2's fix only needs the two-case qualification. The full characterization — `⊥` at `a` is permanent iff `a` can never become a consumable position on any document's link sub-allocator chain in any future trace — is a reachability result over the transition system (interacting with ChainMembershipForOrigin's contiguous-prefix structure and document creation), and belongs in a future ASN, not in this read specification.

### Topic 2: Distinguishing "recorded-empty endset" from "unwitnessed endset" at resolution time
**Why out of scope**: Correctly identified by the ASN itself as a FOLLOWLINK obligation (second open question); the read-level behavior here is complete.

VERDICT: REVISE
