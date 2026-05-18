# Review of ASN-0051

This is a long, carefully constructed note. The core machinery (π, locate, discover_s, vitality predicates) is well-defined, and the major proofs (SV5, SV6, SV7, SV9, SV11) work through their case analyses with explicit witnesses. I went through the SV6 sandwich argument, the W(m, p) attainment witnesses, and the disjoint-pair non-attainment proof in detail; all are sound. I found two real but minor issues.

## REVISE

### Issue 1: K.μ~ called "elementary step" in SV14(d) witness
**ASN-0051, SV14(d) witness, third paragraph**: "the Worked Example's after-removing-a₃ composite proceeds in two elementary steps — Step 1, K.μ~, and Step 2, K.μ⁻"

**Problem**: K.μ~ is a *distinguished composite* of K.μ⁻ + K.μ⁺ per ASN-0047, not an elementary step. The Worked Example itself (preceding section) explicitly states "the underlying elementary chain is K.μ⁻ + K.μ⁺ + K.μ⁻, since K.μ~ is itself the distinguished K.μ⁻ + K.μ⁺ composite (ASN-0047)." SV13(e)'s K.μ~ bullet also identifies K.μ~ as "not an elementary transition". The "two elementary steps" phrasing contradicts both.

**Required**: Change to "two transition stages" or "two consecutive operations" — the intent is clear, but the terminology should be consistent across the document.

### Issue 2: Origin function citation imprecision in SV6 proof
**ASN-0051, SV6 proof, "T4-validity of t" subsection**: "The origin function `origin(t) = N(t).0.U(t).0.D(t)` (ASN-0036, S7) presupposes that t is T4-valid"

**Problem**: ASN-0036 S7 explicitly states "For every `a ∈ dom(Σ.C)`, define the *origin*..." — the definition is scoped to dom(Σ.C). The SV6 proof applies origin to arbitrary T4-valid element-level tumblers t ∈ ⟦(s, ℓ)⟧, which need not be in dom(Σ.C) (e.g., child-depth tumblers, unallocated siblings). The underlying projections N, U, D are defined via T4b (UniqueParse, ASN-0034) for any T4-valid element-level tumbler regardless of allocation status, so origin extends naturally — but the citation is technically misaligned with S7's stated domain.

**Required**: Either (a) cite T4b's N, U, D projections directly as the source of origin's structural definition, or (b) add a one-line remark that `origin = N.0.U.0.D` extends to any T4-valid element-level tumbler via T4b's projections (with S7's dom(C) scoping being a downstream specialisation, not a constraint on the structural function).

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
