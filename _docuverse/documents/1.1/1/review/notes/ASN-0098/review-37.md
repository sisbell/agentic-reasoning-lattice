# Review of ASN-0098

This ASN is mature and mathematically solid. I checked LP-Fin's interval-finitude proof case by case (the `#d ≤ #d_0` bound, sub-cases A/B, the `s'' = X` forcing, the n-count), the wp derivation in LP12a (genuine biconditional, hence genuinely weakest), and the operation-coverage (every vocabulary element K.σ/K.α/K.λ/K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~/K.δ/K.ρ has a governing lemma). I found no correctness defects. The findings below are the anti-bloat patterns the `review-mode.anti-bloat` classifier flags — accreted meta-prose that the precise reader must read past.

## REVISE

### Issue 1: LP4 Frame note is a use-site inventory plus hypothetical-frame justification
**ASN-0098, Frame Conditions (note after LP4)**: "The downstream applications below (LP5, LP6, LP7, LP8, LP14, etc.) all instantiate `d ∈ dom(Σ.M)` and rely on M1 … should a future reference frame admit transitions that remove documents from `dom(M)`, LP4's intersection form remains correct as stated, but the LP5–LP8 corollaries below would need re-derivation against the changed frame."
**Problem**: This enumerates LP4's downstream consumers (the flagged "definition's introduction enumerates downstream consumers" pattern) and defends the formulation against a hypothetical future frame that the working-frame section has already fixed. Neither advances LP4's reasoning.
**Required**: Reduce to the load-bearing fact — LP4 quantifies over `dom(Σ.M) ∩ dom(Σ'.M)` and downstream uses lift via M1 — and delete the consumer roster and the future-frame paragraph.

### Issue 2: "Numbering note" is document-history meta-prose
**ASN-0098, after Claims Introduced table**: "Labels LP1 and LP15 are unassigned. LP14 labels the K.ρ frame lemma. LP-Comp is not a claim label — the covering case-analysis it once named is stated in prose…"
**Problem**: This narrates the document's own labeling history. It carries no system guarantee and rots as labels change. Classic accretion.
**Required**: Delete. If gaps in LP-numbering must be recorded at all, that belongs in the PR/commit, not the spec.

### Issue 3: Meta-prose labeling an argument "motivational rather than load-bearing"
**ASN-0098, "Non-canonical spans are unconditionally non-tight"**: "The structural finitude argument that follows is therefore motivational rather than load-bearing for non-canonical decidability: it explains *why* the canonical restriction is the right structural cut…"
**Problem**: This is prose *about* the following prose — it pre-explains the role of an argument instead of making it. The argument itself (grounds (i)/(ii)/(iii)) is substantive; the framing sentence is not.
**Required**: State the decidability fact directly (non-canonical spans are rejected by definitional canonical-form; grounds (i)/(ii) additionally exhibit infinite intersections) and drop the "motivational vs load-bearing" editorializing.

### Issue 4: LP12b scope-restriction closes with defensive justification of the act of flagging
**ASN-0098, LP12b "Scope restriction"**: "We flag the omission rather than silently restricting LP12b's scope, so the asymmetry between content-canonical (wp = false on this retention pattern) and link-canonical (wp value unsettled) is visible to readers."
**Problem**: Declaring the link-canonical case out of scope is legitimate; justifying *that we are declaring it* is meta-prose addressed to the reader rather than content. The technical asymmetry (the structural argument inverts in the link-canonical case) is already stated in the preceding sentences.
**Required**: Keep the technical statement of why the argument inverts; delete the closing sentence about visibility-to-readers.

### Issue 5: Citation chain restated redundantly in the claims table
**ASN-0098, Claims Introduced table (LP-Fin Corollary row)**: "Used in LP12b to derive … LP12b in turn discharges LP12a's deferred … boundary case. The citation chain is LP12a → LP12b → LP-Fin Corollary."
**Problem**: The LP12a→LP12b→LP-Fin dependency is already stated at each of those three claims in prose. Restating the chain a fourth time, inside a one-line table cell, is the flagged "multiple paragraphs defer to the same downstream location" accretion compressed into the index.
**Required**: The claims table should state what each claim says, not re-narrate inter-claim citation. Trim the row to LP-Fin Corollary's statement.

## OUT_OF_SCOPE

### Topic 1: Link-canonical companion case for LP12b
LP12b self-declares the link-canonical wp class (every span `s = [d_s, 0, s_L, k_s]` under `n'_{s_C}=0, n'_{s_L}>0`) as future work. This is a correct boundary to draw — the structural argument genuinely inverts there — and the omission is flagged rather than hidden. Not an error in this ASN.

### Topic 2: Open Questions (reverse-discovery, V-order reflection, link-to-link induced discovery, fork link-subspace projection)
These are correctly deferred; each defines a new primitive or invariant beyond the projection-displacement scope.

VERDICT: REVISE
