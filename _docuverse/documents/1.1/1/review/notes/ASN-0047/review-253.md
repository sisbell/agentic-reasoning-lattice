# Review of ASN-0047

I reviewed the state model, the seven elementary transitions plus K.μ~, the coupling constraints, the D-SEQ★ derivation, the K.μ~ fixity proofs, and the five worked examples. The core argument is sound: the per-state/composite-boundary partition is coherent, the D-SEQ★ case split (m=2, m≥3) is rigorous, K.μ~-FIX and link-subspace fixity chain correctly, and the worked examples genuinely verify their postconditions. I confirmed the FrontierEquivalence biconditional, the GlobalLineage termination argument, and the K.δ zeros/parent identities. I found no correctness defect.

One finding remains, matching the `review-mode.anti-bloat` classifier this note carries.

## REVISE

### Issue 1: Self-admitted non-advancing prose in worked examples

**ASN-0047, *Worked example: fork with subsequent insertion*, K.α step**: "(As corroboration only: cross-document disjointness — T10a.{2,5} → T10 at the document-pair (d₁, d₂) — independently gives a₃ ∉ {a₁, a₂}, but **this adds nothing**, since {a₁, a₂} = dom(C₂) is already covered by the first-emission discharge.)"

**Problem**: This is prose the author explicitly labels as adding nothing — a use-site corroboration the reader must read past to follow the discharge that actually carries the claim (SubAllocatorBundle.FirstEmission). It is exactly the "prose that does not advance reasoning" the forward-reference-accretion guidance flags. A related instance sits in the same example family: the link-allocation Step 1 L11a note — "GlobalUniqueness (ASN-0034) is *not* invoked for the first emission (the FirstEmission clause is the load-bearing route here); GlobalUniqueness applies from the second emission onward" — is a route-disambiguation inventory that restates which lemma fires where, rather than advancing the verification.

**Required**: Delete the parenthetical that "adds nothing." For the L11a note, keep only the operative citation (first emission discharged by SubAllocatorBundle.FirstEmission; subsequent by GlobalUniqueness) and drop the disambiguation commentary. State the load-bearing discharge; do not narrate the discharge that was *not* used.

## OUT_OF_SCOPE

### Topic 1: Link-subspace withdrawal / tombstoning mechanism
The tension between Nelson's tombstoning (LM 4/9) and D-CTG★/D-MIN★ (interior link withdrawal forced into suffix-only removal) is correctly deferred to an open question. This is new territory — a separate withdrawal primitive outside K.μ⁻'s contract — not a defect in this ASN.

### Topic 2: Forked-arrangement / transitive-transclusion provenance guarantees
The relationship a forked document's initial arrangement must bear to its source, and provenance under transclusion chains, are appropriately left as open questions rather than specified here.

VERDICT: REVISE
