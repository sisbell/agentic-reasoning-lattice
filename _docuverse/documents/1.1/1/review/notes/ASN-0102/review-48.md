# Review of ASN-0102

## REVISE

### Issue 1: The "standalone composite" restriction on COPY is stipulated without justification, yet the entire coupling discharge depends on it

**ASN-0102, Definition / "Amendment to `ValidComposite★`"**: "COPY is added to `ValidComposite★`'s atomic vocabulary (ASN-0047) as a new transition kind, admissible only as a length-1 (standalone) composite."

**Problem**: The restriction is internally tense and undefended. ValidComposite★'s atomic vocabulary is precisely the set of building blocks for *multi-step* composites; K.α, K.μ⁺, K.μ⁻, K.μ~ all compose freely. Adding COPY to that vocabulary but barring it from any composite of length > 1 is asserted with no rationale. The restriction is load-bearing, not cosmetic:

- X14 discharges J0/J1★/J1'★ and P4★/P7/P7a by evaluating the couplings *immediately around the single COPY step* (`Σ → Σ'`). If COPY appeared mid-composite, ASN-0047 evaluates couplings only between the composite's initial and final states, and the X14 derivation would not directly apply.
- J1'★ branch (b) and P7a both invoke P4★/P7a *at the pre-state `Σ`*, which requires `Σ` to be a composite boundary — a status that holds only because the preceding composite ended there, i.e. it again rests on the standalone rule.

Moreover the restriction looks *unnecessary* on the ASN's own terms: COPY records its own provenance and discharges its couplings around itself, making it self-sufficient in exactly the sense ASN-0047 attributes to K.μ⁻ (J2) and K.μ~ (J3) — both of which *do* compose. A self-sufficient operation that nonetheless may never compose is a surprising and strong limitation.

**Required**: Either (a) justify why COPY must be standalone (a genuine system constraint, with the consequence that e.g. a COPY-then-DELETE cannot be a single composite, stated explicitly), or (b) drop the restriction and rework X14's coupling/P4★/P7a discharges to hold when COPY participates in a longer valid composite (couplings evaluated initial-to-final). As written, a key admissibility clause of the operation is underived.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
