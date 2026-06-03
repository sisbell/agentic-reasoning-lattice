# Review of ASN-0069

## REVISE

### Issue 1: V12(b) formula has an unbalanced parenthesis
**ASN-0069, §"Permanence Across Source and Fork", V12(b)**: "`(A a ∈ ran(M'(d_new)) :: a ∈ dom(C'')` for every subsequent state `Σ''` (P0, S0/S1)"

**Problem**: The opening `(A` quantifier is never closed — counting delimiters, the `(A` has no matching `)`. Compare V12(c), which is balanced (`... :: (a, d_new) ∈ R'')`). A precise reader has to reconstruct the intended scope.

**Required**: Close the quantifier, e.g. `(A a : a ∈ ran(M'(d_new)) : a ∈ dom(C''))`.

### Issue 2: V9a closes with explanatory color that does not advance the claim
**ASN-0069, §"Provenance Recording", V9a**: "What R *does* support is three independently recoverable pieces: the relation reports *who has it*; `origin(a)` (the original allocator) tells you *who made it*; the parent prefix (V2's ancestry) tells you *who you came from*."

**Problem**: V9a's substantive content is the negative claim — R records containment, not acquisition path. The trailing three-way "who has it / who made it / who you came from" gloss restates facts already carried by V9 (containment), S7/`origin` (allocator), and V2 (ancestry) in mnemonic essay form. It is the kind of meta-prose the anti-bloat pass targets: it does not establish or sharpen anything, it decorates.

**Required**: Drop the trailing sentence; the negative claim plus the V9/origin/V2 citations already stand on their own.

### Issue 3: Worked example re-proves V12(a) in the empty-source case rather than citing it
**ASN-0069, §"Worked Example", "Empty source (V7)"**: "V12(a) — joint permanence of the two entities — holds substantively: `d_src° ∈ E'_doc` (K.δ's E-frame `E^{(1)} = E ∪ {d_new°}` preserves `E ⊆ E^{(1)}`; P1; the K.δ-alone composite has `Σ' = Σ^{(1)}`...) and `d_new° ∈ E'_doc` (V1) persist into every subsequent state by T8 and P1."

**Problem**: §"The Empty-Source Case" already states the organizing principle (structural properties V1/V2/V3/V12(a) hold substantively; quantified-over-`V_{s_C}` properties hold vacuously), and V12 already carries the permanence derivation. A worked example should *check* the concrete instance against the property, not re-run the general proof (K.δ E-frame, P1, T8). This re-derivation duplicates content the body already established — "two paragraphs say the same thing in different words."

**Required**: In the worked example, instantiate the result concretely (the empty fork `d_new°` and `d_src°` are permanent) and cite V12(a)/V7; do not re-discharge the frame/permanence argument.

## OUT_OF_SCOPE

### Topic 1: V6a's link-projection apparatus (coverage / project / discoverable_from)
**Why out of scope**: V6's core fork guarantee — `V_{s_L}(d_new) = ∅` — is a legitimate property of CREATENEWVERSION. But V6a builds three new definitions (`coverage`, `project`, `discoverable_from`) used nowhere else in the ASN, solely to establish a link-*discoverability* preservation result, and the worked example carries a matching discoverability walk. Discoverability of which links reference an address is link-discoverability semantics; the projection machinery would be better grounded in a dedicated link/discoverability ASN, with this ASN retaining only the frame consequence (`L' = L`, source projections preserved) that follows directly from V4 + V5. The heavy apparatus is borderline drift from the fork operation into link semantics.

VERDICT: REVISE
