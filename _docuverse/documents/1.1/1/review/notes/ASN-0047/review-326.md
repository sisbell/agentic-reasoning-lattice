# Review of ASN-0047

I focused on the proof obligations, boundary cases, and — given the `review-mode.anti-bloat` classifier — accreted/unused prose. The ASN is mature and internally consistent on the cases it exercises; the findings below are a missing concrete verification of a load-bearing novel postcondition and one unused accreted property.

## REVISE

### Issue 1: J4's multiplicity-preservation postcondition is never exercised on a duplicate-I-address source
**ASN-0047, Coupling and isolation, J4 step (ii)**: "φ is injective, so two distinct source V-positions carrying the *same* I-address — as S5 (UnrestrictedSharing) permits, e.g. `M(d_op)([s_C,1]) = M(d_op)([s_C,2]) = a` — map to two distinct target V-positions, each retaining that I-address; no duplicate is collapsed and the document's content count is preserved."

**Problem**: This is the load-bearing distinction the ASN itself draws between the φ-copy characterization and mere range equality ("Range equality is now a *derived consequence*, not the characterization"). Yet all three fork worked examples (`d₁ → d₂`, `d₂ → d₃`, and the link example) use sources whose content V-positions carry **pairwise-distinct** I-addresses (`a₁ ≠ a₂ ≠ a₃`). The novel claim — that K.μ⁺ realizing φ produces a *non-injective* `M'(d_new)` (two target positions mapping to one I-address, which S2 permits but does not require) and that this is what separates a faithful version copy from a deduplicating range copy — is asserted but never checked against a concrete duplicate-source scenario. By the ASN's own depth standard ("verify its key postconditions against at least one specific scenario"), the single most distinctive J4 postcondition lacks a worked example.

**Required**: Add a fork trace with a transcluded duplicate at the source (e.g. `M(d_op) = {[s_C,1] ↦ a, [s_C,2] ↦ a}`), verifying that φ produces `M'(d_new) = {[s_C,1] ↦ a, [s_C,2] ↦ a}` (two positions, one address, count preserved) and that S2 holds despite non-injectivity — distinguishing it from the wrong outcome `{[s_C,1] ↦ a}`.

### Issue 2: K.λ's forward-allocation conjunct (T9) is stated but consumed by nothing
**ASN-0047, Link allocation, K.λ**: "In addition, the forward-allocation conjunct `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` (T9) holds: it is a consequence of `inc(·, 0)` on the frontier in the subsequent case, and is vacuous in the first-link case."

**Problem**: No downstream invariant, lemma, or proof in the ASN uses link-address forward ordering. Link-subspace sequentiality is carried by D-SEQ★ (contiguity + minimum), link distinctness by L11a, link injectivity by CL-UNIQ — none of which reference `ℓ' < ℓ`. The conjunct reads as a property asserted for parallelism with the content side rather than to advance any claim. Under the anti-bloat classifier this is accreted prose: a stated-but-unused guarantee at a definition site.

**Required**: Either remove the conjunct, or name the specific invariant/proof step it discharges. If it is intended only as documentation, it should not be presented as a verified additional precondition obligation of K.λ.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement withdrawal under renumbering
**Why out of scope**: K.μ⁻ models only suffix removal; interior withdrawal with V-position compaction (the implementation's `DELETEVSPAN`) is genuinely new contraction-operation territory, already correctly logged in the ASN's Open Questions. Not an error in this ASN.

### Topic 2: One-sided / type-only links (`e₁` or `e₂` empty)
**Why out of scope**: Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` is a future endset-semantics refinement; L3's `e₃ ≠ ∅` is the only mandatory-slot constraint here, and the question is already surfaced as an Open Question.

VERDICT: REVISE
