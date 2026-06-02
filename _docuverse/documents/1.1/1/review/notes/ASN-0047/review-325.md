# Review of ASN-0047

I checked the arithmetic (entity-chain construction, anchor derivations `b_C(d)=inc(d,2)`, `b_L(d)=inc(b_C(d),0)`, the k=0/1/2 zero-count identities), the D-SEQ★ derivation (both m=2 and m≥3 cases, including the infinite-family contradiction in Step 1), the J4 φ-bijection order/multiplicity argument, FrontierEquivalence/ChildSpawnFreshness, and the P4a/J1'★ relationship (P4a witnesses range over composite boundaries, so J1'★'s boundary witness is consistent with it — not a gap). Correctness holds up. My findings concern the meta-prose / forward-reference accretion the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: S3★ and S3★-aux defer in lockstep to the same downstream cell
**ASN-0047, *Generalized referential integrity***: S3★ closes with "Per-transition preservation of S3★ is discharged in the Class (a) verification matrix below (the joint *S3★ / S3★-aux* prose entry), the authoritative site for both invariants." S3★-aux then closes with "Per-transition preservation is discharged jointly with S3★ (see the pointer above)."
**Problem**: Two definition boxes in the same section each carry a paragraph whose only content is a forward pointer to the same downstream location, plus the essay phrase "the authoritative site for both invariants." This is precisely the flagged pattern — "multiple paragraphs in different sections defer to the same downstream location" and naming an "authoritative site" in a structural slot. Neither sentence advances the definition's meaning; the reader must skip both to reach the actual discharge.
**Required**: Drop both deferral paragraphs. The Class (a) matrix and its prose entry already carry the discharge; the definitions need no forward pointer to it.

### Issue 2: Defensive "discharged (not merely asserted)" framing in K.δ case (ii)
**ASN-0047, *Elementary transitions*, K.δ case (ii)**: The k=1 sub-case states the freshness read is "a fact discharged (not merely asserted) by ChildSpawnFreshness at `k' = 1`," and the k=2 sub-case repeats "a fact discharged (not merely asserted) by ChildSpawnFreshness at `k' = 2`."
**Problem**: "(not merely asserted)" argues about the *quality* of the discharge rather than performing it — defensive meta-prose responding to an anticipated objection, repeated verbatim across sub-cases. Citing the lemma that discharges the obligation is sufficient; the parenthetical adds no reasoning and reads as a residue of a prior review exchange.
**Required**: Reduce to the plain citation ("discharged by ChildSpawnFreshness at `k'=1`") in both sub-cases.

### Issue 3: "Derived distinctness corollaries" restate matrix content already established
**ASN-0047, *Class (a)*, "Derived distinctness corollaries"**: The *Entity distinctness* and *Link distinctness* paragraphs state that K.δ/K.λ freshness preconditions handle distinctness ("the freshness guard `e ∉ E` and its GlobalUniqueness distinctness preservation are the case-(ii) preconditions discharged at the K.δ definition" … "freshness `ℓ ∉ dom(L) ∪ dom(C)` … is SubAllocFresh at `x = L`"), with forward pointers to CrossDocEntityDisjoint / CrossDocDisjoint.
**Problem**: This duplicates the S4 cell rationale and the K.δ/K.λ definition-box preconditions already cited in the same matrix, then forwards to lemmas stated elsewhere. The substantive content (cross-document distinctness) lives in the named lemmas; these paragraphs are a use-site inventory of where distinctness "is discharged," not new reasoning.
**Required**: Either fold these one-line facts into the relevant matrix cells (S4, the Entity/Link rows) or cite the lemmas directly without the intervening restatement paragraphs.

## OUT_OF_SCOPE

### Topic 1: Interior-position arrangement contraction (renumbering)
**Why out of scope**: The ASN models contraction as suffix removal only; interior `DELETEVSPAN`-style compact-and-renumber is correctly deferred to a named open question and is not an error in this ASN's elementary-transition layer.

### Topic 2: Link-subspace correspondence-run canonicity
**Why out of scope**: S8★ honestly drops ASN-0036 S8 condition (c) for the link subspace (length-1 decomposition, non-canonical), justified because link labels target `dom(L)` not `dom(C)`. Whether a canonical link-run partition is needed is a future-ASN question; nothing downstream here consumes it.

VERDICT: REVISE
