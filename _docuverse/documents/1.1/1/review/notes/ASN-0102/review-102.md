# Review of ASN-0102

I checked the COPY definition, the precondition collection (PC1–PC4), the `wp(COPY, S3★)` reduction, X16's tiling/disjointness argument, and the full X17 invariant-preservation discharge (all conjuncts of `ExtendedReachableStateInvariants`, the composite-boundary properties P4★/P4a/P7a, and the transition theorem P3). The mathematics is sound and unusually complete: the three position classes tile `[1, n_S+W]` with no gap or overlap, S8a is discharged per-class (not just at the anchor `v`), the provenance routing (RR) correctly handles the self-transclusion case where a copied address is already range-resident (P4★ at `Σ_0` makes the redundant write non-`R`-new, so J1'★ stays vacuous), and the four worked scenarios exercise the merging *and* non-merging halves of X8/X12. I found no correctness or missing-edge-case defects.

The findings below are anti-bloat (this note carries `review-mode.anti-bloat`).

## REVISE

### Issue 1: X1 carries fold-residue duplication
**ASN-0102, X1 (ContentStoreInvariance)**: "Gregory's trace confirms … the I-address high-water mark … is therefore unchanged by COPY (Q16). In particular, COPY consumes no previously-unallocated address: since `dom(Σ'.C) = dom(Σ.C)`, no address absent from `dom(Σ.C)` becomes present."
**Problem**: The final sentence restates `dom(Σ'.C) = dom(Σ.C)` in different words — "no address absent from `dom(Σ.C)` becomes present" is the same proposition unfolded. The Claims table then repeats it a third time ("in particular COPY consumes no previously-unallocated address"). This reads like residue from the recent fold of X2 into X1: the consumed-address phrasing was likely X2's content, now re-asserting what X1 already states. Two paragraphs (plus the table row) say the same thing.
**Required**: Drop the "In particular, COPY consumes no previously-unallocated address …" sentence and the table's "in particular" clause; the equality `dom(Σ'.C) = dom(Σ.C)` already carries it.

### Issue 2: X6 closes with a rhetorical restatement
**ASN-0102, X6 (OriginPreservation)**: "Nelson's 'you always know where you are' [LM 2/40] is a structural consequence of X3 … Attribution cannot be stripped, because there is no attribution metadata to strip: there is only the address."
**Problem**: The final sentence ("Attribution cannot be stripped, because there is no attribution metadata to strip") restates the immediately preceding clause ("a structural consequence of X3, not a separately maintained annotation"). It is essay emphasis, not a step in the derivation — the claim that `origin(a)` is unchanged is already established by S7 + M16a one sentence earlier.
**Required**: Remove the trailing restatement; the derivation ends at "is invariant under arbitrarily deep copy chains" / the M16a citation.

### Issue 3: Preamble meta-framing
**ASN-0102, standing-state paragraph**: "The tumbler vocabulary … is taken from the foundations without restatement. Mapping blocks … are taken from ASN-0058." And the Definition: "Because the standing state carries five components, `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)`, the contract must pin all five."
**Problem**: "is taken from the foundations without restatement" and "the contract must pin all five" are meta-prose about the document's construction rather than content that advances the operation's definition. The symbols are used where needed; announcing in advance that they are imported, and justifying that the effect clause names five components, is the kind of orientation a precise reader skips past.
**Required**: State the operation directly. The five-component frame is self-evident from the five effect clauses (`Σ'.C =`, `Σ'.L =`, `Σ'.E =`, target arrangement, `Σ'.R =`); drop the "must pin all five" justification and the "without restatement" framing.

## OUT_OF_SCOPE

(none — the four Open Questions are correctly deferred to future ASNs and the note defines no claims on out-of-scope topics.)

VERDICT: REVISE
