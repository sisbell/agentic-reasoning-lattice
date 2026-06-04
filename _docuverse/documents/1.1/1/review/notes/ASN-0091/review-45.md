# Review of ASN-0091

This ASN is mathematically careful — I checked the fragmentation, coalescence, equality, collapse-case, 4-cut, interior-cut, bijection-non-uniqueness, and two-step composition witnesses against R-P1/R-P2/R-S1–S3 and the run definitions, and every concrete arrangement and cardinality count is correct. The findings below are almost entirely about accreted prose and redundant re-derivation, consistent with the `review-mode.anti-bloat` classifier. None of the math is wrong; the document is roughly twice the length its reasoning requires.

## REVISE

### Issue 1: Per-invariant discharge re-proves a foundation theorem
**ASN-0091, "Per-Invariant Discharges (ASN-0036 Foundation Invariants)" and "(ASN-0047 Extended Invariants)"**: the ASN names K.μ~ as the realiser in the non-trivial case, yet then re-derives S0, S1, S2, S4, S5, S7, S7a/b/d, S8a, S8-fin, S8-depth, M0, M1, D-CTG★, D-MIN★, D-SEQ★, S3★, S3★-aux, CL-OWN, CL-UNIQ, P4★, S8★ individually at Σ'.
**Problem**: ASN-0047's ExtendedReachableStateInvariants already establishes that every valid composite (K.μ~ is one) preserves exactly this per-state invariant package. Re-discharging each invariant from scratch duplicates a verified foundation result and is the bulk of the section's length. This is the "re-prove what the foundation already gives" form of drift.
**Required**: For the non-trivial (K.μ~) case, discharge RA-adm by citing ASN-0047's ExtendedReachableStateInvariants for K.μ~; retain only the genuinely ASN-specific arguments (the abstract S2 derivation, RE-subpres, and the RA-dom-via-ASN-0084 independence claim). Keep a per-invariant discharge only for the parts that do *not* route through K.μ~ (the collapse/identity case is already trivial).

### Issue 2: Frame-inherited invariants enumerated twice
**ASN-0091, "Per-Invariant Discharges (ASN-0036 Foundation Invariants)"**: S0, S1, S4, S7, S7a, S7b, S7d, M0, M1 each receive a one-line "preserved by RA-frame's `Σ'.C = Σ.C` / state-independent structural projection" clause.
**Problem**: The later "State-Component-Only Invariants" section already disposes of ~25 invariants by exactly this mechanism in a single sentence ("RA-frame fixes each of these components verbatim"). Listing the frame-inherited ASN-0036 invariants separately, line by line, is inventory bloat duplicating that one paragraph.
**Required**: Fold the frame-inherited invariants into the single state-component-only sentence; keep individual treatment only for S2, S8a, S8-fin, S8-depth (the arrangement-structural ones that need RA-dom).

### Issue 3: "What Rearrangement Is Not" restates every claim a third time
**ASN-0091, "What Rearrangement Is Not"**: each RE-* claim is restated as a negation ("does not modify the content store (RE-C); does not modify the link store (RE-L); …").
**Problem**: Every RE-* claim is already (a) derived in prose and (b) tabulated with provenance in "Claims Introduced". This negation list advances no reasoning — it is a third statement of the same content the reader must skip past. The Nelson framing it carries is already present at each derivation site.
**Required**: Delete the section, or reduce to a single sentence pointing at the table.

### Issue 4: Worked examples re-discharge admissibility redundantly
**ASN-0091, four "Worked Example" sections**: each closes with an "Admissibility (RA-adm)" paragraph. The 4-cut example states "by the same per-invariant package verified in detail in the first Worked Example" and then re-verifies S3★, S8★, P4★ anyway; the interior-cut and bijection examples do likewise.
**Problem**: The repeated per-invariant verification is the "two paragraphs say the same thing in different words" pattern at scale. Once the first example exhibits the full package, subsequent examples need only the clauses whose witness genuinely differs (e.g., the μ-region run in the 4-cut case, the shared-I-address S5/S2/S8★ behaviour in the bijection case).
**Required**: In examples 2–4, cite the first example's discharge for unchanged clauses and show only the structurally distinctive clause(s). Do not re-list the per-invariant package each time.

### Issue 5: Bijection non-uniqueness is expounded twice
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "This is the standard fact that a bijection of the finite set `dom(Σ.M(d))` … respects its partition into arrangement pre-image fibers — necessity (π restricts to each block) and sufficiency (assemble π from free per-block bijections) both hold, with the within-block assignment unconstrained."
**Problem**: This abstract necessity/sufficiency essay is then realised concretely in full by the dedicated "Worked Example — Bijection Non-Uniqueness Under Shared I-Addresses" (π₁, π₂, RE-proj uniformity). The opening prose duplicates the worked example's payoff; the "standard fact … necessity … sufficiency" elaboration is the bloat.
**Required**: Reduce the opening to the one-sentence statement that shared I-addresses make π non-unique, with the within-block freedom; let the worked example carry the detail.

### Issue 6: Navigation / forward-pointer meta-prose
**ASN-0091, multiple sites**: e.g. "We separate these layers below — first the clause-by-clause realisation argument, then the per-invariant discharges grouped by ASN of origin … Each subsection isolates a single thematic concern."; "RE-sub is one of two REARRANGE_K-specific consequences in this ASN that do not flow from the abstract class alone; the other, RE-ext, is introduced in the next section and complements RE-sub …"; "We will examine the consequences for the link subspace as a separate frame property (RE-sub) below, and the consequences for the cut-subspace exterior as a complementary frame property (RE-ext)."
**Problem**: These sentences describe the document's own structure and announce where things appear, rather than advancing the argument — exactly the forward-reference/organizational meta-prose the anti-bloat pass targets. The "Subspace and Affected-Range Restrictions" subsection is essentially entirely such announcement.
**Required**: Remove the structural-announcement sentences; let each claim be stated where it is proved.

### Issue 7: P4a append-only essay re-explains the axiom
**ASN-0091, "P4a Handling"**: "The append-only corollary unfolds as follows. SequentialTransitionAxiom declares each transition `Σ_k → Σ_{k+1}` atomic, uninterruptible, and totally ordered … each `Σ_k` is the input to the (k+1)-th transition … admits no transition mechanism that re-writes any earlier `Σ_k` … So the prior states `Σ_0, ..., Σ_n` are concrete tuples …"
**Problem**: A paragraph-length unpacking of why an atomicity axiom yields trace append-only, for a one-line consequence ("the trace is append-only, so prior witnesses persist"). This is the "new prose around an axiom explaining why it is needed rather than using it" pattern.
**Required**: Compress to the single sentence: by SequentialTransitionAxiom the trace is append-only, so any pre-existing witness `Σ_k` for `(a,d) ∈ Σ.R` survives, and RE-R preserves `(a,d) ∈ Σ'.R`.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: Open Question 2 ("What semantics … should rearrangement carry on the link subspace") is correctly deferred — REARRANGE_K fixes S = s_C by CS3, and a link-subspace reordering operation is a separate future ASN, not a gap here.

### Topic 2: Split-then-transclude span handling and reachability-equivalence
**Why out of scope**: Open Questions 1 and 3 (cross-document transclusion of a split span; observational equivalence at the discoverability level) are genuinely new territory building on RE-proj/RE-disc, appropriately listed as future work.

### Topic 3: Run-cardinality bound and rearrangement completeness
**Why out of scope**: Open Questions 4 and 5 (upper bound on run-cardinality increase; whether every well-formedness-preserving bijection is a finite composition of cut-sequence rearrangements) are extensions, not defects in the present claims.

META: not warranted — the ASN defines a real operation with state-transition semantics and system-level invariants; it is over-elaborated, not off-track.

VERDICT: REVISE
