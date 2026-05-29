# Review of ASN-0036

This ASN carries `review-mode.anti-bloat`. The formal content is largely sound — proofs check out (S8's singleton decomposition, the within-subspace incompatibility lemma, D-CTG-depth's infinite-intermediate construction, OrdAddHom). The findings below are mostly accreted meta-prose, plus one genuine consistency defect.

## REVISE

### Issue 1: S8a dependency contradiction between proof and table
**ASN-0036, S8a proof vs. Properties Introduced table**: The proof states the conjuncts "follow from this element-field commitment together with T0's ℕ-valued carrier, **without appeal to T4's field-segment constraint**," and the S8a Formal Contract `Depends` lists only T0 and NAT-discrete. But the Properties Introduced table row reads "zero-count and positivity **derived from T4, T0**."
**Problem**: The table credits T4 for a derivation the proof explicitly disclaims. A reader tracing dependencies gets contradictory answers.
**Required**: Make the table consistent with the proof — remove T4 from the S8a derivation citation (or, if T4 is genuinely needed, fix the proof and contract `Depends`).

### Issue 2: "axiomatic state component, not a derived property" rationale paragraphs
**ASN-0036, Σ.C and Σ.M(d) sections**: e.g. "Σ.C is an axiomatic state component, not a derived property. Nelson's architecture requires a mechanism that associates content values... It is partial because... It maps to `Val` rather than to a specific type because..."
**Problem**: This is "why the axiom is needed / what kind of thing it is" essay prose in the slot before the Formal Contract — the flagged pattern. The Axiom and Definitions that follow already state the content; the paragraph explains motivation, not meaning. Both Σ.C and Σ.M(d) carry near-identical versions.
**Required**: Cut the rationale paragraphs; keep the Nelson quote and the Formal Contract.

### Issue 3: "Persistence independence" section is meta-commentary with no new content
**ASN-0036, Persistence independence**: "The formal property... is already supplied by S0... What remains to be stated is the *design commitment* that S0's formulation does not emphasize on its surface... This is a remark on what S0 forbids, not a separately-axiomatized property."
**Problem**: The section self-admits it introduces no formal property. It also imagines a case S0 already excludes ("A system could satisfy a weakened variant of S0 — one that permits removal of `a`... while preserving a conditional form") purely to re-argue that S0 rules it out — the flagged "paragraph imagines a case the claim's precondition already excludes" pattern. The orphan/dark-matter discussion repeats S3's frame remark.
**Required**: Collapse to one or two sentences noting S0 forbids reclamation, or fold the orphan observation into S3's frame and delete the section.

### Issue 4: subspace-identifier-as-structural-context restated repeatedly
**ASN-0036, S7c / S8-depth paragraph / w_ord / OrdinalDisplacementProjection**: The explanation "the subspace identifier is structural context outside the ordinal so that shifts act only within the subspace" (and its `w₁ = 0` / action-point-≥-2 mechanism) appears in S7c, the long S8-depth paragraph, the w_ord definition, and OrdAddHom part (b).
**Problem**: Two-paragraphs-say-the-same-thing, compounded four times. The mechanism is proved once (OrdAddHom part b); the prose restates it as motivation elsewhere.
**Required**: State the mechanism once (at OrdAddHom or w_ord) and reference it; strip the restatements.

### Issue 5: S8-depth explanatory paragraph re-derives proven facts inline
**ASN-0036, paragraph beginning "S8-depth allows us to define 'consecutive V-positions' precisely..."**: "A parallel uniformity holds for I-addresses... This follows directly from TumblerAdd... The uniformity is definitional... Subspace preservation follows separately..."
**Problem**: This inline-derives depth/prefix/subspace preservation that ShiftPreservation and OrdShiftHom prove formally below. Essay content duplicating a downstream proof. The trailing notational rule ("We reserve the symbol `+` for NAT addition... never as `v + k`") is housekeeping that belongs once, tersely.
**Required**: Reduce to the definition of consecutive positions plus a pointer to ShiftPreservation/OrdShiftHom; drop the re-derivation.

### Issue 6: essay flourish and archaeology in S1's proof region
**ASN-0036, S1**: "S0 and S1 are upheld not by architectural impossibility but by a design choice so consistent that four decades of continuous operation have never violated it."
**Problem**: Rhetorical flourish; "four decades" advances no reasoning. The `refcount` / `subtreefree`/`12/04/86` archaeology is borderline-acceptable evidence but is positioned as proof-adjacent narrative.
**Required**: Drop the flourish; keep at most one sentence of implementation evidence.

### Issue 7: repeated deferral of link-subspace to a future ASN
**ASN-0036, S8a Remark / Arrangement contiguity intro / Scope**: "link-subspace contiguity semantics are deferred to a future ASN"; "Subspace *alignment*... is deliberately not a strand-level invariant... posed as an Open Question below"; the S8a remark restates the same.
**Problem**: Multiple paragraphs in different sections defer to the same downstream location — the flagged pattern.
**Required**: Defer once (Scope or the contiguity intro); remove the duplicate deferrals.

### Issue 8: S8 "Corollary" restates ShiftPreservation
**ASN-0036, S8 Corollary (subspace and field-structure preservation)**: The corollary's three conclusions (i)–(iii) are ShiftPreservation's (i),(iii),(iv) re-stated for runs, then restated a third time in S8's Formal Contract postconditions.
**Problem**: The same preservation facts appear in the lemma, the corollary body, and the contract — three statements of one result.
**Required**: Let the corollary cite ShiftPreservation and state only the aggregation-over-`k`; don't re-enumerate the conclusions in both corollary and contract.

## OUT_OF_SCOPE

### Topic 1: whether DELETE/INSERT/COPY/REARRANGE preserve D-CTG and D-MIN
**Why out of scope**: Correctly identified by the ASN as a per-operation verification obligation (Open Question). The strand model defines the invariant abstractly; operation frame conditions belong to operation ASNs.

### Topic 2: subspace alignment `subspace(v) = subspace_I(M(d)(v))`
**Why out of scope**: The ASN explicitly leaves this as an operations-layer obligation, not a state invariant. That placement is defensible — alignment is established by operations, not by the arrangement-state axioms.

### Topic 3: subtraction homomorphism `ord(v ⊖ w) = ord(v) ⊖ w_ord` and round-trip
**Why out of scope**: Genuinely new territory (Open Questions), depending on TA7a's conditional subtraction results; not an omission in this ASN's addition-side treatment.

VERDICT: REVISE
