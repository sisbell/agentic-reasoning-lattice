# Review of ASN-0086

## REVISE

### Issue 1: "Enumeration index" terminology in R0 Step 2 Case A conflates two distinct concepts
**ASN-0086, R0 Step 2 Case A**: "advancing from `A_{d.0.1}`'s base `d.0.1` (its first emission, enumeration index 1 at zero-count depth 1) to `d.0.s_L` (enumeration index `s_L` at the same depth)"

**Problem**: T10a.7 (EnumerationInjectivity) defines an allocator's domain as `{tₙ : n ≥ 0}`, so the base address is at enumeration index 0, not 1. The author appears to be using "enumeration index N" to mean "the last-component digit value N" — `d.0.1`'s last digit is 1, `d.0.s_L`'s last digit is `s_L`. A reader cross-referencing T10a.7 will read "enumeration index 1" as `t_1` (the *second* emission), which is wrong. The sweep applies `s_L − 1` times (correctly stated), but the index notation contradicts the step count under T10a.7's convention.

**Required**: Replace "enumeration index N" with "last-component value N" or "sibling sweep digit N" throughout this passage, and reserve "enumeration index" for T10a.7's index-from-zero. Alternatively, add a one-line note: "Here 'enumeration index' denotes the last-component value of A_{d.0.1}'s output, not T10a.7's domain index."

### Issue 2: R0a-Cor1's induction quantifier scope should be →_D, not →
**ASN-0086, R0a-Cor1 proof**: "By induction on the `→`-chain length, parallel to R0a's induction."

**Problem**: R0a is explicitly restricted to states reachable via `→_D*` (the discipline-respecting reachability — "every class-(iii) `→`-transition along the reachability chain is `→_D`-admissible"). R0a-Cor1's "Under R0a's hypothesis" qualifier means the quantifier should also be `→_D*`-reachable states, not `→*`-reachable states. Saying "→-chain length" suggests R0a-Cor1 might hold over arbitrary →-chains, but the Sub-case B argument explicitly invokes R0a's invariant — which only holds under the discipline. The formal statement of R0a-Cor1 should also use `Σ_0 →_D* Σ`, matching R0a.

**Required**: Replace "By induction on the →-chain length" with "By induction on the →_D-chain length (the discipline-restricted reachability inherited from R0a's hypothesis)"; update R0a-Cor1's formal statement to use `Σ_0 →_D* Σ`.

### Issue 3: SharedDepthOneAllocator is an unnumbered lemma with downstream citations
**ASN-0086, Setup section, "Lemma — SharedDepthOneAllocator"**: substantive lemma with a three-step proof, cited by R0 Step 2 Case A's L1c chain construction, R0a-Cor2's depth argument, and the worked sketch's allocator scaffolding.

**Problem**: The lemma is unnumbered while every other proven result has an R-number. The Properties Introduced table gives it a row labeled "LEMMA" but no number, creating two citation styles within the ASN (numbered R-claims vs. named lemmas). Cross-references like "the *SharedDepthOneAllocator* lemma in Setup" are harder to locate via the index than R-numbered citations would be. The lemma is load-bearing — R0 Step 2 Case A depends on the shared-allocator structure for the sibling sweep through `A_{d.0.1}` from position 1 to position `s_L`.

**Required**: Either (a) assign a number (e.g., R0-Pre, or fold into R0's preconditions as a numbered sub-claim), or (b) explicitly document the citation convention for named (unnumbered) lemmas, and ensure downstream citations are uniform. The Properties Introduced table's row for SharedDepthOneAllocator should also indicate its relationship to R0 and R0a-Cor2 in the dependency column.

### Issue 4: No explicit weakest precondition analysis
**ASN-0086, overall**: The ASN does not include explicit wp computations for any non-trivial postcondition.

**Problem**: The review template specifies wp analysis for non-trivial postconditions is mandatory. The ASN embeds wp-style reasoning within proofs (e.g., the "Single-tuple scope" remark on Nullify computes precondition obligations derivatively; the "A_K^{Σ'} membership of the fresh emission" remark on Emit_K computes obligations under regime (i)/(ii)) but doesn't label or present them as wp computations. A reader looking for implementation contracts via wp must reconstruct them. The non-trivial cases worth computing explicitly are:
- wp(Nullify(Σ, d_retr, a), "single-tuple scope holds at Σ'") — should yield: P0–P3 hold at Σ, the discipline holds along the chain reaching Σ, AND no crafted-span retraction in `L_R^Σ` covers `a`'s home (else regime (ii) failure at the fresh `b` produced by the internal Emit_R).
- wp(Emit_K(Σ, d, F, G), "(a, F, G) ∈ A_K^{Σ'}") — should yield: regime (i) (unit-depth retraction discipline) holds, AND no `L_R^Σ` tuple's coverage contains a fresh sibling-frontier address under `d`.
- wp(Nullify(Σ, d_retr, b₁) where b₁ ∈ L_R^Σ, "a₁ remains in `nullified(Σ')`") — should yield: trivially `true` (R6b is single-depth). This is a trivial-by-design case worth labeling.

**Required**: Add an explicit wp analysis subsection (or wp tags on Nullify / Emit_K's Definitions) computing the weakest preconditions for at least these non-trivial cases. R6b's trivial-by-design wp would help motivate the single-depth design choice.

## OUT_OF_SCOPE

### Topic 1: Behavior of higher-arity links under retraction
**Why out of scope**: ASN-0086 explicitly restricts attention to standard-triple links (`|Σ.L(a)| = 3`); higher-arity behavior is properly flagged in Open Questions.

### Topic 2: Concurrency model for Emit_K and Observe_K
**Why out of scope**: Properly flagged in Open Questions as requiring additional substrate-level commitments.

### Topic 3: Operational meaning of `nullified(Σ)` for crafted-span (regime-(ii)) retractions
**Why out of scope**: The ASN deliberately scopes `Nullify` to unit-depth spans (regime (i)) and flags crafted-span retractions as admissible but not its concern. Open Questions touches on this.

### Topic 4: Substrate-level realization paths for the sibling-frontier discipline
**Why out of scope**: The Open Questions section properly flags this as future work — tightening Emit_K's spec or the substrate primitive to make R0a unconditional.

VERDICT: REVISE
