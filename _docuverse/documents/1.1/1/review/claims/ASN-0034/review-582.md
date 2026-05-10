# Cone Review — ASN-0034/TA-assoc (cycle 1)

*2026-04-26 00:38*

### Defensive justification meta-prose in NAT-sub Consequence framing
**Class**: OBSERVE
**Foundation**: n/a (foundation ASN; internal)
**ASN**: NAT-sub. Two paragraphs frame *why* strict monotonicity and strict positivity are exported as Consequences rather than axiom clauses: "Strict monotonicity ... is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from..." and "Strict positivity ... is exported as a *Consequence:* rather than an additional axiom clause, because its content is not purely subtractive..."
**Issue**: These passages explain a structural choice (Consequence vs axiom) rather than advance the mathematical claim. They're defensive justification for the chosen layout — the kind of meta-prose the precise reader must skip past to reach the actual derivation. The derivations themselves are sound; the framing prose adds no claim content.

### Use-site inventory in NAT-sub
**Class**: OBSERVE
**ASN**: NAT-sub. The paragraph beginning "The axiom body invokes symbols beyond ℕ's primitive membership..." walks through each appearing symbol (`<`, `≤`, `≥`, `>`, `+`) and names the dependency that licenses it, then re-states which Consequence cites which clause from where.
**Issue**: This is a use-site inventory explicitly flagged by the review prompt as noise. The Depends slot already encodes the same information in structured form; the prose duplicates it without adding reasoning.

### Defensive justification in NAT-addassoc
**Class**: OBSERVE
**ASN**: NAT-addassoc. The paragraph "Two primitives appear in the axiom that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause...A single Depends entry on NAT-closure therefore suffices: it grounds `+` directly and `ℕ` transitively, matching the precedent NAT-closure itself sets..."
**Issue**: This explains why the Depends list is minimal rather than what the axiom says. Defensive justification for a structural choice; the associativity axiom needs no such defense.

### TA-assoc placed under "What tumbler arithmetic is NOT"
**Class**: OBSERVE
**ASN**: TA-assoc sits inside the section headed "What tumbler arithmetic is NOT", which otherwise contains the negative remarks (no group, not commutative, no multiplication, differences are not counts). TA-assoc is positive content — addition *is* associative on its domain — and reads as misfiled.
**Issue**: A reader scanning section structure for properties would not find associativity here. The placement obscures rather than advances the argument; the proof itself is sound.

### Reverse-companion abbreviation prose in T1
**Class**: OBSERVE
**ASN**: T1 closes with "The strict total order `<` admits the customary non-strict companions: `a ≤ b` abbreviates `a < b ∨ a = b`, and `a ≥ b` abbreviates `b ≤ a`." The same content also appears in the *Abbreviations* line of the Formal Contract.
**Issue**: Duplicate of the structured contract entry; minor noise. Soundness unaffected.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 573s*
