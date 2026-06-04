# Review of ASN-0091

This note is mathematically sound — I checked the collapse-case witness, the fragmentation/coalescence/equality witnesses, and the four worked-example traces against the foundation contracts, and the arithmetic and case analysis hold. The problems are structural: the note carries the `review-mode.anti-bloat` classifier, and across cycles it has accreted heavy meta-prose and redundant verification around its forward references. The findings below target that accretion.

## REVISE

### Issue 1: Bijection-non-uniqueness exposition duplicated across four locations
**ASN-0091, "REARRANGE as Vstream-Only Operation" / "Where Position Lives After Rearrangement" / RE-proj / "Worked Example — Bijection Non-Uniqueness"**: The same fact — π is not unique when `Σ.M(d)` shares I-addresses, and RE-proj's set image is nonetheless witness-invariant — is stated in the opening definition ("The bijection π is not in general unique: when Σ.M(d) has shared I-addresses..."), restated in "Where Position Lives" ("π is not in general unique when Σ.M(d) carries shared I-addresses, per the bijection-class characterisation in the ... section above"), re-derived in the RE-proj "well-defined across the freedom in choosing π" paragraph, and then given an entire worked example.
**Problem**: Two-plus paragraphs say the same thing in different words, with cross-references deferring back to the same upstream location. This is exactly the duplication/deferral pattern the anti-bloat classifier targets.
**Required**: State the non-uniqueness once at the definition, prove the RE-proj set-image invariance once (either inline at RE-proj or in the dedicated example, not both), and delete the back-references in "Where Position Lives."

### Issue 2: Worked Example 2 re-verifies the full RE-* list it admits is identical
**ASN-0091, "Worked Example — 4-cut Swap"**: "The routine claims — RE-C, RE-L, RE-dom, RE-ran, RE-μ, RE-cov, RE-disc, RE-other, RE-sub, RE-origin, and RE-R — discharge exactly as in the first Worked Example."
**Problem**: The example then re-runs verification prose for those routine claims despite stating they are identical; only the μ-region deltas (RE-proj, RE-frag, RE-trans, S8★) are genuinely new. Re-running an entire verification when one mechanism differs is use-site re-inventory.
**Required**: Keep only the μ-region-specific deltas and the one structurally distinctive admissibility clause (S8★); drop the verbatim re-verification of the routine claims, citing the first example for them.

### Issue 3: RA-adm defined by what it is not
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "It is a per-state-invariant-preservation clause, not a blanket 'all foundation results' constraint." and the surrounding "RA-adm ranges over the *per-state* foundation invariants only — those that are state predicates evaluable at a single state, so that 'satisfied by Σ' and 'satisfied by Σ'' each carry state-relative content."
**Problem**: Defensive justification explaining what the clause excludes and why, rather than stating what it requires. The negative framing ("not a blanket constraint") is reviser drift — it answers an objection rather than advancing the definition.
**Required**: State positively that RA-adm requires Σ' to satisfy each per-state foundation invariant; drop the "not a blanket constraint" gloss and the meta-explanation of why "satisfied by Σ'" is well-typed.

### Issue 4: non-trivial/collapse case split stated, then restated downstream
**ASN-0091, "REARRANGE as Vstream-Only Operation" (S5 witness + two bullets) and "REARRANGE_K Realises the Abstract Class"**: The collapse/non-trivial split is built up with the S5 witness and a two-bullet case analysis, then re-narrated at the realisation section ("its domain splits across the two cases isolated above, and the realiser is not uniform over that domain...").
**Problem**: The second statement is prior content relocated rather than removed; the realisation section re-explains the same split it defers to ("the two cases isolated above"). The S5 witness plus two-bullet treatment is also over-elaborated for a point whose payload is one sentence (REARRANGE_K carries no non-triviality precondition, so a value-fixed range yields Σ'=Σ).
**Required**: Establish the split once at the abstract level; at the realisation section, state the realiser per case in one sentence each without re-deriving the split.

### Issue 5: P4a discharged once, then deferred to from three places
**ASN-0091, "P4a Handling" subsection, plus both single-step worked examples**: P4a gets a dedicated subsection, after which Worked Example 1 ("P4a ... is discharged by the canonical derivation given in the 'P4a Handling' subsection") and Worked Example 2 ("discharge exactly as in the first Worked Example") both point back to it.
**Problem**: Multiple paragraphs deferring to the same downstream/upstream location — the catalogued forward-reference accretion pattern.
**Required**: Discharge P4a once; in the examples, cite the label `P4a` without re-narrating that it is "discharged by the canonical derivation in the subsection above."

### Issue 6: Admissibility obligations walked three times
**ASN-0091, "REARRANGE_K Realises the Abstract Class"**: The admissibility content is traversed by (a) the "K.μ~ Admissibility Clauses" reverse mapping (RA-* ← K.μ~ definitional clauses), (b) the "Forward Direction" subsection re-walking clauses (i)–(v), and (c) the "Per-Invariant Discharges" three-layer structure — with clause (i) of the forward direction explicitly forward-referencing "the constructive shape-package layer of the per-invariant discharges below."
**Problem**: Three structures circle the same admissibility obligations, with internal cross-pointers ("discharged by ... below") binding them. The shape-package invariants (S8a, S8-depth, D-CTG★, D-MIN★) are named as consumed by clause (i), then re-derived in the per-invariant layer — a use-site inventory plus a deferral to the layer that actually does the work.
**Required**: Collapse to a single pass: state the per-invariant discharge layers, and let the forward/reverse clause correspondences be a short table rather than two re-narrated walks.

### Issue 7: Worked Example 4's bijection-non-uniqueness content overlaps Issue 1
**ASN-0091, "Worked Example — Bijection Non-Uniqueness Under Shared I-Addresses"**: Constructs π₁ and π₂, verifies RA-π for each, and re-argues "the set image is invariant under the within-block freedom" — content already asserted abstractly in the RE-proj uniformity paragraph.
**Problem**: The example is valuable as the single concrete realisation but duplicates the abstract uniformity argument it should merely instantiate; it also re-derives the `coverage(e_a) ∩ stores = {a}` LP-Fin computation already performed identically in Worked Example 1.
**Required**: Make this example the *sole* site of the uniformity argument (per Issue 1) and have it cite — not re-derive — the LP-Fin Corollary computation pattern established in Worked Example 1.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The Open Questions section already frames "what semantics, if any, should rearrangement carry on the link subspace" as future work. RE-sub correctly scopes the present note to content-subspace cuts; link-subspace reordering is a distinct future operation, not a gap here.

### Topic 2: Upper bound on run-cardinality increase per invocation
**Why out of scope**: RE-frag establishes increase is possible; bounding it is posed as an open question and belongs to a future quantitative ASN, not this one.

VERDICT: REVISE
