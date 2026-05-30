# Channel Assignment — ASN-0042 review-103

**Date:** 2026-05-30 03:07

## Issue 1: Notation-justification prose in the `delegated` definition does not advance the definition
Reason: Purely editorial — the fix collapses meta-prose about evaluation-state semantics into a one-clause convention. Nothing here depends on design intent or implementation; the convention is already fixed by the ASN's own O13/O15 references.

## Issue 2: `acct(a)` well-formedness duplicates FieldStructure
Reason: Internal deduplication — state the case definition once in the Formal Contract and cite FieldStructure. Both the definition and the lemma already exist in the ASN; no external input needed.

## Issue 3: Freshness-(v) is restated at every consumer rather than cited
Reason: Internal — Freshness-(v) is already a named derived lemma in the ASN; replacing paraphrases with bare citations is a mechanical edit requiring no design or implementation evidence.

## Issue 4: Essay paragraphs occupy argument slots without advancing reasoning
Reason: Internal — these paragraphs restate already-proved O3/O8/O12/O13/B0 results in prose; deletion (or folding into a contract) is derivable from what the ASN already proves, with no new claim requiring Nelson or Gregory.

## Issue 5: O1a is invoked before it is proved, and `Π` is used unqualified in a state-relativized contract
Reason: Internal — writing `π ∈ Π_Σ` in O9 and signposting that O1a's induction lives in *Delegation* are notational/cross-reference fixes fully determined by the ASN's existing structure.

## Issue 6: Worked example applies single-transition lemmas across milestone arrows
Reason: Internal — whether `Σ₀ → Σ₁` is a single delegation edge (vs. invoking the multi-step corollary) is a choice within the author's own worked example, resolvable against the ASN's own O3 and OwnershipDomainPermanence★ statements.
