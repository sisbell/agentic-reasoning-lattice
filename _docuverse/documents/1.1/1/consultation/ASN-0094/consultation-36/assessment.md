# Channel Assignment — ASN-0094 review-36

**Date:** 2026-05-23 19:53

## Issue 1: NAT-card termination measure cites the wrong axiom
Reason: Pure proof-technique correction — the reviewer has provided the correct approach (strong induction on an external bound `n` with `S ⊆ {0, ..., n}`, justified via NAT-wellorder). The fix uses only NAT axioms already cited in the ASN; no design or implementation input is needed.

## Issue 2: Walkthroughs introduce K's after `Σ_init` without discharging the lifetime-constancy escape clause
Reason: Mechanical fix — the Comment walkthrough already exhibits the required pattern ("Registered catalog for this walkthrough" preamble); the remaining walkthroughs need the same preamble added. Derivable entirely from the ASN's own conventions.

## Issue 3: SHCD's "Coverage and Comment both use `idem = ⊥` but for different reasons" justification is informal
Reason: This is a design-intent question about whether the relational vocabulary structurally distinguishes Coverage-like ordered relations from Comment-like event relations. Nelson can inform whether this distinction was a designed semantic axis; Gregory is unlikely to help since udanax-green's relational model is unlikely to surface this abstract framework-level distinction.
Nelson question: In Nelson's design vocabulary, are coverage-style relations (where later assertions supersede earlier ones) and comment-style relations (where each emission is a distinct event) meant to be structurally distinct kinds of links, or are they the same kind of link with different layer-level reading conventions?
