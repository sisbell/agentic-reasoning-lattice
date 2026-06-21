Reading the full cone — foundation statements plus ASN-0053 (S3, WR, S3a, S4, S6, WF, S3b) — looking for what lives between claims.

**WF** establishes the reach-identity and well-formedness facts that almost every other claim borrows. Its proof is tight and its depends list (T12, D1, T1, Divergence, TumblerSub) is complete. The T1 case (ii) exclusion via #s = #r, followed by Divergence's uniqueness identifying the T1 witness with the divergence index, is correctly executed and cited.

**S3 and S6** read cleanly. S3's WLOG reduction to reach(α) ≥ start(β), the two-case union argument, and the WF invocation all check out. S6 is a definition and its inline consequence (#reach = #s via TA0's result-length identity) follows directly from level-uniformity.

**S3a** establishes commutativity of disjunction → commutativity of set union. The set-level proof is sound.

Three correctness gaps follow.

---

### WR — T1 and Divergence absent from depends while proof uses both

**Class**: REVISE
**Foundation**: D2 (DisplacementUnique)
**ASN**: WR (WidthRecovery) — "divergence(s, reach(σ)) = k ≤ #s, the D2 precondition on divergence (established as in WF's proof: #s = #reach(σ) excludes the prefix case, so the divergence is of type (i))"
**Issue**: The inline argument discharging D2's precondition `divergence(s, reach(σ)) ≤ #s` has two steps that each require a foundation dependency absent from WR's list. First, excluding T1 case (ii): `#s = #reach(σ)` forces `k = #s + 1 ≤ #reach(σ) = #s`, contradicting NAT-addcompat — this case analysis is T1's definition. Second, the identification "T1 witness k = divergence(s, reach(σ))": k qualifies for Divergence's case (i) and is minimal because sᵢ = reach(σ)ᵢ for i < k eliminates all smaller candidates — this uniqueness clause belongs to Divergence. Neither T1 nor Divergence appears in WR's *Depends* list, which names only D2, T12, TA-strict, and TA0.
**What needs resolving**: T1 (LexicographicOrder, ASN-0034) and Divergence (Divergence, ASN-0034) must be added to WR's *Depends*, with their roles in the divergence-type argument made explicit — specifically T1's case (i)/(ii) definition and case (ii) exclusion, and Divergence's case (i) uniqueness clause identifying the T1 witness with the divergence index.

---

### S4 — D1 cited for reach(λ) = p but creates undeclared T1 and Divergence dependencies; WF already delivers the same result

**Class**: REVISE
**Foundation**: WF (WellFormedSpanFromEndpoints), D1 (DisplacementRoundTrip, ASN-0034)
**ASN**: S4 (SplitPartition), part (c) — "the divergence is of type (i) with divergence(s, p) ≤ #s — equal length excludes the prefix case — so D1's preconditions … are met and D1 gives s ⊕ (p ⊖ s) = p. So reach(λ) = s ⊕ d = p"
**Issue**: WF's postcondition — already invoked earlier in S4's proof to construct λ — states `reach(γ) = s ⊕ (r ⊖ s) = r`. Applied to γ = λ = (s, p ⊖ s) with r = p, this directly gives `reach(λ) = p`, with no further argument required. The proof nevertheless reinvokes D1 to re-derive the same identity. That redundant invocation forces an inline divergence-precondition discharge (`divergence(s, p) ≤ #s` via the equal-length/case (ii) exclusion argument), which uses T1 and Divergence in exactly the same pattern flagged in WR above — neither of which is in S4's *Depends*. The depends list therefore misrepresents what the proof as written actually uses: D1 is cited for a result WF already supplies, while T1 and Divergence are used without citation.
**What needs resolving**: Either (a) the part (c) argument is restructured to read `reach(λ) = p` directly from WF's postcondition, making D1 and its sub-argument unnecessary and allowing D1 to be removed from the depends; or (b) D1 is retained and T1 (LexicographicOrder, ASN-0034) and Divergence (Divergence, ASN-0034) are added to S4's *Depends* with their roles in discharging D1's divergence precondition made explicit. The current state — D1 cited, T1 and Divergence silently used — cannot be used by a downstream verifier.

---

### S3b Case B — S3a cited for span equality but S3a's postcondition establishes only set equality

**Class**: REVISE
**Foundation**: S3 (MergeEquivalence), S3a (MergeCommutativity)
**ASN**: S3b (MergeSplitInverse), Case B — "By S3a (merge commutativity) the merge of α and β equals the merge of β and α, which is the Case A configuration with the roles of α and β exchanged."
**Issue**: S3a's postcondition is `⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧` — point-set equality. S3a's proof derives this from commutativity of disjunction; it says nothing about the pair `(start(γ), width(γ))`. S3b Case B uses the citation to assert that `merge(α, β)` and `merge(β, α)` are the same *span*, then applies S4 to that span. S4 takes a span (a pair) as input, not a set. The step from S3a's set-equality conclusion to the needed span-equality conclusion is a gap: S3a's proof does not establish it. The span equality is in fact true — S3's endpoint formula uses min(start(α), start(β)) and max(reach(α), reach(β)), both symmetric — but this follows from S3's formula, not from S3a. Additionally, S3a's own opening prose ("the merge of α and β yields the same span as the merge of β and α") overstates S3a's formal postcondition, and S3b is exploiting that overstatement. The correct argument for Case B needs no commutativity lemma at all: in Case B, `start(γ) = start(β)` and `reach(γ) = reach(α)` (directly from S3's formula, since `start(β) < start(α) = reach(β) < reach(α)`), and S4 splits γ at `p = start(α)` giving left part `(start(β), start(α) ⊖ start(β))` and right part `(start(α), reach(α) ⊖ start(α))`; WR then identifies these as β and α respectively.
**What needs resolving**: Either (a) S3a's postcondition is strengthened to assert span equality `merge(α, β) = merge(β, α)` and S3a's proof is extended to establish it (requiring S3's formula symmetry or an injectivity argument for level-uniform span denotations); or (b) S3b Case B is restructured to derive the split directly from S3's formula and WR, without routing through S3a. In either case, S3a's prose and postcondition must be made consistent with each other.

---

VERDICT: REVISE