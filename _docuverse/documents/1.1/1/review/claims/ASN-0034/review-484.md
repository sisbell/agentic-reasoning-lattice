# Regional Review — ASN-0034/ActionPoint (cycle 3)

*2026-04-24 03:41*

### NAT-discrete and NAT-wellorder prose justifies the Depends slot itself
**Class**: REVISE
**Foundation**: (internal)
**ASN**: NAT-discrete, paragraph ending "Both are declared in the Depends slot so that the axiom body can be read without silently importing foundations."; NAT-wellorder, sentence "NAT-order is therefore declared in the Depends slot so that the axiom body can be read without silently importing the definition."
**Issue**: Both paragraphs execute the same move: name a symbol the axiom uses, name the dependency that supplies it, then add a clause explaining that the dependency is listed in the Depends slot so the reader won't silently import foundations. That last clause is self-reference to the structural slot — it explains *why* a Depends entry exists rather than *what* the axiom says. The `≤`/`+` discussions themselves are legitimate exegesis, but the "declared in the Depends slot so that…" tail is defensive structural justification of the kind the reviewer instruction names as reviser drift ("new prose around an axiom explains why the axiom is needed rather than what it says"). The two occurrences also establish the pattern — leaving them in invites future axioms to acquire the same paragraph.
**What needs resolving**: Trim the "declared in the Depends slot so that…" clauses from both paragraphs. The factual content — that `≤` unfolds via NAT-order's definition, that `m + 1` needs NAT-closure — can stand without the structural self-reference; alternatively, fold those facts into the Depends bullets themselves where they already appear.

### NAT-wellorder note on set-theoretic primitives is pure negative justification
**Class**: REVISE
**Foundation**: (internal)
**ASN**: NAT-wellorder, sentence "The set-theoretic primitives `⊆`, `∈`, and `≠ ∅` carry their standard first-order meaning (subset, membership, nonemptiness) in the ambient register shared across the ASN; they are not axiomatized by any NAT dependency and no NAT axiom is cited to ground them."
**Issue**: This sentence exists solely to explain why certain symbols are *not* cited in Depends. No other axiom in the ASN carries such a disclaimer — T0, TA-Pos, and ActionPoint all use `∈`, `⊆`-flavored set-builder notation, and `≠` without a paragraph justifying their absence from Depends. This is defensive justification (the reviewer instruction's "essay content in structural slots" / "defensive justifications") and is asymmetric with the rest of the ASN. If the ambient register is genuinely shared, it should be stated once at the ASN level (if at all) rather than re-asserted at one claim.
**What needs resolving**: Remove the sentence. If a convention about ambient set-theoretic primitives is considered necessary, state it once at the ASN level and drop the per-claim repetition.

VERDICT: REVISE
