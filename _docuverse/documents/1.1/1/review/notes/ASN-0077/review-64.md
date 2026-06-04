# Review of ASN-0077

## REVISE

### Issue 1: O5★ derivation buries the proof in apparatus-justifying meta-prose
**ASN-0077, Claim O5★ derivation**: "The disjunctive hypothesis `a ∈ dom(Σ.C) ∪ dom(Σ.L)` is not itself in the schema's clause grammar — the Closure schema (★) ... admits membership-persistence clauses only in the per-store form ... The value-preservation half is likewise constrained ... An unconditional clause `[origin'(a) = origin(a)]` therefore lies outside the schema's per-clause grammar."
**Problem**: Three sentences explain *why* the disjunctive clause cannot enter the schema before any work is done. This is the "new prose explaining why the apparatus is needed rather than what it says" pattern. The load-bearing content is only: split into store-conditioned clauses `c₁, c₂, c₃_C, c₃_L`; O5 discharges each single-step; the schema lifts the conjunction; case-split the hypothesis. The grammar exegesis is defensive padding around that.
**Required**: Compress to the split itself. State that `origin` is well-defined on each store, pair each value-preservation clause with its membership clause, cite O5 for the single-step, the schema for the lift, and case-split. Drop the grammar-eligibility narration.

### Issue 2: Worked example presents the O14 witness as an abandoned chronology branch
**ASN-0077, A worked example**: "*Alternative transition Σ₁ → Σ₁' (arrangement reordering ...)*. Consider an alternative path from Σ₁ in which `d₃` reorders rather than contracts. ... Returning to the main chronology, we proceed instead with the contraction below."
**Problem**: The K.μ~ witness is load-bearing (it is O14's concrete example), but framing it as a branch of the narrative that is then explicitly retracted is navigation noise. The reader must follow a fork-and-return that adds no reasoning — both O13 and O14 are just probes evaluated at/after Σ₁.
**Required**: Present the O13 (K.μ⁻) and O14 (K.μ~) witnesses as two parallel probes from Σ₁ without the "alternative path"/"main chronology"/"returning" framing. Keep the witnesses; drop the branch-and-retract scaffolding.

### Issue 3: O11★★ does not preserve SHOWORIGIN_V precondition (i) at non-`M(d)` steps
**ASN-0077, Claim O11★★ derivation**: "Well-formedness of σ at `Σ_{n-1}` is preserved by induction ... using Corollary O11.1 at each `M(d)`-modifying step ... and the state-independence of σ's structural conjuncts at each non-`M(d)`-modifying step (where the range condition and common depth are inherited unchanged because `M(d)` is unchanged)."
**Problem**: For non-`M(d)`-modifying steps the argument covers precondition (vi) and the common depth (via "`M(d)` unchanged") and (iii) by the same token, but precondition (i) `d ∈ Σ.E_doc` is neither structural nor a function of `M(d)`. Its preservation across an arbitrary intervening transition is not discharged here; it requires P1 (EntityPermanence). The conjunct is skipped.
**Required**: Add the one-clause citation: precondition (i) is preserved at every step by P1 (already invoked inside Corollary O11.1 for the extension steps), so well-formedness carries through non-`M(d)` steps in full, not only its structural and arrangement-tracked conjuncts.

## OUT_OF_SCOPE

### Topic 1: Reporting link-address origins for a cross-subspace I-span
**Why out of scope**: The first Open Question (cross-subspace span guarantees) and the I-span lift's deliberate restriction to `dom(C)` define a future operation that surfaces link origins as well. The ASN's edge-case note correctly states current behavior (link addresses dropped); enriching the guarantee belongs to a future ASN, not a revision here.

VERDICT: REVISE
