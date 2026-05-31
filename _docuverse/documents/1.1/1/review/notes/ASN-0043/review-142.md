# Review of ASN-0043

I worked through the core proofs (CPP, FSP, FSE, L9, L11a, PrefixSpanCoverage) and the arithmetic of the worked example and its six extension steps. The chain derivations, coverage computations, and invariant-preservation arguments check out. One gap remains in the verification artifact itself.

## REVISE

### Issue 1: The worked example omits two state-local invariants it claims to verify

**ASN-0043, "Worked Example"**: "We construct a minimal conforming state to verify that L0–L14 hold simultaneously." The example then checks S3, S7a, S7b, S7d, S8a, S8-depth, D-CTG, and D-SEQ for the constructed state `Σ`.

**Problem**: *A Shared Conformance Lemma* enumerates the state-local invariants a conforming state must satisfy, explicitly including **S8-fin** and **D-MIN** (and **S2**). The worked example verifies most of the S-side invariants but never addresses these. D-MIN is not idle here: the D-SEQ check leans on it — "*starting at the D-MIN witness `[1,1]`*" — yet D-MIN (`V_1(d) ≠ ∅ ⟹ min(V_1(d)) = [1,1,...,1]`) is asserted by use rather than verified. For a state advertised as demonstrating that *all* invariants hold simultaneously, two listed conjuncts are silently skipped. Both are trivial to discharge (`min(V_1(d)) = [1,1]` of length 2; `|dom(Σ.M(d))| = 2 < ∞`), which is precisely why their omission reads as oversight rather than difficulty — and "every invariant conjunct addressed" includes the easy ones when the example's stated purpose is simultaneous conformance.

**Required**: Add explicit D-MIN and S8-fin checks (and an S2 single-image note) to the worked example's verification list, so the "conforming state" demonstration covers the full state-local set named in the conformance lemma.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
