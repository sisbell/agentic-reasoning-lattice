# Review of ASN-0131

I checked the mathematics first, then ran the anti-bloat pass the classifier calls for.

The technical content is sound. I verified: RE-DEF's biconditional structure makes RE-SND/RE-CMP immediate reads (correct); RE-UDIST's factoring through a region-independent `Avail(Σ)` is valid (the `touch_W` predicate is `a`-independent, so the existential splits); RE-CWP's weakest precondition is exactly the "no pair dropped" condition (`coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅` is the correct contrapositive of the drop condition, and the `R = ∅` collapse to `RE = ∅` checks out); RE-RET's iff holds under the stated hypothesis, with the backward direction correctly resting on R-Scope's single-tuple confinement; the worked instance computes correctly and genuinely exercises RE-OVL, RE-CLIP, RE-WHOLE, per-endset surfacing, and RE-UNIT; the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement argument is rigorous; the stability enumeration over the transition vocabulary is complete (K.μ⁺/K.μ⁻/K.μ~/shifts/K.λ as movers; K.μ⁺_L, link-only K.μ⁻, K.α, K.δ, K.ρ, off-document edits as non-movers). Boundary cases (empty image, no addressable links, empty slot, `R = ∅`) are all handled. No correctness gaps.

The REVISE items are anti-bloat polish, which the standing rule (any REVISE item ⟹ REVISE) and the explicit mandate require me to surface.

## REVISE

### Issue 1: Rhetorical / self-important meta-framing recurs throughout
**ASN-0131, multiple sections**: representative instances —
- §"The unit of the answer": "RETRIEVEENDSETS is a realisable query, not merely a defined set." (the three preceding sentences already establish computability — the clause adds nothing)
- §"The unit of the answer": "Read what this definition does, and as importantly, what it withholds."
- §"The unit of the answer": "It is worth recording what the operation reads and what it does not."
- §"When does an endset touch": "Three properties of this definition are worth stating, because each is a claim an alternative implementation would also have to honour."
- §"Stability" (M-only lift): "This lift is the load-bearing step, and it is *depth-independent*..."

**Problem**: Each is an intro flourish or self-importance label that the reader skips to reach the substantive content beneath it. The classifier (`review-mode.anti-bloat`) flags this note specifically for accreted meta-prose; under that mandate these framings are noise, not house style. The content they introduce (RE-LOC, the touch properties, the lift) is fine — the framing is removable without loss.

**Required**: Delete the framing clauses; lead each passage with the claim itself. E.g., the decidability paragraph can end at "...finitely many decidable tests over the finite store." and the RE-LOC paragraph can open with "`RE` reads the arrangement `Σ.M(d)` and the link store `Σ.L`...".

### Issue 2: The "Claims Introduced" table restates prose derivations at paragraph length
**ASN-0131, Claims Introduced table** (e.g., RE-DEF, RE-EDIT, RE-CWP entries): each cell runs ~100–130 words, re-embedding region conditions, citation chains, and partial derivations already present in the body.

**Problem**: This is the "two passages say the same thing in different words" pattern at scale. The convention in the foundation ASNs is a terse claims table (compare ASN-0034's TA5 row, ASN-0058's M-rows — one-line statements). A reference table should *state* each claim crisply; restating the derivation duplicates the body the reader just read.

**Required**: Compress each cell to the claim statement plus its label/status, with derivations left to the body. RE-DEF's cell, for instance, needs the set-builder, the region/`touch_W`/`addressable` definitions, and `Σ' = Σ` — not the decidability recap.

### Issue 3: Transclusion section presents a definitional fact as transclusion-forced
**ASN-0131, §"Anchoring reached through borrowed content"**: "This forces what the returned span must *describe*. The endset's spans are over content identity — the I-addresses of the content's permanent home — not over the V-positions where `d` currently displays the borrowed content."

**Problem**: Endsets reference I-addresses by definition (ASN-0043's `Endset`/`coverage`), independent of any transclusion. The note itself states RE-IDENT is "independent of transclusion" two sentences earlier. So transclusion does not *force* the span representation; it merely illustrates an already-definitional property. The causal framing ("This forces") overstates transclusion's role.

**Required**: Reframe as illustration ("Transclusion makes this concrete: because spans denote I-addresses, the *same* endset is reached through `d` and through `d_src`...") rather than derivation, so it does not appear to derive a fact the definitions already fix.

## OUT_OF_SCOPE

The note's Open Questions already defer the genuinely-future topics appropriately — cross-store completeness (OQ5), link-subspace regions (OQ7), intersection composition (OQ4), rendered answers (OQ3), multiplicity preservation (OQ2), entirety-vs-touching-spans (OQ1), and type-slot/content matching (OQ6). No additional deferral is missing.

The passing mentions of out-of-scope operations (FINDLINKSFROMTOTHREE, READLINK, etc.) are contrasts, not claims, so they do not violate the scope exclusion — the note correctly does not define guarantees for them.

VERDICT: REVISE
