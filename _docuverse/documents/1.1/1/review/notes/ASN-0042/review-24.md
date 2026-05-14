# Review of ASN-0042

## REVISE

### Issue 1: Σ.alloc reinvents foundation notation
**ASN-0042, throughout (O4, O5, O2, O6, O8, O10, O14, O16, O17, summary)**: "(A a ∈ Σ.alloc : ...)"
**Problem**: ASN-0040 (foundation) defines `Σ.B` as the baptismal registry — the set of baptized tumblers. ASN-0042 introduces `Σ.alloc` with no definition and no explicit relationship to `Σ.B`. The review standards explicitly state: "If an ASN invents its own notation for something a foundation already defines, flag it as a REVISE item."
**Required**: Either rename `Σ.alloc` to `Σ.B` consistently, or explicitly define `Σ.alloc` and state its relationship to the foundation's `Σ.B` at first use.

### Issue 2: O7(c) "well-founded" claim is incorrect
**ASN-0042, O7 proof, postcondition (c)**: "The recursive structure is well-founded: each delegation introduces a principal with a strictly longer prefix (condition (i)), and prefix length is bounded by address length."
**Problem**: "Prefix length is bounded by address length" is meaningless — which address? By T0(b) (UnboundedLength), tumbler length is unbounded. The recursion is *ascending* (each delegation strictly extends a prefix), so it does not terminate by length-induction. Either "well-founded" is used loosely (each step is well-defined) and misleading, or it's incorrect (claiming termination).
**Required**: Remove the "well-founded" claim or replace with the correct observation — each delegation step is independently well-defined; the recursion may continue indefinitely.

### Issue 3: AccountLevelPermanence induction structure is implicit
**ASN-0042, AccountLevelPermanence proof**: "We prove this by induction on the order in which principals enter Π... By the inductive hypothesis, π_d itself entered Π through an act authorized by π or a sub-delegate of π."
**Problem**: The induction is invoked without explicit setup. No `P(n)` statement is given. The "base case" (bootstrap non-nesting) and "inductive step" (delegation introducing π') do not match a single induction variable — they appear to mix induction on transition count and induction on delegation-chain depth. A reader cannot verify the induction is well-founded or that base case and step match the same proposition.
**Required**: State the induction variable explicitly. Either (a) formulate `P(n) :=` an explicit proposition with matching base and step, or (b) recognize the lemma statement is single-transition and recast the proof as direct — the multi-step consequence follows by repeated application without invoking induction.

### Issue 4: T5 misattributed for prefix comparability
**ASN-0042, AccountLevelPermanence proof**: "Both pfx(π) and pfx(π_d) are prefixes of pfx(π'), and two prefixes of the same tumbler are comparable by T5's nesting lemma."
**Problem**: T5 (ContiguousSubtrees) is about subtrees occupying contiguous intervals on the tumbler line, not about prefix comparability. The needed property — that two prefixes of the same tumbler are linearly ordered by `≼` — follows directly from Prefix (PrefixRelation) in the foundation: if `p₁ ≼ a` and `p₂ ≼ a` with WLOG `#p₁ ≤ #p₂`, then `(p₁)ᵢ = aᵢ = (p₂)ᵢ` for `1 ≤ i ≤ #p₁`, hence `p₁ ≼ p₂`. The proof of O2 uses this property correctly without citing T5.
**Required**: Replace "T5's nesting lemma" with the Prefix definition or prove the comparability step explicitly.

### Issue 5: "FieldParsing" used as a colloquial citation
**ASN-0042, AccountField, O6, AccountPrefix proofs**: "By FieldParsing...", "by T4's field structure (FieldParsing)...", "FieldParsing from ASN-0034"
**Problem**: "FieldParsing" is not a labeled property in the foundation. The foundation has T4 (HierarchicalParsing), T4a (SyntacticEquivalence), T4b (UniqueParse), T4c (LevelDetermination). Using "FieldParsing" conflates distinct foundation properties and makes citations imprecise — at each call site it is unclear which specific property is being invoked.
**Required**: Replace each "FieldParsing" reference with the specific foundation property: T4b (UniqueParse) for unique field decomposition, T4 for the validity predicate itself, T4c for level labels.

### Issue 6: Worked example does not cover O7, O8, O9
**ASN-0042, Worked Example section**: The example illustrates O0–O6 and O10 but does not verify O7 (delegation), O8 (irrevocability), or O9 (node-locality) against the constructed scenario.
**Problem**: Per review standards: "the ASN should verify its key postconditions against at least one specific scenario." For the π_N → π_A delegation, the six conditions (i)–(vi) of the delegation relation are not walked through. O8's irrevocability is mentioned informally ("Nelson's 'forevermore'") but the abstract postcondition `ω_{Σ'}(a) ≠ π` is not checked against a concrete address. O9 (node-locality) is entirely absent from the example — no cross-node case appears.
**Required**: Extend the worked example to (a) verify each of conditions (i)–(vi) for the π_A delegation in state Σ₀; (b) explicitly check O8's postcondition for π_N over a₁ across multiple states; (c) introduce a second-node principal (e.g., `pfx(π_M) = [2]`) and an address `[2, 0, ...]` to illustrate O9.

### Issue 7: Finiteness assumption in O10 zeros=0 case
**ASN-0042, O10 proof, zeros=0 case**: "Collect the user-field components of all existing sub-delegate prefixes... such a value exists because a finite set of natural numbers has a maximum"
**Problem**: The argument depends on the finiteness of sub-delegates. The justification "by O15... the system has undergone finitely many transitions" treats reachability via finite transition sequences as obvious, but no axiom in this ASN establishes this. The bootstrap clause O14 should be strengthened — `|Π₀| < ∞` — and the inductive step (each transition adds at most one principal, per O15) then gives `|Π_Σ| < ∞` in every reachable state.
**Required**: Add `|Π₀| < ∞` to O14 (or cite an existing finiteness axiom from the foundation), and explicitly derive `|Π_Σ| < ∞` from O14 + O15 as a lemma the O10 proof can cite.

## OUT_OF_SCOPE

### Topic 1: Formal bridge to allocator discipline and baptism registry
**Why out of scope**: The ASN introduces `allocated_by_Σ(π, a)` as primitive with mechanism "out of scope... belongs to the tumbler baptism specification". A bridge ASN would establish the formal correspondence `allocated_by_{Σ'}(π, a) ⟺ a ∈ Σ'.B ∖ Σ.B ∧ π = ω(a)` and verify ASN-0040's `Bridge1` projects through the ownership layer.

### Topic 2: Ownership transfer mechanism
**Why out of scope**: Listed as open question. Nelson alludes to "someone who has bought the document rights" but Gregory's codebase has no transfer machinery. Any transfer regime requires structure external to the address — properly a separate ASN.

### Topic 3: Cross-node identity federation
**Why out of scope**: O9 establishes node-local authority. Cross-node federation (the same human owning prefixes on multiple nodes) is mentioned in prose but is a separate problem — what protocol governs cross-node identity establishment.

### Topic 4: Domain density (ghost addresses)
**Why out of scope**: Listed as open question — whether `dom(π)` may contain gaps between baptized siblings. Intersects with content model.

### Topic 5: Concrete authentication mechanisms
**Why out of scope**: O11 explicitly parameterizes over principal identity. Concrete certificate/key/token mechanisms belong elsewhere.

VERDICT: REVISE
