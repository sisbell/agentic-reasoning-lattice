# Review of ASN-0091

## REVISE

### Issue 1: RE-subpres is derived but load-bearing for nothing

**ASN-0091, "REARRANGE as Vstream-Only Operation" (RE-subpres derivation) and Claims table**: "The bijection π preserves the subspace identity of every V-position: ... (RE-subpres). ... The derivation is abstract — it relies only on RA-π, RA-frame's `Σ'.C = Σ.C` and `Σ'.L = Σ.L`, pre-state S3★, RA-adm (for both post-state S3★ and post-state S3★-aux), and foundation L14."

**Problem**: Nothing downstream consumes RE-subpres. The K.μ~ realisation discharges admissibility clause (iv) "Directly from the R-PPERM/R-SPERM branch structure ... Discharged from the cut-sequence construction alone," not via RE-subpres. RE-sub is described as a "pointwise strengthening of RE-subpres," but RE-sub's own derivation is sourced from R-PPERM/R-FRAME-P, not from RE-subpres. Moreover the derivation takes RA-adm (which *assumes* post-state S3★/S3★-aux) as a premise, so RE-subpres merely unpacks an assumed invariant — it cannot help establish admissibility and is consumed by no RE-* claim. This is accretion: a stated consequence with no consumer.

**Required**: Remove the RE-subpres paragraph and its table row, or wire it in as an explicit premise of some claim that currently re-derives subspace behaviour from scratch.

### Issue 2: Realisation-specific net-effect reasoning placed in the abstract-class section

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "This makes π non-identity *as a permutation of V-positions*, but that is strictly weaker than ASN-0047's K.μ~ admissibility clause (ii) ... The realisation therefore splits on net effect: in the *non-trivial case* ... the realiser is K.μ~ ... and in the *collapse case* ... the transition is already the reflexive `Σ' = Σ` ..."

**Problem**: The collapse-vs-non-trivial split, the comparison against K.μ~ clause (ii), and the realiser routing are properties of the *concrete* REARRANGE_K realiser, not of the abstract Vstream-only class. They sit two sections ahead of "REARRANGE_K Realises the Abstract Class," which then points back at them ("the non-trivial case of the net-effect split witnessed in 'REARRANGE as Vstream-Only Operation'"). The concrete S5 witness is correct and worth keeping, but its placement forces a forward/backward reference pair around realiser-specific content lodged in the abstract section.

**Required**: Move the net-effect split, the K.μ~ clause-(ii) comparison, and the S5 collapse witness into the realisation section, where the K.μ~ admissibility discharge already lives. Keep in the abstract section only the empty/identity degenerate cases, which are genuinely class-level.

### Issue 3: Composition section carries a coverage-inventory in place of argument

**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"**: "The lemma's hypothesis ... is met by exactly the M(d)-function preserved-equality claims: RE-dom★, RE-ran★, RE-μ★, and RE-sub★ follow from it by induction. The remaining ★ forms chain by other mechanisms, not by this lemma: ..."

**Problem**: The chaining-lemma is stated once, then a multi-bullet inventory partitions every ★ label into "covered by the lemma" vs "chains by another mechanism." Each non-lemma bullet (RE-C★, RE-disc★, RE-proj★, etc.) restates its provenance, which the ★ table already records in its Provenance/Composition-Conditions columns. The prose duplicates the table rather than advancing the proof.

**Required**: State the chaining lemma and the genuinely distinct cases (RE-other★'s no-targeting side condition, RE-ext★'s per-step exterior condition, RE-trans★ clause (iii), the existential RE-frag★/coal★/eq★ construction), and let the ★ table carry the bare-equality cases instead of re-narrating each label's mechanism.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN restricts REARRANGE_K's cut subspace to s_C and only frames the link subspace (RE-sub). Defining a rearrangement that reorders the link subspace, and its invariants, is new territory — correctly deferred to an Open Question, not an error here.

### Topic 2: Joint reconstitution of a split transcluded source span
**Why out of scope**: RE-trans establishes per-fragment origin (RE-origin) but explicitly leaves whether two fragments jointly reconstitute the original source span to the first Open Question. That is a future claim, not a gap in this ASN.

VERDICT: REVISE
