# Review of ASN-0100

I read the full specification, checked every invariant-preservation argument against its cited foundation claims, re-derived the worked examples numerically, and stress-tested the boundary cases (beginning, append, empty document, single insert). I focused hardest on the two areas most likely to hide defects: the freshness/atomicity argument (the most recently revised material) and the I3-disclaiming logic.

## Findings

The specification holds. The points I scrutinized most carefully all check out:

**Freshness discharge (Effect One).** The split of K.α's precondition into `a_k ∉ dom(Σ_k.C)` (via ChainEnumerationInjectivity + ChainMembershipForOrigin + Disjointness, with FirstEmissionFreshness only for the `m_d = 0` boundary) and `a_k ∉ dom(Σ_k.L)` (via subspace separation L0 + SC-NEQ) is correct and non-circular — the link clause of L0 does not depend on the K.α firings, so no circularity arises in establishing intermediate validity.

**The I3 disclaiming.** The decision to cite only I3's positive shift clause and disclaim I3-V/I3-CS/I3-CX is correct: those three describe a strictly-smaller shift-only post-state, and the demonstration that I3-V would force `shift(p,k) ∉ dom(M'(d))` precisely at coinciding Insertion positions (`p_m + k ≤ N`) is a genuine, well-localized argument, not a hand-wave.

**The atomicity/ordering retraction.** The reductio establishing that coupling constraints are per-own-boundary is sound: since K.μ⁺ requires `a_k ∈ dom(C)`, the unplaced-allocation window for C is structurally unavoidable; if the literal set-difference reading applied to foreign boundaries, no decomposition could discharge it, contradicting INSERT's well-definedness. The C/R symmetry argument correctly dissolves the apparent asymmetry, and atomicity (not reordering) is correctly identified as the shield.

**S8★ collapse via INS.chain-shift.** `a_{k+1} = shift(a_k,1)` is properly grounded (T4-validity → `sig = #` → TA5 single-component bump = `shift(·,1)`), not asserted; the M7 merge of the n length-1 Insertion blocks into `(p, a_0, n)` correctly verifies both V- and I-adjacency.

**Worked examples.** I re-computed the interior example end-to-end: K.μ⁻ retention `n'_{s_C} = 2`, the seven post-state mappings, `coverage(e_1) = [a_2, a_5) ∩ ran = {a_2,a_3,a_4}`, `N_S = {[1,5],[1,6]}`, `N_I = ∅`, and `π(P_0) = {[1,2],[1,5],[1,6]}` matching `project(Σ')`. Every number is correct.

**Boundary coverage and wp depth.** Beginning (`j=0`), append (`j=N`, K.μ⁻ omitted), and empty-document first insertion (ternary predicate, caller-chosen `m`) are each handled with distinct, correct composite structures. The wp analysis includes two genuinely non-trivial cases (discoverability collapsing to the pre-state condition for tight endsets; P4★ resolving to a chain-membership predicate).

The cross-substrate tension (ASN-0047 `E_doc` vs ASN-0093 `dom(M)`) is acknowledged up front in the Formal Contract and reconciled via the explicit `E_doc = dom(M)` identification in the P6 derivation — adequate given both are foundation ASNs.

## OUT_OF_SCOPE

### Topic 1: INS.identity.version corollary references version derivation
**Why out of scope**: The corollary uses `d_v = inc(d_src, 1)` as a premise. It does not *define* version-creation mechanics — it states an INSERT identity property when the target happens to be a version — so it legitimately belongs to INSERT. Noted only because version creation is on the excluded list; no action needed, the corollary is correctly scoped to INSERT behavior and explicitly defers the K.δ mechanics.

VERDICT: CONVERGED
