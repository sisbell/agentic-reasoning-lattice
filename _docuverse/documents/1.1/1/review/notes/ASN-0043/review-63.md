# Review of ASN-0043

## REVISE

### Issue 1: Worked-example L1c verification has arithmetic errors

**ASN-0043, Worked Example, L1c verification**: "intermediate lengths are `#t₁ = #t₂ = 6 > 5 = #h(a)` and `#t₃ = #a = 7 > 5`"

**Problem**: The lengths are off by one throughout the chain. By TA5(d) at step (i) `inc(d, 2)`: `#t₁ = #d + 2 = 5 + 2 = 7`, not 6. By TA5(c) at step (ii) `inc(t₁, 0)`: `#t₂ = #t₁ = 7`. By TA5(d) at step (iii) `inc(t₂, 1)`: `#t₃ = #t₂ + 1 = 8 = #a`. Direct count of `a = 1.0.1.0.1.0.2.1` yields 8 components (positions 1=1, 2=0, 3=1, 4=0, 5=1, 6=0, 7=2, 8=1), which also matches the worked example's stated "depth 8" for all addresses used in the spans `δ(1, 8)`. The 6/7 numbers are internally inconsistent with the rest of the example.

**Required**: Replace `#t₁ = #t₂ = 6` with `#t₁ = #t₂ = 7`, and `#t₃ = #a = 7` with `#t₃ = #a = 8`. The chain's structural validity (every `#tᵢ > #h(a) = 5`) is unaffected — only the reported lengths need correction.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage placement
**Why out of scope**: The lemma `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` is a property of tumblers and spans (a half-open-interval identity), independent of any link-ontology content. Its natural home is a tumbler or span algebra ASN. The proof and its uses (L10, L13) are correct as stated here; relocating it is an architectural cleanup awaiting the consolidation, not a defect in this ASN.

### Topic 2: Operational alignment between L1c's "structural producibility" reading and event-level GlobalUniqueness invocations
**Why out of scope**: The ASN's deliberate distinction between L1c (structural witness chains, may overlap across links) and GlobalUniqueness (per-(t, k') uniqueness over genuine allocation events) is correct and internally consistent. The conformance proofs (L9, L11b) interleave both readings, which works but invites future tightening — best handled when an explicit allocator-event semantics ASN is introduced.

VERDICT: REVISE
