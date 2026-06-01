# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ admissibility clause (i) mislabeled as "full per-state invariant package"
**ASN-0047, *Decomposition of K.μ~***: "π is admissible iff (i) the induced post-state M'(d) would satisfy the full per-state invariant package on M'(d) — S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, S3★, and S3★-aux, from which the derived D-SEQ★ follows..."

**Problem**: The enumerated set is *not* the full per-state package. CL-OWN, CL-UNIQ, and S2 are per-state arrangement invariants on M'(d) (each quantifies over `dom(M(d))`), and S8★ is also a per-state arrangement property — yet none appear in clause (i). These are instead *derived* for K.μ~ (the matrix discharges CL-OWN/CL-UNIQ via link-subspace fixity, S2 via "π bijection," S8★ via the rebuild). Labeling the partial list "full" wrongly suggests the admissibility filter itself guarantees CL-OWN/CL-UNIQ/S2/S8★, when in fact the fixity proof (Steps C, D) *concludes* them. This matters because the necessity argument leans on link-subspace fixity being derived, not assumed.

**Required**: Rename clause (i) to "the arrangement-*shape* invariant package" (or similar) and state explicitly that CL-OWN, CL-UNIQ, S2, and S8★ are derived consequences of fixity/bijection (per the verification matrix), not admissibility hypotheses.

### Issue 2: P4a discharge mechanism stated three times verbatim
**ASN-0047, *Cross-layer invariants* (P4a box), *Composite-boundary verification matrix*, and Class (b) prose**: The same two-route discharge — "for `R' \ R`, J1'★ supplies a content-subspace witness at Σ'; for the carried-forward slice, the IH supplies a trace-state witness propagated by P2" — appears in the P4a definition box's "*Discharge mechanism*" paragraph, again in the matrix P4a row, and a third time in the Class (b) P4a prose.

**Problem**: Three restatements of one argument. The reader who follows the P4a definition box must re-skip the same content at two later sites to confirm nothing new is said. This is the "multiple paragraphs say the same thing" accretion the anti-bloat classifier flags.

**Required**: State the discharge once (the definition box is the natural site) and have the matrix/Class (b) prose point to it without re-deriving.

### Issue 3: Redundant "caller-checked precondition" restatement in K.μ~ necessity/sufficiency
**ASN-0047, *Necessity and sufficiency of the precondition***: "As a caller-checked precondition: a transition whose `M(d)|_{dom_C}` is constant-valued ... does not fire ... **Equivalently**, the operation's discharge of admissibility clause (ii) is a sufficiency obligation that the operation realises ... the precondition makes that obligation discharge via the full-clearance form."

**Problem**: The "Equivalently" sentence re-expresses the preceding sentence (precondition gate ⟺ sufficiency obligation), and both repeat the role already established by the formal necessity and sufficiency directions above. Defensive restatement that does not advance the argument.

**Required**: Delete the closing paragraph or compress to a single sentence noting the precondition is caller-checked.

## OUT_OF_SCOPE

### Topic 1: Forked document's arrangement relationship to source, transitive transclusion provenance, link inheritance under forking
**Why out of scope**: These are correctly deferred to the Open Questions and concern future operation/provenance specifications (INSERT/COPY-class semantics and version-lineage invariants), not the elementary transition taxonomy this ASN fixes.

VERDICT: REVISE
