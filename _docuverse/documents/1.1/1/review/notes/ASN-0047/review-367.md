# Review of ASN-0047

## REVISE

### Issue 1: Matrix justifies K.δ as "frame" for M-dependent invariants, but K.δ is not a pure frame on M

**ASN-0047, Class (a) verification matrix, K.δ column**: The S3★, S3★-aux, CL-OWN, and CL-UNIQ rows all give the K.δ cell as "frame", whereas the S8a/S8-depth/S8-fin row correctly gives the K.δ cell as "new doc has M(d)=∅ (vacuous)".

**Problem**: K.δ is a pure frame on M only in the Node/Account cases. In the Document case, the effect is `dom(M') = dom(M) ∪ {e}` with `M'(e) = ∅` (stated explicitly at the K.δ definition and in the Bridging lemma). So K.δ *does* touch M. The correct preservation argument for S3★, S3★-aux, CL-OWN, CL-UNIQ under the Document case is the same vacuous-on-the-new-empty-arrangement argument the matrix already uses for S8a/S8-depth/S8-fin — not "frame." The S2 cell already gets this right ("frame (M(e)=∅ on new entity disjoint)"), which makes the bare "frame" entries in the four M-dependent rows internally inconsistent.

**Required**: Replace the K.δ "frame" cell in the S3★, S3★-aux, CL-OWN, and CL-UNIQ rows with the vacuous-on-empty-arrangement justification (matching the S8a row and the S2 cell), or split each into the Node/Account (true frame) and Document (vacuous on M'(e)=∅) sub-cases.

### Issue 2: Forward-reference accretion around the K.μ~ shape-invariant discharge

**ASN-0047, K.μ~ definition clause (i)** and **Class (a), "K.μ~ discharge for the arrangement-shape invariants"**: Clause (i) carries the aside "the operational discharge of D-SEQ★ at Σ' (and of S8-fin(Σ'), which sits outside the shape package) is given once in the Class (a) paragraph … below, and is not restated here; this package constrains which V-position *domains* exist, not which I-address each position carries." The Class (a) paragraph then re-narrates the same filing: "bundled in the matrix with S8a/S8-depth but *not* part of the shape package," "discharged independently of admissibility (i) and K.μ~-FIX," "D-SEQ★ is then derived at Σ'."

**Problem**: Two paragraphs in different sections both describe the *bookkeeping* of which invariants are in the "shape package" versus discharged separately (S8-fin, D-SEQ★, the S8★ delta), and each defers to the other. This is meta-prose about the proof's organization rather than the argument itself — the reader must hold both copies to confirm they agree. This is the forward-reference/duplicate-paragraph accretion the review-mode classifier targets, and it is distinct from the previously-declined sprawl/split findings.

**Required**: State the shape-package membership and the separate discharge of S8-fin(Σ') and D-SEQ★ once, at the Class (a) paragraph (the discharge site), and reduce the clause (i) aside to a bare pointer without re-explaining the package boundary.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering (DELETEVSPAN)
**Why out of scope**: The penultimate Open Question correctly defers the renumbering-aware interior contraction to a future ASN; K.μ⁻'s suffix-only model is a deliberate scoping choice, and named operations including DELETEVSPAN are listed OUT OF SCOPE. No revision required — the ASN handles this correctly as an open question rather than under-specifying it.

VERDICT: REVISE
