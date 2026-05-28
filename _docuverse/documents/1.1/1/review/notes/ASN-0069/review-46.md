# Review of ASN-0069

## REVISE

### Issue 1: T3 (CanonicalRepresentation) missing from Dependency Audit
**ASN-0069, "Dependency Audit"**: The audit lists ASN-0034 supplying "T0, T1, T8, T12, TA5, TA5(b), TA5(c), TA5(d), TA5-SigValid, T10a, T10a.4, T10a.6, T10a.7, Prefix, and ASN-0034's NAT-order transitivity."
**Problem**: T3 is invoked explicitly in V11a's recovery argument ("T3 (CanonicalRepresentation, ASN-0034) — equal length plus componentwise agreement is identity — gives that this prefix equals dⁱ_new") and is load-bearing — without T3 the recovery's identification of prefix-with-componentwise-agreement as identity has no source. T3 is also implicit in V2's analogous argument.
**Required**: Add T3 to the Dependency Audit's ASN-0034 supply list.

### Issue 2: V11 premise scope remark conflates two distinct discharge mechanisms
**ASN-0069, "Remark on V11's premise scope"**: "Modifications M-targeted at d_src itself between step 1 and step k are also admissible — they fall outside the premise's per-step-immediate-source scope (which only covers d^{i-1}_new between adjacent step boundaries)..."
**Problem**: The remark mixes two structurally different cases without separating them: (a) modifications between step i-1's post-state and step i's pre-state targeting documents *other than* the chain step's immediate source (e.g., a third document or a non-immediate chain member), and (b) modifications to d_src after step 1. Case (a) is genuinely outside premise scope and harmless to V11's induction. Case (b) appears outside scope only because V11's *conclusion* anchors at Σ — the premise covers d_src only at i=1, where the gap is empty by the reflexivity convention. The remark elides the distinction and leaves the reader inferring why each case is admissible. The earlier paragraph's mention of "V5a Corollary 2 supplies the discharge condition" further muddies this: V5a Corollary 2 is the *operational* discharge for premise satisfaction, not the structural justification for what the premise leaves unconstrained.
**Required**: Split the remark into two distinct paragraphs — one for non-immediate-source modifications (premise structurally silent) and one for d_src modifications after step 1 (conclusion anchoring at Σ). Each should cite the operative mechanism (V5a Corollary 2 for the operational discharge; conclusion anchoring for the historical fixing).

### Issue 3: V9a's parenthetical justification is compressed and slightly wrong
**ASN-0069, V9a**: "(if origin(a) = d_new, which cannot occur in a fresh fork since d_new ∉ E_doc pre-fork)"
**Problem**: The cited reason ("d_new ∉ E_doc pre-fork") is not quite the operative one. A_C(d_new) is activated by the K.δ step *during* the fork composite (SubAllocatorAxiom), so post-K.δ, A_C(d_new) exists; the absence of any a with origin(a) = d_new in ran(M'(d_new)) follows from (i) V3's C' = C, ensuring the inherited I-addresses are exactly those already in dom(C) before the fork, and (ii) the pre-fork absence of A_C(d_new) (since d_new ∉ E_doc pre-fork means SubAllocatorAxiom had not yet activated it). The current phrasing collapses the two-step argument into the activation precondition alone, losing the inheritance-from-pre-fork-state step that V3 supplies.
**Required**: Rewrite the parenthetical to cite both V3 (the inherited addresses come from pre-fork dom(C)) and the pre-fork inactivity of A_C(d_new) (since d_new ∉ E_doc pre-fork).

### Issue 4: V8a's claim is narrower than its name suggests
**ASN-0069, V8a**: "*correspondence persistence under content-store growth*: Subsequent K.α allocations (extending C) leave every arrangement unchanged..."
**Problem**: The name "correspondence persistence under content-store growth" suggests V8a applies to any sequence where C grows. But the body restricts to "K.α-only sequence" — K.α is one of several transitions that can grow dom(C); K.λ also extends L (and L14 prevents overlap with C, but the name's "content-store growth" framing is loose). More importantly, the property holds for any sequence consisting entirely of *arrangement-preserving* steps, not just K.α. The narrowing to K.α-only is artificial given that V8b covers the general case anyway. The name promises more than the body delivers.
**Required**: Either rename to "correspondence persistence under K.α" (matching the body) or broaden the body to cover all M-preserving sequences (K.α, K.λ, K.ρ), with V8b handling the cases where arrangements do shift. The current asymmetry is a documentation issue, not a correctness one.

### Issue 5: V11a's value characterization claim is loose at the boundary
**ASN-0069, V11a**: "value 1 when step i is a first fork of d^{i-1}_new (V1's first-fork sub-case at inc(d^{i-1}_new, 1)), and value m ≥ 2 when step i is a subsequent fork"
**Problem**: V11a claims the chain extension value is 1 *or* m ≥ 2, presented as exhaustive. But the construction-defined value is `1 + j` where j is the *subsequent emission count* on A_v(d^{i-1}_new). At j = 0 (first emission), value = 1. At j ≥ 1, value = 1 + j ≥ 2. The claim is correct, but the proof body conflates "value 1 + j at the j-th subsequent emission" with "value m ≥ 2 for subsequent forks" without explicitly closing the boundary case j = 0 / j ≥ 1. A reader has to do the j-indexing themselves to verify exhaustiveness.
**Required**: Either present the unified characterization "value = 1 + j where j ≥ 0 is the subsequent-emission count" (covering both cases uniformly), or explicitly enumerate the two disjoint cases and verify they exhaust A_v(d^{i-1}_new)'s emission stream.

### Issue 6: Verification of K.δ sub-case A freshness leans on T10a's at-most-once clause without addressing alternate emission paths
**ASN-0069, "The Fork Composite" verification, K.δ sub-case A**: "Sub-case A's predicate that A_v(d_src) has emitted no prior version means no K.δ event with (t = d_src, k = 1) has fired yet; the at-most-once constraint then forces that no past K.δ event has placed inc(d_src, 1) into E via this spawning path."
**Problem**: The argument shows no past K.δ event with parameters (d_src, 1) has fired. T10a.6 then rules out cross-allocator collision. But the verification does not explicitly address whether some K.δ event with *different* parameters could produce the same address `inc(d_src, 1)` within the same allocator family — e.g., a K.δ at (d_src, 2) might in principle produce a tumbler that coincides with inc(d_src, 1) under some degenerate construction. TA5's component-formulas rule this out (at k = 1 vs k = 2, the position-#d_src+1 components differ — value 1 vs value 0 as field separator), but the verification does not cite this and treats it as folded into T10a.6. A rigorous reading wants the within-allocator-family case explicitly addressed: either by the parametrized-cases analysis (TA5(d) at different k' values produces structurally distinct outputs) or by an explicit appeal to T10a-N (necessity of the sibling restriction).
**Required**: Either add a step citing TA5(d)'s structural difference between k = 1 and k = 2 outputs (or T10a.7 over the joint emission space of the parent allocator), or explicitly note that T10a.6 covers all spawning-parameter variations under the at-most-once-per-(t, k') clause.

## OUT_OF_SCOPE

None — the ASN appropriately defers operation mechanics (INSERT, DELETE, etc.), link semantics, and version DAG structure to other ASNs.

META: The ASN is correctly framed as a state-and-operation specification — it defines a state transition (V0), establishes properties of that transition (V1–V12), and derives consequences from foundation invariants. It does not drift into implementation mechanics.

VERDICT: REVISE
