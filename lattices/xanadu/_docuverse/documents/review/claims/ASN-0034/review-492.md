# Regional Review — ASN-0034/Divergence (cycle 4)

*2026-04-24 05:52*

Reading the ASN as a system, checking claim boundaries, precondition chains, and the post-cycle-3 prose state.

### Divergence's NAT-order Depends cites a "uniqueness argument" not carried in the prose
**Class**: REVISE
**Foundation**: (internal)
**ASN**: Divergence, *Formal Contract → Depends → NAT-order*: "trichotomy at length pair `(#a, #b)` splits case (ii) into sub-cases (ii-a)/(ii-b); **trichotomy at candidate pair `(k, k')` discharges case (i)'s uniqueness argument**."
**Issue**: The Depends line claims a use site — trichotomy applied to two candidate values `k, k'` for the divergence index — that does not appear in the Definition or its surrounding prose. Case (i) of the Definition reads "is the least `k` satisfying [conjunction]"; once "least" is the designating quantifier, uniqueness is built into the description (least element of a set is unique by NAT-order's strict-total-order properties at the level of NAT-wellorder, which Depends already cites separately for existence). The parenthetical "equivalently, the unique `k` satisfying ... the universal conjunct restating minimality" asserts uniqueness but does not walk an argument over `(k, k')`. The Depends citation reads like the residue of an earlier draft where uniqueness was argued explicitly via candidate comparison, and now references walking that no longer exists.
**What needs resolving**: Either reinstate the uniqueness walk in the prose (showing why two candidates `k, k'` collapse via the minimality conjunct) and let the Depends citation point at it, or trim the Depends citation to the use that *is* present — trichotomy at length pair `(#a, #b)` in case (ii) — and drop the candidate-pair clause.

### NAT-cancel still frames summand absorption with axiom-bookkeeping prose
**Class**: REVISE
**Foundation**: (internal)
**ASN**: NAT-cancel, opening sentence of the absorption discussion: "Summand absorption is recorded as a consequence rather than an axiom because both its posited form `m + n = m ⟹ n = 0` and its mirror form `n + m = m ⟹ n = 0` are derivable from the two cancellation axioms together with NAT-closure's two-sided additive identity."
**Issue**: The prior cycle removed the "recording either form as an axiom would make the set non-minimal" line; the surviving sentence is the same pattern in compressed form — it justifies the axiom/consequence slot choice rather than presenting the claim. The derivation walk that follows is substantive and stands on its own; it does not need the "is recorded as a consequence rather than an axiom because" preamble. The reader does not need to be told why summand absorption sits in the Consequence slot — that is a structural choice, not a claim. Compounding the issue: the lead paragraph at the top of the axiom already states "A sum equals one of its summands only when the other summand is zero — a consequence of cancellation together with NAT-closure's two-sided additive identity." So the "is recorded as a consequence because derivable" sentence repeats material already present and adds the bookkeeping framing on top.
**What needs resolving**: Drop the "is recorded as a consequence rather than an axiom because" framing. Open the derivation with the substance — e.g., "Summand absorption follows from cancellation and NAT-closure's two-sided identity. From the hypothesis ..." — letting the walk carry the weight without prefatory justification of the slot choice.

VERDICT: REVISE
