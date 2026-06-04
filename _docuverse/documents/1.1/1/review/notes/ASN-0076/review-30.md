# Review of ASN-0076

## REVISE

### Issue 1: Use-site inventory closing the Foundation Recap
**ASN-0076, Foundation Recap**: "These are the foundation items most central to the construction. Additional items — from ASN-0034 (T0, T1, T4, T4b, T10a.7, T12, TA5, ...), ASN-0043 (...), ASN-0047 (...), and ASN-0098 (LP13 ...; LP12, LP17, LP18 ...) — are cited at the points where they bear on a specific discharge."
**Problem**: This is a downstream-consumer inventory — it enumerates every foundation item that will later be cited "at the points where they bear" rather than advancing any definition. It is exactly the use-site-inventory accretion pattern. The actual citations already appear at their points of use; the catalog adds nothing.
**Required**: Delete the closing inventory paragraph. Each foundation item is introduced where it is used.

### Issue 2: Citation-preference meta-prose
**ASN-0076, Foundation Recap (LP13 bullet)**: "LP13 is the proper citation wherever EDITLINK's reasoning crosses multiple atomic steps; we use it in preference to repeated single-step L12 applications."
**Problem**: This is prose about which citation to prefer — methodology commentary, not reasoning. It explains the author's citation discipline rather than stating a fact the proofs need.
**Required**: Remove the sentence; cite LP13 directly at the multi-step sites (E1, E5, E9 already do).

### Issue 3: Defensive "we do not re-derive" prose in E0
**ASN-0076, E0 (successor step, depth bound)**: "We do not re-derive the structural facts the foundation already fixes for `A_L(d_new)` outputs: ... is a foundation consequence — not something this proof must establish — and we cite it rather than reconstructing it from T0/T4 field-segment primitives."
**Problem**: Defensive meta-prose explaining what the proof declines to do and why. The reader does not need a justification for citing a foundation fact; the citation itself suffices.
**Required**: Replace with the direct citation of the `zeros(t') = zeros(t) = 3` foundation consequence, dropping the self-narration.

### Issue 4: Repeated deferral to the same future ASN
**ASN-0076, multiple sections**: "deferred to a future ASN on type-endset conventions" (The Composite, τ_sup paragraph), "defers to a future ASN on type-endset conventions (see Open Questions)" (The Supersession Relationship), and again in Appendix Step 2.
**Problem**: Three paragraphs in different sections defer the same `τ_sup`-convention question to the same unnamed downstream location. This is the multiple-deferral-to-one-location pattern; it compounds across the note.
**Required**: State the deferral once (the Open Questions list already carries it) and remove the in-body repetitions, leaving at most a single pointer.

### Issue 5: E10 imagines an excluded notification step
**ASN-0076, E10 (final paragraph)**: "Adding such a notification step would require either operating on a document the executor does not own ... or coordinating with the original owner's system ... The append-only, no-notification design follows from the underlying architecture."
**Problem**: E10's proof is the one-line frame composition (`M'(d)=M(d)`, `R'=R`). The closing paragraph then imagines adding a notification step that the K.λ frame already excludes — prose reasoning about a case the claim's carrier forecloses. It does not advance E10.
**Required**: Cut to the frame argument plus, at most, one sentence noting notification is not performed.

### Issue 6: Over-derivation in T12 length check
**ASN-0076, E0 (T12 span well-formedness)**: "`#ℓ_old ≥ 1` by T0 ...; concretely `#ℓ_old ≥ 8` since `ℓ_old` is element-level — `zeros(ℓ_old) = 3` (L1) gives three separators ... for a minimum total of `3 + 1 + 1 + 1 + 2 = 8`."
**Problem**: T12(b) requires only positivity of the length (`#x ≤ #x` saturates with equality once `Pos(δ(1,#x))` holds). The "concretely `≥ 8`" computation is decorative — it discharges nothing the `≥ 1` step does not already discharge. Same for the `E_to` bullet.
**Required**: Drop the `≥ 8` field-counting addendum; keep `#x ≥ 1` by T0.

## OUT_OF_SCOPE

### Topic 1: Termination and well-definedness of the reader procedure
**Why out of scope**: The Appendix already marks the procedure as illustrative and defers termination, successor-extraction, and cycle questions to future ASNs. These are genuinely new territory (link-search and supersession-relation invariants), not defects in EDITLINK.

VERDICT: REVISE
