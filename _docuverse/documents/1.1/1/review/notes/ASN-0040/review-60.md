# Review of ASN-0040

## REVISE

### Issue 1: Stray/incorrect citation "(by B4)" in the B1 proof
**ASN-0040, B1 proof, target namespace sub-case**: "By the inductive hypothesis, children(B, p₀, d₀) = {c₁, ..., cₘ} for some m ≥ 0 (by B4)."
**Problem**: The contiguous-prefix form `{c₁, ..., cₘ}` is supplied by the inductive hypothesis (B1 at state B), which the same sentence already names. B4 (Atomic Baptism) says nothing about prefix shape — it fixes that the read is against a single state. Attaching "(by B4)" to the prefix-form claim is a misattribution (the reviser-drift pattern: a citation relocated to where it no longer applies). A precise reader has to stop and reconcile two incompatible justifications for one claim.
**Required**: Delete "(by B4)". If atomicity is genuinely load-bearing here, state separately what B4 discharges; do not staple it to the inductive-hypothesis step.

### Issue 2: B6 necessity of condition (i) conflates T4-preservation with namespace disjointness, and the d=1 branch depends forward on B7
**ASN-0040, B6 intro and necessity sub-case (b), d=1**: "Conditions (ii) and (iii) are necessary and sufficient for T4 preservation… Condition (i) is necessary by two distinct mechanisms — defect propagation and namespace collapse." … "Excluding trailing-zero parents at d = 1 is precisely what prevents one namespace from duplicating another."
**Problem**: Sub-case (b) d=1 *admits* that the stream of a trailing-zero parent is fully T4-valid ([1,0,1], [1,0,2], … all satisfy T4). So condition (i) is **not** necessary for T4 preservation in this case — it is needed only for namespace disjointness. That necessity argument then leans on B7 (Namespace Disjointness), which is proved later and whose statement is *itself gated on B6-validity*. Using "if we dropped (i), (p,1) would duplicate the B6-valid namespace (p′,2)" is design motivation that presupposes the very validity boundary B6 defines — it reads as circular rationale rather than a self-contained necessity proof. The headline ("necessary and sufficient for T4 preservation") and the d=1 argument pull in opposite directions.
**Required**: Either (a) drop the d=1 namespace-collapse argument — condition (i) is already established as necessary *for T4* by sub-case (a) and sub-case (b) d=2, which is all the sufficiency direction needs — or (b) cleanly relabel the d=1 paragraph as a disjointness *motivation* (not a T4-necessity step) and remove the forward dependence on B7 from a necessity proof. Do not let one proof carry two different "necessity" senses under one banner.

### Issue 3: Triplicated induction scaffolding across B1, B_fin, B10 (anti-bloat)
**ASN-0040, proofs of B1, B_fin, B10**: each opens "By induction on the number of state transitions… By B0a (Baptismal Closure), Σ partitions into s.B-frame operations and baptismal operations… *s.B-frame transitions.* … s'.B = s.B = B' … by the inductive hypothesis."
**Problem**: The frame-transition paragraph is reproduced near-verbatim three times, and the B0a case-split boilerplate four times (counting B8's reliance). This is exactly the flagged "two paragraphs say the same thing in different words" pattern, here as literal repetition. The precise reader skips identical text three times to reach the one part of each proof that differs (finiteness vs. T4 vs. contiguity of the new element).
**Required**: Factor the shared step into one stated lemma — "every transition either leaves s.B unchanged (s.B-frame) or adds exactly one element next(s.B,p,d) (baptismal)" — and have B1, B_fin, B10 each cite it and present only the per-invariant argument on the added element.

### Issue 4: B9 trace re-argues the general unbounded claim instead of exhibiting the M=5 instance
**ASN-0040, "B9 unbounded extent exhibited"**: "The construction depends on no upper bound at position 3 of the stream: TA5(c) advances the ordinal value from 2 to 3 to 4 to 5 without consulting any ceiling, and the same step can be repeated indefinitely to grow the namespace through every natural number, each successor remaining in ℕ by NAT-closure."
**Problem**: This duplicates the B9 proof's own "No ceiling is consulted… the construction may be iterated through every natural number" passage. A worked trace should *instantiate* the proof (here, M=5 in three baptisms), not re-prove the general theorem. The closing paragraph restates the unboundedness derivation a second time — meta-prose the reader must recognize as redundant.
**Required**: Trim the trace's closing to the concrete claim it earns ("three baptisms take hwm from 2 to 5; for M′>5, M′−5 more along the same pattern"). Leave the general no-ceiling argument to B9's proof, where it already lives.

## OUT_OF_SCOPE

### Topic 1: Cross-branch (non-co-reachable) address uniqueness
B8 explicitly scopes Global Uniqueness to acts on a single transition path and notes that two baptisms on incomparable reachability branches may compute the same address. Whether branch-merge/replica reconciliation preserves uniqueness is genuinely new territory (it needs a model of branch composition), not a defect in this ASN — and it overlaps the listed out-of-scope item on cross-replica ordering. The single-path result stands on its own.

### Topic 2: Parent-prerequisite for baptism
Whether `p ∈ s.B` must hold before baptizing under p is correctly deferred (Open Questions, and depends on the ownership model). The arithmetic proofs here do not require it, so its absence is not a gap in ASN-0040.

VERDICT: REVISE
