# Review of ASN-0091

The technical content is strong. I checked the arithmetic in all six worked examples (3-cut pivot, 4-cut swap μ-delta, interior cuts, bijection non-uniqueness, net-effect collapse) and the run-cardinality witnesses (RE-frag/coal/eq) against R-P1/R-P2/R-S1/R-S2/R-S3 — they compute correctly. The L-chain lemma, the RE-disc biconditional chain, RE-proj transport, and the RA-adm/binary-transition/composite-boundary partition of foundation invariants are sound. The cross-references are all to foundation ASNs (0034, 0036, 0047, 0053, 0058, 0084, 0093, 0098); no non-foundation references appear in the body.

The remaining issues are accretion, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Provenance columns restate body derivations
**ASN-0091, "Claims Introduced" tables**: e.g. RE-ran's Provenance cell — "abstract (target case from RA-π; non-target case from RA-frame's other-document clause)".
**Problem**: The Provenance column compresses and repeats the derivation already given in the body (RE-ran, RE-μ, RE-proj, RE-disc each derive exactly this case structure in prose). This is the "two passages say the same thing in different words" pattern, split across table cell and body. A reader following the body never needs the cell; a reader reading the table re-reads the body.
**Required**: Reduce Provenance entries to a bare premise-label list (e.g. "RA-π; RA-frame") and let the body carry the derivation, or drop the column where the body already derives the claim. Keep only entries that add something the body omits (e.g. "structural (state-independent)").

### Issue 2: Proof bodies crammed into K.μ~ admissibility table cells
**ASN-0091, "K.μ~ admissibility clause (i)–(v) ← discharge" table, clause (iv) cell**: a five-step proof ("...every affected-range position v lies in V_S(d) (by R-PRE(iv)...), so subspace(v) = S... R-PPERM/R-SPERM map it to a position of the form c₀ + (offset)... so subspace(π(v)) = S = subspace(v) (OrdShiftHom(a)). Discharged from the cut-sequence construction alone").
**Problem**: A multi-step argument sits inside a table cell (a structural slot). The content is substantive verification, but its placement degrades readability — the reader must parse a paragraph-length proof out of a one-line discharge slot, and clauses (i) and (iii) carry similar cell-internal proofs.
**Required**: Move the per-clause discharges into prose; keep the table cells as pointers ("by the cut-sequence construction; see below") or one-clause summaries.

### Issue 3: RA-bndy section leads with why-it-is-needed rather than what it requires
**ASN-0091, "Composite-Boundary Properties"**: the precondition RA-bndy is one line ("Σ is the final state of a trace of valid composites"), preceded by a paragraph explaining *why* it must be imposed ("...ExtendedReachableStateInvariants splits its conclusion... includes such interior states, at which P4★/P4a/P7a need not hold. We therefore impose...").
**Problem**: This is the "prose around a precondition explains why it is needed rather than what it states" accretion pattern. The motivation can be compressed to a clause; the current paragraph is rationale, not argument that advances a claim.
**Required**: State RA-bndy, then justify in a single sentence ("interior composite states need not satisfy P4★/P4a/P7a, so the boundary claims require the pre-state at a boundary"). Drop the expanded restatement.

## OUT_OF_SCOPE

### Topic 1: 4-cut collapse illustration
The net-effect split's collapse mechanism is illustrated only via the 3-cut R-P1/R-P2 form, and the collapse worked example is 3-cut. The dichotomy itself ("splits on net effect") is generic and the empty-sequence realiser is cut-count-agnostic, so this is an illustration choice, not a proof gap — not a required revision.

### Topic 2: Open Questions (span-splitting reconstitution, link-subspace rearrangement, run-cardinality bounds)
The five Open Questions correctly defer span-reconstitution after a cut, link-subspace REARRANGE semantics, and cardinality bounds to future ASNs.

VERDICT: REVISE
