# Review of ASN-0119

I checked the imported postconditions against ASN-0084 (R-EXT/R-P1/R-P2 and R-EXT/R-S1/R-S2/R-S3 transcribed correctly), verified both worked examples arithmetically (pivot `A B C D E ↦ A C D E B`, swap `A B C D E F ↦ A E F C D B`, the two-move composite and its intermediate `A C D B E`), and re-derived the load-bearing claims. The technical core is sound: RA1 (`ran` invariance), RA2 (bijection), the per-subspace S3★ derivation through `π⁻¹`, the S8★ argument via R-BLK + R-CANON, RA7a's inline derivation from RA1 (and the correct reason for *not* citing LP11 — REARRANGE_K is not K.μ~ and the no-op case lies outside LP11's non-triviality hypothesis), and the four contiguity cases all hold. The findings below are the anti-bloat patterns the classifier flags, plus one completeness gap in an exhaustiveness claim.

## REVISE

### Issue 1: The "cuts resolve against one arrangement" claim is stated twice, the first as a self-described preview of the second
**ASN-0119, "Cuts and regions" and "Atomicity"**:

"Cuts and regions": *"The cuts are interpreted against one arrangement. This is the first thing the 'two cuts at once' formulation reveals, and we record it before going further: all of c₀, …, c_{n-1} are coordinates in the same M(d), so the geometry of the regions is fixed before any reassignment occurs."*

"Atomicity": *"Second, the cut coordinates resolve against a single, unshifted frame. All of c₀, …, c_{n-1} are coordinates in one M(d), so the regions' boundaries cannot drift out from under each other mid-operation."*

**Problem**: These carry the identical claim (all cuts are coordinates in one `M(d)`). The "Cuts and regions" occurrence explicitly announces itself as a forward-preview of the Atomicity discussion ("the first thing the 'two cuts at once' formulation reveals, and we record it before going further") — the named anti-bloat pattern of two paragraphs saying the same thing, with prose justifying where the point is placed. The substantive treatment (the anti-drift consequence, the "every cut valid simultaneously" payoff) lives in Atomicity; the preview adds only framing overhead.
**Required**: Drop the preview framing in "Cuts and regions." If a one-clause statement of region well-posedness is needed there, state it without the "this is the first thing … we record it before going further" pointer; let the Atomicity section carry the claim and its consequence.

### Issue 2: Reading-process narration in structural slots
**ASN-0119, "The two streams" and "What is preserved"**: *"we will be watching, throughout, for the property that this value is carried intact while the key under which it is filed is permuted."* … *"A consequence we will lean on repeatedly: the set of I-addresses the document references is invariant."*

**Problem**: "we will be watching, throughout" and "we will lean on repeatedly" narrate the reading process rather than advance the argument — essay prose in slots that should carry claims. The precise reader skips them to reach the math (the value/key distinction; `ran(M'(d)) = ran(M(d))`).
**Required**: State the property and the consequence directly. The address-vs-position invariant and RA1's range-invariance stand on their own without the meta-framing.

### Issue 3: The "fully accounted for" invariant census omits S3★-aux
**ASN-0119, "What is preserved"**: the inherited-invariant list reads *"Concretely: text-subspace contiguity (D-CTG★), sequentiality (D-SEQ★), the minimum position (D-MIN★), V-position well-formedness (S8a), uniform per-subspace depth (S8-depth), and finiteness (S8-fin) …"* and the closing census states *"The remaining ExtendedReachableStateInvariants conjuncts (P6, P7, P8, P7a, P4a, the L-family, the C-family) are preserved by the C/E/R/L frame, so the invariant package REARRANGE joins is fully accounted for."*

**Problem**: S3★-aux (SubspaceExhaustiveness — every V-position has subspace `s_C` or `s_L`) is a named conjunct of the ExtendedReachableStateInvariants package, but it appears in *neither* explicit bucket. It is M-keyed (a property of V-positions), so "preserved by the C/E/R/L frame" does not reach it; and it is absent from the named key-set list. It is covered only implicitly by the earlier universal sentence ("Every reachable-state invariant that constrains this set alone is therefore inherited verbatim"). When the note makes the explicit exhaustiveness claim "fully accounted for," a conjunct that no enumeration names is a gap. (The E-family conjuncts NodeLineage and ActivatedEmission are similarly absent from the parenthetical enumeration, though the frame mechanism's "E" does reach them.)
**Required**: Add S3★-aux to the key-set-inherited list — it constrains `V_{s_C}(d) ∪ V_{s_L}(d)` (a key-set property unchanged by RA2), so it is inherited verbatim by the same argument as D-CTG★/D-SEQ★. One word in the list discharges it. Optionally name an "E-family" term in the census so NodeLineage/ActivatedEmission are explicitly placed.

## OUT_OF_SCOPE

### The five Open Questions
**Why out of scope**: cross-document boundary-hood under transclusion, unserialized concurrent rearrangement, the content-discovery-index invariant under footprint fragmentation, prior-arrangement recoverability, and the closed-form-arithmetic boundary guard are all genuinely new territory, correctly deferred. They need no action in this ASN, and the note does not drift into them — its claims (RA0–RA9) remain abstract state guarantees, and the Gregory implementation discussion is used only to motivate the abstract tiling requirement, not to specify mechanics.

VERDICT: REVISE
