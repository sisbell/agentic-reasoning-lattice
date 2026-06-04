# Review of ASN-0091

This is a deep, careful note. The technical content checks out: the abstract Vstream-only class (RA-*) is correctly bridged to the REARRANGE_K realiser, the net-effect split (non-identity π vs. `M'(d) ≠ M(d)`) is handled with an explicit collapse branch, the RE-* consequences are derived from the right clauses, and the boundary cases (empty, identity, collapse) each carry a witness. The five worked examples are concrete and each isolates a distinct phenomenon (basic pivot, 4-cut μ-displacement, interior R-EXT, bijection non-uniqueness, net-effect collapse) — concrete examples are exempt from the anti-bloat sweep and I am not flagging their volume.

The findings below are anti-bloat redundancies, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Duplicate sentence in "Pointwise-fixity frames"
**ASN-0091, REARRANGE_K Realises the Abstract Class**: "For each class, ASN-0084's R-PPERM and R-SPERM define π directly as the identity on that position set, and the corresponding arrangement-preservation clause records `Σ'.M(d)(v) = Σ.M(d)(v)` for the same positions; together these supply the named fact in full pointwise form. These frames derive directly from R-PPERM/R-SPERM and R-FRAME-P/S(a)."
**Problem**: The second sentence restates the first verbatim in content — both say the frames come from R-PPERM/R-SPERM plus the arrangement-preservation clause (R-FRAME-P/S(a)). Two paragraph-final sentences saying the same thing.
**Required**: Delete the trailing sentence "These frames derive directly from R-PPERM/R-SPERM and R-FRAME-P/S(a)."

### Issue 2: Double-justification of RE-cov
**ASN-0091, Links Persist; Their Coverage Cannot Move**: "Since RE-L preserves every endset verbatim, coverage is preserved — RE-cov is ASN-0098's LP3 (CoverageInvariance) instantiated at a REARRANGE step"
**Problem**: One claim is given two independent justifications in a single sentence — derivation "from RE-L" (endset preserved → coverage preserved) and "LP3 instantiated at a REARRANGE step." The Provenance table lists only "abstract (from RE-L)." Pick one route.
**Required**: Keep the RE-L derivation (matching the table) and drop the LP3-instantiation clause, or vice versa — not both.

### Issue 3: Meta-prose in "Composite-Boundary Properties"
**ASN-0091, Composite-Boundary Properties**: "ASN-0047's **ExtendedReachableStateInvariants** then delivers **P4★ ∧ P4a ∧ P7a** at Σ' in a single citation; no hand re-derivation of the three is required, since the foundation theorem already owns them at every reachable composite boundary and Σ' is one."
**Problem**: The clause "no hand re-derivation of the three is required, since the foundation theorem already owns them at every reachable composite boundary and Σ' is one" explains *why a step is unnecessary* rather than advancing the argument. The load-bearing content is just: Σ' is a reachable composite boundary, so ExtendedReachableStateInvariants gives P4★∧P4a∧P7a. The same section's later "not merely for the one trace ending in this REARRANGE step" is a similar defensive clarification.
**Required**: Reduce to the operative claim ("Σ' is a reachable composite boundary, so ExtendedReachableStateInvariants delivers P4★ ∧ P4a ∧ P7a at Σ'") and drop the editorializing.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: Open Question 2 asks what a rearrangement on the link subspace would mean and what invariants it must preserve. REARRANGE_K fixes the cut subspace at `S = s_C` (CS3), so this ASN correctly only proves the link subspace is left frame-invariant (RE-sub). A link-rearranging operation is a future ASN.

### Topic 2: Reconstitution of same-source split spans
**Why out of scope**: Open Question 1 (whether two fragments of a same-source transcluded span jointly reconstitute the original) is correctly deferred — RE-trans establishes per-byte origin preservation (RE-origin) but not joint span reconstitution, and the note is explicit that this is not established here.

VERDICT: REVISE
