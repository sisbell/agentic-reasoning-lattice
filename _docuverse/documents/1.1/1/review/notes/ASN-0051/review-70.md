# Review of ASN-0051

## REVISE

### Issue 1: Editorial note's SV-label list incomplete

**ASN-0051, Editorial note**: "the SV-labelled claims throughout (SV2–SV11, SV13; SV0/SV1/SV12 withdrawn — see Properties Introduced) are the survivability properties"

**Problem**: The body introduces SV14 (DocumentDerivedDiscoverySurvivability) as a substantive labeled survivability claim, and it appears in the Properties Introduced table and is cited in SV13(i). The Editorial note's enumeration of survivability properties omits SV14, which suggests SV14 was added in a later revision without updating the framing summary.

**Required**: Update the parenthetical to include SV14: e.g., "(SV2–SV11, SV13, SV14; SV0/SV1/SV12 withdrawn — see Properties Introduced)" or "(all SV-labelled claims — see Properties Introduced)".

### Issue 2: Single-block precondition gap for SV11 fragment cover formula

**ASN-0051, SV11**: "let B = {β₁, ..., β_p} be the maximally merged block decomposition... `ran_text(M(d)) = ⋃_{k=1}^{p} I(β_k)` (B1 applied to the restriction together with C1a, ASN-0058...)"

**Problem**: The derivation states "B1 applied to the restriction" gives the I-extent cover, but B1 (ASN-0058) is a property of *V-extents* not I-extents. The actual reasoning needed: B1 covers all V-positions in dom(restriction), so ran(restriction) = ⋃ M(d)(V(β_k)) = ⋃ I(β_k) since each block's V→I mapping is M-restricted. The leap from V-coverage to I-extent union should be made explicit rather than packaged into a B1 citation.

**Required**: Add the explicit step deriving I-extent union from V-coverage and M's per-block mapping rule (M0/M3 from ASN-0058), or rephrase the citation chain.

### Issue 3: SV11 attainment proof's "fragment count ≤ non-empty term count" not derived

**ASN-0051, SV11 attainment biconditional, (⇒) direction**: "The fragment count is bounded above by the non-empty-term count (each non-empty term is contiguous within its block by the S0-convexity argument below, hence lies in exactly one maximal fragment within its block; distinct fragments therefore arise from distinct or non-coalescing terms)"

**Problem**: The parenthetical asserts the bound but doesn't derive it. The actual derivation: each non-empty term lies in exactly one fragment; the map "non-empty term → containing fragment" is well-defined; image cardinality (fragment count) ≤ domain cardinality (non-empty term count). The sentence "distinct fragments therefore arise from distinct or non-coalescing terms" gestures at this but isn't a derivation — it's a restatement.

**Required**: Either state the surjection argument explicitly, or replace the parenthetical with a brief two-line proof.

### Issue 4: (m=1, p≥4) generalization recipe under-specified

**ASN-0051, SV11 attainment witnesses, "Generalisation to (m = 1, p ≥ 4)"**: "the per-p direct construction circumvents this... allocate 2p + 1 T4-valid siblings... apply p − 1 excision composites — each a K.μ~ + K.μ⁻ pair removing one chosen I-address... Each excision targets an *interior* (non-boundary) I-address of a *currently-targeted* block of size ≥ 3"

**Problem**: The recipe requires each excision to target a block of size ≥ 3, but doesn't establish that such a block always exists after the first few excisions. The text gives explicit construction at p = 4 (sizes 9 → 2,6 → 2,2,3 → 2,2,1,1) where the third excision exhausts the size-3 block. For arbitrary p ≥ 5, the schedule "any whose successive excisions each target an interior position of a current block of size ≥ 3 suffices" — but at p = 5 starting from 2p+1 = 11 siblings, after four excisions, do we still have a size-≥3 block to target? Not always: 11 → 2,8 → 2,2,5 → 2,2,2,2 (no more interior of size-≥3). The recipe needs to allocate enough siblings (or schedule excisions on larger blocks first) to maintain a size-≥3 block until p − 1 excisions complete.

**Required**: Either prove that 2p+1 siblings suffice with an appropriate schedule, or revise the sibling count formula (e.g., allocate 3p − 2 siblings).

### Issue 5: SV5 proof's "ran-equality from K.μ~" assertion needs scope qualifier

**ASN-0051, SV5 proof**: "The middle equality is range invariance alone: K.μ~'s ran-preservation corollary (ASN-0047) records that K.μ~ preserves ran(M(d)) as a set — ran(M'(d)) = ran(M(d)) — because K.μ~ is a bijection on V-positions that holds the V↦I assignment's image fixed"

**Problem**: This is stated as if it's a primitive property, but ran-preservation under K.μ~ is the *composite-level* corollary (as discussed in the Composite-level scope subsection further down). The proof reads "ran(M'(d)) = ran(M(d))" without yet noting this is endpoint-only. A reader following linearly might be confused when the very next subsection clarifies "per-step π is not claimed to be invariant — it shrinks at the K.μ⁻ midpoint and recovers at the K.μ⁺ endpoint."

**Required**: Add a parenthetical at first use noting the equality is endpoint-only, or reorder so the composite-level scope subsection precedes the proof.

### Issue 6: SV6 proof's element-level restriction timing

**ASN-0051, SV6 proof**: After deriving "zeros(t) ≥ 3, with at least three zeros at positions p₁, p₂, p₃", the proof says "Restricting to element-level t."

**Problem**: The proof asserts conclusions about origin(t) for *all* element-level t in the span. But the SV6 conclusion only needs the contrapositive for the element-level b. The intermediate generality (origin(t) = origin(s) for all element-level t ∈ ⟦(s,ℓ)⟧) is stronger than needed and could be confusing. Clearer to state the contrapositive directly: "For any element-level b with origin(b) ≠ origin(s), the field-decomposition argument shows b cannot agree with s on positions 1..k-1, hence b ∉ ⟦(s,ℓ)⟧."

**Required**: Either retain the generality with explicit note that it's stronger than needed, or restructure to derive the contrapositive directly.

### Issue 7: SV13(e) bullet on M-frame transitions misses K.μ⁺_L distinction context

**ASN-0051, SV13(e)**: "K.α, K.δ, K.ρ, and K.λ all preserve M-values in their frame, so locate(e, d) is unchanged for every endset e and every pre-existing document d ∈ dom(Σ.M)..."

**Problem**: This list pointedly excludes K.μ⁺_L (since it modifies M at its targeted d), but the prior bullets group K.μ⁺_L with K.μ⁺ under "Extension." Reader has to cross-reference to understand why K.μ⁺_L is treated differently here vs in the extension bullet. The "K.μ⁺_L parallel" subsection clarifies, but its placement after the M-frame list creates a forward reference.

**Required**: Either reorder so K.μ⁺_L parallel precedes the M-frame bullet, or add an inline note in the M-frame bullet: "(K.μ⁺_L modifies M at its targeted d and is covered under Extension above)".

### Issue 8: Witness shape W(m, 2) ambiguity at m=2

**ASN-0051, "Boundary witness shapes" — W(m, 2)**: defined "for m ≥ 3" with single-element spans.

**Problem**: The explicit W(2, 2) standalone witness uses multi-element spans (block sizes 10, 5), and the text correctly notes this differs from the single-element-span W(m, 2)-shape instance at m = 2 (which would have block sizes 8, 3). However, since (α_2) lifts W(m, 2) → W(m+1, 2) for m ≥ 3, starting from W(3, 2), there's no consistency claim that the W(m, 2)-shape at m = 2 (block sizes 8, 3) would lift to W(3, 2) (block sizes 10, 5) under (α_2). The text says "either base would suffice for the iterated lift family," but doesn't verify the shape-based m=2 → m=3 lift.

**Required**: Either verify the W(m,2)-shape m=2 → W(3,2) lift under (α_2), or remove the "either base would suffice" claim and explicitly start (α_2) at W(3, 2).

## OUT_OF_SCOPE

(none — the ASN appropriately scopes link type semantics and replication to other ASNs without making claims about them)

VERDICT: REVISE
