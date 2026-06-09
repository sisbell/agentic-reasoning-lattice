# Review of ASN-0116

## REVISE

### Issue 1: P7a proof relies on an unstated precondition
**ASN-0116, "The document remains one coherent sequence" (PROV) / Precondition**: "For prior addresses `b ∈ dom(C)`: the pre-state is itself a composite boundary, so P7a held there, giving some `(b, d') ∈ R`."
**Problem**: The post-state P7a (ProvenanceCoverage) is discharged for prior content addresses by *assuming* P7a holds at the pre-state. But P7a is a composite-boundary property in ExtendedReachableStateInvariants (ASN-0047) — it holds only at composite boundaries, not at arbitrary reachable states. INSERT's stated precondition is only `d ∈ dom(M)`, `n ≥ 1`, value/position well-formedness. Nothing in the precondition establishes that `Σ` is a composite boundary, so the proof step is not licensed by the stated preconditions.
**Required**: Add to INSERT's precondition that `Σ` is a composite boundary (the natural input for a composite), or derive coverage of prior addresses without appeal to pre-state P7a.

### Issue 2: P6 range identity omits the cross-subspace contribution
**ASN-0116, "A weakest precondition"**: "left positions keep their I-addresses (I-LEFT), shifted positions carry their I-addresses to new slots (I-SHIFT), and the new block adds exactly `A_new` (I-NEW). Hence `ran(M'(d)) = ran(M(d)) ∪ A_new`."
**Problem**: LP12 (ASN-0098) consumes the *full* `ran(M(d))`, which includes the images of `d`'s positions in the link subspace `s_L` (and any other subspace). The derivation enumerates only subspace-`S` positions (left, shifted, new block) and never accounts for the cross-subspace positions that also contribute to both `ran(M(d))` and `ran(M'(d))`. The conclusion is correct (those images are identical pre- and post- by F-SUB), but the chain as written is incomplete — it is exactly the "X follows from Y" shortcut without the F-SUB step. Note the PROV section is careful to scope its identity to the "content-subspace range," whereas P6 silently widens it to the full range.
**Required**: Add the F-SUB citation establishing that the link/cross-subspace range of `M'(d)` equals that of `M(d)`, so the full-range identity is fully derived.

### Issue 3: Repeated non-inheritance meta-prose (anti-bloat)
**ASN-0116, "The document remains one coherent sequence"**: three consecutive paragraphs — "We do *not* inherit referential integrity from ASN-0082's I3-S3: that lemma is proved under the content frame I3-C…", "The same non-inheritance applies… I3-S7 is no more inheritable than I3-S3…", and "Contiguity is INSERT's own theorem, not an inherited lemma… inapplicable here."
**Problem**: Each paragraph narrates the *provenance of the reasoning* (which foundation lemma was tempting, why its frame is broken) rather than advancing the discharge. This reads as prior-finding resolutions relocated into the body. The load-bearing content in each is a single clause (the direct discharge: "each left/shifted position carries `M(d)(v) ∈ dom(C) ⊆ dom(C')`, so S3★ holds by S3 + P2"); the surrounding why-not-inherit narrative is meta-prose the precise reader must skip.
**Required**: Keep one brief note that the I3-C-framed lemmas don't transfer, then state the direct discharges. Drop the repeated "we do not inherit / no more inheritable than / not an inherited lemma" framing.

### Issue 4: Range identity derived twice (anti-bloat)
**ASN-0116, PROV section** ("First fix the range identity that drives all four… range-new… are precisely `A_new`") **and "A weakest precondition" section** ("We read it off the Effect… `ran(M'(d)) = ran(M(d)) ∪ A_new`").
**Problem**: The same underlying range fact is derived in two sections with overlapping prose. This is the pattern the recent "hoist block-disjointness" revision targeted, recurring for the range identity.
**Required**: Hoist a single named range-identity fact (full range and its content-subspace restriction) and cite it from both PROV and P6, as block-disjointness was hoisted.

## OUT_OF_SCOPE

### Topic 1: Insertion at a transcluded/shared position; concurrent insertions; provenance under transclusion; post-edit fragmentation
**Why out of scope**: These are the note's own Open Questions and concern transclusion (ASN-0118), concurrency/serialization, and downstream editing — new territory, not defects in the INSERT specification presented here.

VERDICT: REVISE
