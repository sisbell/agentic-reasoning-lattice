# Review of ASN-0030

## REVISE

### Issue 1: Ghost permanence — PrefixOrderingExtension misapplied, conclusion overstated

**ASN-0030, The Ghost Domain**: "A child of t₁ extends t₁'s prefix and is therefore > t₁ but — by PrefixOrderingExtension — < t₃ only if t₁ ≼ t₃, which contradicts t₁ and t₃ being distinct siblings."

**Problem**: PrefixOrderingExtension says the opposite. Given siblings t₁ < t₃ where neither is a prefix of the other, PrefixOrderingExtension guarantees every extension of t₁ is < every extension of t₃. So a child of t₁ is < t₃ *because* t₁ ⋠ t₃ ∧ t₃ ⋠ t₁, not "only if t₁ ≼ t₃." The implication is backwards.

Counterexample to the stated conclusion: t₁ = [1], t₃ = [3] (siblings, zeros = 0). Ghost t₂ = [1, 0, 1] satisfies t₁ < t₂ < t₃ under T1. Child allocation inc([1], 1) produces [1, 0, 1] = t₂ by TA5(d). The ghost is filled by a permitted allocation. This works because [1] ≼ [1, 0, 1] — the ghost is in t₁'s prefix subtree.

The proof's case 1 (same-length ghosts, forward allocation) is correct. Case 2's internal reasoning — "children of t₁ fall within t₁'s subtree, so a ghost NOT in any sibling's subtree cannot be produced" — is also correct. But the conclusion "no future allocation fills a ghost position between existing allocations" drops both restrictions. The correct claim: a ghost t₂ between siblings t₁, t₃ remains permanent when t₂ is at the same level (#t₂ = #t₁) and not in any sibling's prefix subtree. Ghosts within an existing allocation's subtree can be filled by child allocation.

**Required**: (a) Fix the PrefixOrderingExtension direction. (b) Restrict the conclusion to same-level, non-subtree ghosts. (c) Note explicitly that ghosts within an allocation's prefix subtree (different-length addresses in the interval) are fillable.

### Issue 2: A2 partition — fourth case silently excluded

**ASN-0030, The Accessibility Partition**: "exactly one of: (i) active, (ii) unreferenced, (iii) unallocated. These are exhaustive and mutually exclusive."

**Problem**: The three cases cover {allocated ∧ reachable, allocated ∧ ¬reachable, ¬allocated}. The fourth combination — reachable ∧ ¬allocated — is excluded without argument. The step is simple (P2 gives reachable(a) ⟹ a ∈ dom(Σ.I), so ¬allocated ⟹ ¬reachable) but it must be stated. A partition claim requires showing all cases are covered.

**Required**: State that P2 (ReferentiallyComplete) rules out the fourth case: if a is reachable through any document, it is in dom(Σ.I).

### Issue 3: A4 — DELETE has no V-space postcondition

**ASN-0030, DELETE section**: A4 specifies Σ'.I = Σ.I and persistence of removed I-addresses. No V-space postcondition is given.

**Problem**: The reachability analysis says "the I-addresses at positions p through p+k−1 are no longer in range(Σ'.V(d))" and the worked example says "Σ'.V(d) = [a₁, a₃]" — both require DELETE's V-space behavior, which is nowhere formalized. REARRANGE gets A4a (permutation), COPY gets A5 (identity sharing). DELETE gets nothing for V-space. The ASN references "P9-right applied in reverse," but the reverse of an INSERT postcondition is not a DELETE postcondition — it's an analogy, not a derivation. No foundation ASN specifies DELETE's V-space behavior (ASN-0026 classifies it only as `fresh = ∅`).

**Required**: Add a DELETE V-space specification requirement parallel to A4a/A5: precondition (`1 ≤ p`, `p + k − 1 ≤ n_d`, `k ≥ 1`), length (`|Σ'.V(d)| = n_d − k`), left-unchanged (`(A j : 1 ≤ j < p : Σ'.V(d)(j) = Σ.V(d)(j))`), right-shifted (`(A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))`), and cross-document frame (P7). Label it as a specification requirement, consistent with A4a/A5's treatment.

### Issue 4: A5 — COPY target frame conditions absent

**ASN-0030, COPY section**: A5(a) specifies the new positions. A5(b) specifies I-space unchanged. Nothing addresses existing content in d_t.

**Problem**: After COPY, what happens to positions that were already in d_t? Without left-unchanged and right-shifted conditions, we cannot derive that COPY preserves reachability of existing content in the target. The ASN claims "COPY *increases* reachability" and "If d_s later deletes the content, it remains reachable through d_t" — but without a frame on d_t, we cannot prove existing d_t content survives the COPY. Gregory's implementation uses `insertpm` (insert semantics), suggesting left-unchanged + right-shifted + length = n_{d_t} + k, but none of this appears in A5.

**Required**: Extend A5 with: `|Σ'.V(d_t)| = n_{d_t} + k`, left-unchanged frame (positions below p_t), right-shifted frame (positions ≥ p_t shift by k), and cross-document frame.

### Issue 5: Worked example forward-references A4

**ASN-0030, A Worked Example**: "Identity (A4): Σ'.I = Σ.I, so a₂ ∈ dom(Σ'.I) and Σ'.I(a₂) = Σ.I(a₂)."

**Problem**: A4 is introduced in the next section ("Operations and the Two Properties"). At the point of the worked example, only A0–A3 are defined. The result follows from A0 plus +_ext (fresh = ∅ for DELETE), both of which are already available.

**Required**: Reference A0 and +_ext instead of A4, or move A4's definition before the worked example.

## OUT_OF_SCOPE

### Topic 1: MAKELINK operation analysis
The ASN discusses link integrity (A7, A7a, A7b) but does not analyze the MAKELINK operation itself. Since links are not formalized in any foundation ASN, MAKELINK's specification belongs in a future ASN.
**Why out of scope**: Link operations are new territory. The ASN's link analysis correctly depends only on A0 and the structural definition of endsets.

### Topic 2: Historical backtrack mechanism
Transition (ii)→(i) for truly unreferenced addresses is "permitted by the invariants but not achievable by any currently defined operation." The recovery mechanism is noted but unspecified.
**Why out of scope**: Correctly identified as a gap and recorded in open questions. Specifying the mechanism is a distinct specification effort.

### Topic 3: Publication–reachability interaction
The open question "can published content become unreferenced?" identifies an important boundary between D10/D11 (publication semantics) and V-space editing.
**Why out of scope**: Requires interaction between publication permanence and deletion that neither ASN-0029 nor ASN-0030 addresses.

VERDICT: REVISE
