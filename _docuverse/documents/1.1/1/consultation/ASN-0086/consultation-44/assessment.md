# Channel Assignment — ASN-0086 review-44

**Date:** 2026-05-18 01:10

```
## Issue 1: Use-site inventory in Sparse-allocator hypothesis
Reason: Pure deletion of a *Consumers* enumeration paragraph. The hypothesis statement itself is unchanged; the fix is editorial.
```

```
## Issue 2: Discipline-conditionality flag restated 6+ times
Reason: Consolidate restatements into a single Setup location with cross-references at downstream sites. No external evidence needed — the conditionality fact is already established.
```

```
## Issue 3: R0a "Failure modes — necessity of the discipline" paragraph
Reason: Pure deletion of defensive justification. The conditional form of R0a stands on its own; no external consultation needed.
```

```
## Issue 4: "Modal note" on R5
Reason: Pure deletion of classification-defending prose. The LEMMA classification is supported by the proof structure itself.
```

```
## Issue 5: R6c Consequence (d) forward-reference accretion
Reason: Internal document-organization decision — either prove in R6's scope or defer entirely to R7. The content already exists at both sites; the fix is choosing one.
```

```
## Issue 6: Convention—RetractionDirectionality defensive paragraphs
Reason: Pure deletion of L4–L8 disclaimer and alternatives paragraph. The convention statement (to-set carries targets) is self-contained.
```

```
## Issue 7: "Why X is a caller parameter" rationale paragraphs
Reason: Pure deletion of design-rationale prose. The signatures carry the parameters; removing the rationale paragraphs requires no external verification.
```

```
## Issue 8: Allocator-naming convention restated
Reason: Pure deletion of duplicate annotation in Worked Sketch. The convention is stated once in Setup.
```

```
## Issue 9: R6b classified as LEMMA but is META about the Definition
Reason: Internal classification decision based on the ASN's own typology (LEMMA vs META). The proof content already establishes that R6b follows from the Definition's quantifier range; reclassification is structural.
```

```
## Issue 10: R5 Stage 2's exhaustiveness asserted, not enumerated
Reason: Requires enumerating L0–L14a + L-fin from ASN-0043 and tagging each invariant by whether it constrains endset content. ASN-0043 is internal project content, derivable by reading that ASN directly.
```

```
## Issue 11: R7 is largely tautological given Definition of relational layer
Reason: Internal restructure decision — fold R7 into the Definition as a derived corollary or rewrite to carry independent weight. No external evidence needed.
```

```
## Issue 12: R0a-Cor2 and Nullified definition forward-reference Open Questions
Reason: Pure deletion of forward pointers. The standalone statements of R0a-Cor2 and the Nullified scope are unchanged.
```

```
## Issue 13: Worked Sketch L-invariant verification list
Reason: Internal pruning — identify which L-invariant discharges depend on the concrete tumbler structure (e.g., L0's first-element check) versus those covered generically by R0's discharge. Derivable from R0's proof and the worked tumbler values.
```

```
## Issue 14: Sparse-allocator hypothesis cites Nelson and udanax-green inline
Reason: Positional relocation only — move the existing Nelson/udanax-green citations from the axiom body to a separate Implementation Notes remark. The citation content is already accepted; no re-verification needed.
```

```
## Issue 15: Setup section is the bloat epicenter
Reason: Internal restructure — separate structural foundation from implementation hypotheses and defer BroadExtension to R6c-Corollary's point of use. All constructs already exist; the fix is reorganization.
```
