I read the foundation contracts, then worked the ASN as a system: tracing the precondition chains from the displacement lemmas (D0/D1/D2, TA-assoc, TA-LC) through WF/WR into the span/span-set algebra (S0–S11d), and checking that "level-uniform," "well-formed span," and "level-compatible" hold one meaning throughout.

The core logic is sound. The displacement round-trip chain (WF → S1/S3/S4/S8/S11), the split/merge inverses (S4a/S3b), the normalization existence/uniqueness pair (S8/S9), and the difference case taxonomy (S11/S11a–d against SC) all walk their cases and discharge their cited preconditions correctly. The equal-length exclusion of T1 case (ii) is applied consistently, and the SC five-case split is genuinely exhaustive and aligned with the S11d table. The findings below are about noise and contract hygiene introduced in revision, not correctness.

### Redundant carrier-membership re-derivations assert a non-obligation
**Class**: OBSERVE
**Foundation**: Span (preconditions license `s ⊕ ℓ ∈ T` via TA0); TumblerAdd (`a ⊕ w ∈ T`)
**ASN**: S1 ("the reach endpoint r' = min(reach(α), reach(β)) is not [in T directly] ... carrier-membership of a sum is not immediate"), with the same paragraph reproduced in S3, S4, S8, S11, and S11c Case 2.
**Issue**: For any well-formed span σ, `reach(σ) = start(σ) ⊕ width(σ) ∈ T` is immediate — it is precisely the postcondition TA0 supplies as part of σ being a span (the Span definition assumes `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` and "TA0 licenses `s ⊕ ℓ ∈ T`"). The repeated "this is not immediate, we discharge it as S11 does" paragraphs re-prove what well-formedness already grants, and the phrase "not immediate" actively misstates the situation. This is a use-site inventory / defensive justification duplicated across six claims that the reader must skip past to follow each proof.
**What needs resolving**: N/A (OBSERVE).

### WR lists derived facts as preconditions
**Class**: OBSERVE
**Foundation**: D2, T12, TA-strict, TA0, T1, Divergence
**ASN**: WR formal contract — *Preconditions:* "ℓ > 0 with action point k ≤ #s (T12); s < reach(σ) (TA-strict on T12); ... divergence(s, reach(σ)) = k ≤ #s of type (i) (T1, Divergence)."
**Issue**: The only genuine caller obligation is "σ is a well-formed level-uniform span." Everything else listed — `s < reach(σ)`, `divergence(s, reach(σ)) ≤ #s` of type (i), the TA0 length facts — is *derived inside WR's own proof* and parenthetically attributed to the lemmas that establish it. Listing proof obligations the claim discharges itself as if they were caller-supplied preconditions conflates the contract's two halves; a downstream consumer reading the contract would think it must independently establish divergence type before invoking WR.
**What needs resolving**: N/A (OBSERVE).

### WR reproduces WF's divergence argument inline while citing WF as a navigation pointer
**Class**: OBSERVE
**Foundation**: WF, Divergence, T1
**ASN**: WR proof ("The fifth, divergence(s, reach(σ)) ≤ #s, we establish exactly as WF does, instantiated at (s, reach(σ))" followed by a full re-derivation), with the Forward Reference to WF labeled "cited as a navigation pointer."
**Issue**: WR both says it argues "exactly as WF does" and then transcribes the entire equal-length / case-(ii)-exclusion / Divergence-uniqueness argument verbatim against `(s, reach(σ))`. Either the inline copy or the "navigation pointer" reference is superfluous; the duplication is the kind of essay content that compounds across cycles.
**What needs resolving**: N/A (OBSERVE).

### Defensive type-commentary in structural slots (S2, S7)
**Class**: OBSERVE
**Foundation**: T12, Span; T0 (comprehension), T0(b)
**ASN**: S2 prose ("This second condition is a comparison of natural numbers ... not of the end offset s ⊕ ℓ, which is a tumbler"); S7 parenthetical ("The separate UnboundedLength claim T0(b), being purely existential about length, is not invoked here").
**Issue**: Both are defensive notes explaining why a particular reading is *not* intended or which axiom is *not* used — reviser-drift prose that argues against a misreading rather than advancing the claim. S7's parenthetical in particular explains why T0(b) is the wrong citation, which is meta-commentary on a prior framing, not part of the covering/infinitude argument.
**What needs resolving**: N/A (OBSERVE).

VERDICT: OBSERVE