# Review of ASN-0043

I checked the foundational derivations (PrefixSpanCoverage, CPP, the two-invocation L1c postcondition proof), the conformance machinery (FSP, FSE), the existence lemmas (L9, L11b), and recomputed every tumbler in the worked example. The mathematics is sound throughout, and the prior substantive concerns are addressed in the declined-findings record. I record below the items I examined for the standard checks and the anti-bloat mandate, none of which rose to a REVISE.

## Items examined, no defect found

- **PrefixSpanCoverage** — both inclusions verified, including the `k = m` boundary sub-case where `t_m = shift(x,1)_m` forces the prefix/proper-extension split. Action-point boundary `actionPoint(δ(1,#x)) = #x ≤ #x` holds at equality. Sound.
- **CPP and the two L1c invocations** — the second invocation on the post-seed sub-chain `t₁,…,tₙ` with `p = #s+1` correctly pins `a_{#s+1} = 0`; the `#E(a) ≥ 2` argument that the third zero is non-terminal (`#s+1 ≤ #a−2 < #a`) is correct. The "first invocation says nothing about `#s+1`" sentence is genuine motivation for the second invocation, not skippable meta-prose.
- **FSP bullets** — every state-local L- and S-invariant is discharged; S0–S3, S7a/b/d, S8-* fall through `Σ'.C = Σ.C` / `Σ'.M = Σ.M`. L14a correctly routes through S3 + L1d(b) under `s_C`-residence.
- **L9 Case A/B** — the producer chain `inc(d,2) → sweep → inc(·,1)` lands `a` in subspace `s_L` with `#E(a) = 2`; freshness follows from the per-`d` link-allocation split (covers the empty-link-store boundary). FSE guarantees a fresh sibling always exists (infinite enumeration, finite store).
- **Worked example** — all tumbler arithmetic recomputed (`inc(d,2)=1.0.1.0.1.0.1`, the subspace sweep, `g ⊕ δ(2,8) = h`, the `[g,g') ∪ [g',h) = [g,h)` adjacency in Step 6). Steps 1–6 exercise L5 (≥2-span), L8 (match/discriminate/coverage-vs-decomposition), L11b, L13 non-vacuously.

## Anti-bloat patterns checked

- The FSP/FSE factoring genuinely *removes* duplication: L9 and L11b apply it cleanly rather than re-proving preservation. This is good structure, not accretion.
- L4(a–c), L7's citation/counterpart/heading examples, and the "Gregory confirms…" lines are illustration and implementation evidence — permitted per the meta-prose exclusion (statements of what the structure does/does not constrain).
- No forward-reference-justification prose, no document-ordering apologetics, and no paragraph that imagines a precondition-excluded case were found. References to ASN-0034 and ASN-0036 are all to foundation ASNs (Standard 7 satisfied — ASN-0036 appears under the Foundation heading).

## OUT_OF_SCOPE

No misplaced claims. The Open Questions correctly defer transclusion/link-store consistency, compound-link well-formedness, allocation ordering, and the global content-subspace constant to future ASNs rather than asserting them here.

VERDICT: CONVERGED
