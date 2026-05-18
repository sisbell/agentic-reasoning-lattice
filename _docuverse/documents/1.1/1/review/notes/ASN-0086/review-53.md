# Review of ASN-0086

## REVISE

### Issue 1: R0 Step 4 invariant verifications skip the inductive hypothesis
**ASN-0086, R0 — TupleAddressFreshness, Step 4**: "L11a holds because `a ∉ dom(Σ.L)` (Step 2's freshness) and the class-(iii) Frame asserts a single-key extension with all prior entries preserved."

**Problem**: L11a is a substrate-wide invariant (distinct allocation events produce distinct addresses). The verification only checks that the new `a` is distinct from prior addresses — it never explicitly invokes the inductive hypothesis that L11a held at Σ. The same gap appears for L14 ("L14 at Σ' requires {a} ∩ dom(Σ'.C)|_{s_C} = ∅: ...") and L14a, which both verify only the new addition without stating that existing pieces are preserved by IH.

**Required**: Explicitly state IH + new-element form: "At Σ, L11a holds (IH); by Step 2's freshness, a is distinct from all addresses in dom(Σ.L); therefore L11a holds at Σ'." Same pattern for L14 and L14a.

### Issue 2: R0a-Cor1's induction step compresses the least-i computation
**ASN-0086, R0a-Cor1, Step Sub-case B**: "The least `i ≥ 1` with `incⁱ(b, 0) = incᵏ⁺ⁱ(d_new.0.s_L.1, 0) ∉ dom(Σ.L)` is therefore `i = J_{d_new}^Σ - k + 1`"

**Problem**: The derivation `i = J - k + 1` is given as the answer without showing the calculation. The reader must verify: incᵐ(...) ∈ dom(Σ.L) iff m ≤ J (from IH's exact form), so we need least i ≥ 1 with k + i > J, i.e., i ≥ J - k + 1. The proof depends on k ≤ J (so i ≥ 1 is satisfiable), which is stated but not connected to the computation.

**Required**: Show one line: "incᵏ⁺ⁱ ∉ dom(Σ.L) iff k + i > J; least such i ≥ 1 (well-defined since k ≤ J ⟹ J - k + 1 ≥ 1) is J - k + 1; hence a = incᴶ⁺¹."

### Issue 3: R7a's class-(i) admissibility for d_k underjustified
**ASN-0086, R7a Proof**: "the existence of this class-(i) step is admissible because `d_k ∈ dom(Σ'.M)` (by L1a applied to `a_k` at Σ' in the original ↝-step), so `d_k` is a legitimate document address — class (i) emits at such an address"

**Problem**: Class-(i) is document allocation under ASN-0036/S7d, which has T4-validity and `zeros(d) = 2` requirements. The proof says `d_k` is "legitimate" because it's in `dom(Σ'.M)`, but the chain to that conclusion needs spelling out: Σ' is a valid state (all invariants satisfied), so `d_k ∈ dom(Σ'.M)` was itself placed by a S7d-conforming step somewhere along the original ↝-transition, hence T4-valid with `zeros(d_k) = 2`.

**Required**: One line: "Σ' satisfies S7d, so d_k ∈ dom(Σ'.M) entails T4-valid(d_k) ∧ zeros(d_k) = 2, discharging class-(i)'s preconditions for d_k."

### Issue 4: Sparse-allocator hypothesis is unused by any proof
**ASN-0086, Implementation Notes**: "**Sparse-allocator hypothesis.** ... This is the implementation-side realization of the substrate emission primitive's witness-only reading of L1c stated in Setup: ... R0 consumes only the substrate primitive's witness-only reading and is not itself dependent on this hypothesis."

**Problem**: The hypothesis explicitly says R0 doesn't depend on it. No other claim in the ASN cites it either. Its appearance in the appendix's "discipline-conditional" list is misleading because no listed discipline-conditional claim (R0a, R0a-Cor1, R0a-Cor2, Emit_K's function-ness, Nullify's single-tuple scope) consumes it — each consumes the sibling-frontier discipline instead.

**Required**: Either delete the hypothesis, or rewrite to a single sentence in Setup noting that the witness-only reading of L1c has an implementation-side realization (the udanax-green allocator is sparse) without elevating this to a labeled hypothesis.

### Issue 5: R0a-Cor2 hand-waves the #E-preservation step
**ASN-0086, R0a-Cor2 Proof**: "Each subsequent sibling step `inc(·, 0)` operates within the depth-2 link allocator `A_{d.0.s_L.1}` and, by TA5(c) (chain-prefix-preservation, ASN-0034), preserves every position of `E` other than the rightmost — in particular preserving `#E`."

**Problem**: TA5(c) speaks about preserving positions other than sig(t), not "of E." The argument that #E is preserved requires: TA5(c) preserves all positions except sig(t); for T4-valid input, sig(t) = #t (TA5-SigValid); incrementing the last component value doesn't move it; the zero-count partition is therefore unchanged; #E is determined by the partition, so #E is preserved. The proof skips this chain.

**Required**: State the chain: "TA5(c) modifies only position sig(t); TA5-SigValid gives sig(t) = #t for T4-valid t; the modification preserves zero-count partition, hence #E."

### Issue 6: R6c-Corollary's "joint provenance" wording conflates frame and invariant
**ASN-0086, R6c-Corollary**: "arrangement-modifying transitions hold Σ.L identical by the joint provenance of ASN-0036's P3 (governs Σ.M-only mutability without Σ.L change) and ASN-0043's L12 + L12a (forbid modification or removal from Σ.L across any transition)"

**Problem**: L12 + L12a constrain all transitions but permit Σ.L *extension*. What keeps Σ.L fully fixed across arrangement-modifying transitions is ASN-0036's P3 frame condition (arrangement modifications operate on Σ.M only). L12/L12a do not contribute to this preservation — they only prevent modification/removal of existing entries. The "joint provenance" framing implies they share the work.

**Required**: Rewrite: "arrangement-modifying transitions hold Σ.L identical by ASN-0036's P3 frame condition (arrangements operate on Σ.M only); L12 and L12a are not consumed for this preservation."

### Issue 7: T_admissible's Note has defensive bootstrap-circularity prose
**ASN-0086, Definition — TypeCatalog, Note paragraph**: "This avoids the bootstrap circularity that would arise if `K ∈ T_cat^Σ` were required as a precondition for introducing a genuinely new type via emission."

**Problem**: The substantive content of the Note is that T_admissible is the indexing set, T_cat^Σ is descriptive, and L_K^Σ is well-defined for any K ∈ T_admissible. The "avoids bootstrap circularity" sentence is defensive justification for the design choice rather than a statement of meaning. The flagged anti-bloat patterns include "new prose around an axiom explains why the axiom is needed rather than what it says."

**Required**: Remove the bootstrap-circularity sentence. The preceding sentence ("L_K^Σ is well-defined for any K ∈ T_admissible and is simply empty when...") already establishes the design.

### Issue 8: Definition — TypedRelation has a redundant follow-up sentence
**ASN-0086, Definition — TypedRelation**: "Membership at the type slot is by coverage-equivalence, not by literal endset value: a tuple stored with third endset `K'` belongs to `L_K^Σ` whenever `K' ~ K`, so `L_K^Σ = L_{K'}^Σ` whenever `K ~ K'`."

**Problem**: The defining clause itself contains `coverage(Σ.L(a).e₃) = coverage(K)` — the coverage-equivalence membership is already explicit in the definition. The follow-up sentence restates what the definition already says.

**Required**: Delete the sentence, or fold the `L_K = L_{K'}` consequence into a single line.

### Issue 9: Setup opening paragraph forward-references R0a unnecessarily
**ASN-0086, Setup**: "Alongside the active/audit distinction, this note makes a second structural commitment: the *sibling-frontier emission discipline*, a hypothesis on the substrate primitive under which the supplementary lemma R0a (FlatLinkDomain) establishes `dom(Σ.L)` as a tumbler-prefix antichain — discipline-conditional, not substrate-derivable."

**Problem**: This forward-references R0a and the discipline before either is defined. Readers hit a name (sibling-frontier discipline) and a label (R0a) without context. The Implementation Notes appendix (where the discipline is defined) and R0a itself both restate the discipline-conditionality, so this opening sentence is preview overhead.

**Required**: Delete the sentence, or move the structural-commitments preview to a single bulletted summary at the head of Properties Introduced.

### Issue 10: R7a's replay sequence claim incomplete on dom(Σ.C)
**ASN-0086, R7a Statement**: "there exists a finite sequence `Σ = Σ_0 → Σ_1 → … → Σ_m = Σ_n'` (`m ≥ 1`) of `→`-steps, each of class (i), (ii), or (iii), with `Σ_m.L = Σ'.L` and `dom(Σ_m.M) ⊆ dom(Σ'.M)`."

**Problem**: The replay constructs class-(i) prefixes for new home documents but no class-(ii) steps. The conclusion mentions `dom(Σ_m.M) ⊆ dom(Σ'.M)` but is silent on `dom(Σ_m.C)`. By the construction, `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)` (no class-(ii) steps are added). The reader has to derive this.

**Required**: Add to the conclusion: "and `dom(Σ_m.C) = dom(Σ.C) ⊆ dom(Σ'.C)`," and confirm in the proof that the replay introduces no class-(ii) steps because L1a does not require existing content addresses.

### Issue 11: R6a proof contains exegetical commentary
**ASN-0086, R6a Proof**: "By R2, `b ∈ dom(Σ'.L)` with `Σ'.L(b) = (F', G', R'')` — the literal stored value is preserved exactly, so in particular the from- and to-endsets `F'` and `G'` are preserved; the proof requires only this preservation of `G'`, not any literal equality at the type slot."

**Problem**: The clause "the proof requires only this preservation of G', not any literal equality at the type slot" is exegetical — it tells the reader what the proof needs as opposed to advancing the argument. The preservation of G' is already established by the preceding sentence.

**Required**: Delete the trailing exegetical clause. The next sentence then directly uses the preserved G'.

### Issue 12: Worked Sketch Step 3 adds little
**ASN-0086, Worked Sketch, Step 3**: "Arrangement modification illustrates R6c-Corollary..."

**Problem**: Step 3 constructs an arrangement-modifying transition Σ_2 ↦ Σ_arr and verifies that A_K is preserved pointwise. This restates R6c-Corollary's conclusion without adding a non-trivial computation — every quantity is held by frame. The step exhibits no new structure beyond what R6c-Corollary's two-line statement already gives.

**Required**: Either delete Step 3, or replace with a single sentence in Step 2 noting that the established A_K^{Σ_2} = {(a₂, F₁, G₁)} persists across any subsequent arrangement-modifying step by R6c-Corollary.

## OUT_OF_SCOPE

The Open Questions section already enumerates the substantive topics deferred: concurrency between Emit/Observe, multi-arity link relations, second-order Nullify semantics, dynamic type catalog extension, native scoped L14, and whether to elevate the sibling-frontier discipline to a substrate-level guarantee. These are appropriately framed as future work and do not reflect gaps in the current ASN.

VERDICT: REVISE
