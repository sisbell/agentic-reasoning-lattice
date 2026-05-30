# Review of ASN-0058

This is a mature note (review-54) carrying the anti-bloat classifier. The substantive algebra — block decomposition (M2), split/merge duality (M9/M10), canonical uniqueness (M12), and resolution (C0–C2) — checks out: proofs cover the boundary cases (n=1 in M0, empty arrangement in M2, interior cut in M4), M-int and the M12 partition corollary are complete, and the C0 infinitude argument and M16a origin-confinement argument are sound. The findings below are residual meta-prose, which is what this cycle targets.

## REVISE

### Issue 1: Section-opening prose previews downstream results
**ASN-0058, Content References (section intro)**: "The canonical decomposition (M11, M12) applies to any restriction of an arrangement satisfying the structural preconditions, and every resolved I-address satisfies referential integrity."
**Problem**: This sentence states the conclusions of C1a and C1 in an essay slot before either is defined or proven. It is a forward-reference summary that does not advance the section — the claims are made and discharged below. This is exactly the "essay content in structural slots" the anti-bloat pass targets.
**Required**: Delete the sentence. C1a and C1 carry their own statements where they are proved.

### Issue 2: Defensive framing around M0
**ASN-0058, Width Coupling**: "The first property is the structural keystone on which the entire algebra rests." and "This is not a convenience of representation."
**Problem**: Both are editorial/defensive framing that does not advance the M0 proof. "This is not a convenience of representation" is a defensive justification of the property's importance rather than a statement of what the mapping does. (The surrounding "each V-position references exactly one I-byte … positional and unit-ratio" is substantive — a statement of what the mapping does — and should stay.)
**Required**: Remove the two framing sentences; keep the unit-ratio description.

### Issue 3: Bare forward pointer after M1
**ASN-0058, after M1 (OrderPreservation)**: "Across blocks, the same I-address may appear at multiple V-positions; we return to this below."
**Problem**: "we return to this below" is meta-navigation pointing at M13/M14 without advancing the M1 discussion. The cross-block sharing claim stands on its own where M13 introduces it.
**Required**: Drop the forward pointer (and the dependent half-sentence, or fold the substantive observation into M13).

## OUT_OF_SCOPE

None. The Open Questions are correctly deferred (I-space discontinuity structure, decomposition lattice, V-extent/block-count relations), and the ASN does not stray into INSERT/DELETE/COPY operation effects, which belong to downstream operation ASNs.

VERDICT: REVISE
