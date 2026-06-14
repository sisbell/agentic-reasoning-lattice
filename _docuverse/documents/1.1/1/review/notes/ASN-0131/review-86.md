# Review of ASN-0131

The mathematics is sound. I checked RE-NCD (the prefix/separator-zero argument confining the lemma to unit-depth spans), RE-ADDR (discipline ⟹ unit-depth `L_Θ` to-sets, antichain ⟹ only self-target covers a fresh output), the worked instance (every span/coverage computation verifies), RE-UDIST and the two-direction RE-UDIST-∩ analysis (the `⊆` half unconditional; both obstructions genuinely distinct, the second standing under an injective arrangement), RE-SEL's equality with `findlinks_V ∩ addressable`, RE-CWP (the Δ-form is equivalent to "touch image ⟹ touch `I_R`", boundary `R=∅` collapses correctly), and RE-RET (forward via permanence-of-nullification, backward via R-Scope single-tuple scope, conditional on the flagged `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis). No correctness errors, boundary cases covered (RE-BND), depth requirements met (concrete instance, non-trivial wp in RE-CWP and RE-ADDR, derived consequences in RE-SEL/RE-TRANS/RE-IDENT). The operation is properly abstract — a system guarantee, not implementation mechanics.

The remaining items are residual anti-bloat, per this note's classifier.

## REVISE

### Issue 1: Duplicated transition-framing inventory, cited and then re-listed
**ASN-0131, §"Fresh emissions and the addressable population" and §"Stability" (retraction)**: §"Fresh emissions" establishes "Σ.L evolves only through K.λ — the arrangement movers (K.μ family), entity creation K.δ, provenance recording K.ρ, and content allocation K.α all frame the link store (L' = L, ASN-0047/ASN-0093)." The retraction subsection then writes: "…Σ.L evolves only through K.λ **(the Σ.L-evolution inventory above)**. **Every non-K.λ transition — K.δ, the K.μ family, K.ρ, K.α — frames the link store (L' = L)** and so leaves nullified fixed…"
**Problem**: The second passage both *cites* the inventory ("the Σ.L-evolution inventory above") and *re-enumerates* it (the four transition kinds, plus `L'=L`). The cite-and-restate is the flagged accretion pattern — the re-enumeration is redundant given the explicit upstream pointer.
**Required**: Keep one. Either "Every non-K.λ transition frames the link store (the inventory above), leaving nullified fixed" (rely on the pointer) or drop the parenthetical pointer and let the list stand once. Not both.

### Issue 2: Definition introduction previewing downstream use rather than advancing meaning
**ASN-0131, §"When does an endset touch the region?"**: "We define, for the fixed region, `touch_W(e) ≡ coverage(e) ∩ image(W, d, Σ) ≠ ∅` — the subscript naming the region's V-position set W, **the one parameter that varies when we later compose regions**."
**Problem**: The substantive content is "the subscript naming the region's V-position set W." The trailing clause is a forward preview of the composition section; it advances nothing about the definition itself. This is the "definition's introduction enumerates downstream [use]" pattern. (Minor.)
**Required**: Trim to "— the subscript naming the region's V-position set W." The composition section already motivates the subscript where it is used.

## OUT_OF_SCOPE

The seven Open Questions (whole-endset vs touching-spans return value, multiplicity preservation, V-rendered answers, the structurally-restricted intersection-equality condition, non-co-resident link stores, type-slot/content matching, link-subspace regions) are correctly deferred — each is genuinely new territory, not a gap in this note. No claim in the note encroaches on the listed out-of-scope operations (RE withholds identity, does not count/enumerate/traverse/create), and ASN-0127's image and existence/discovery machinery is cited rather than rebuilt (the one-line `image(W₁∪W₂)=image(W₁)∪image(W₂)` sublemma is a fresh local step in service of RE-UDIST, not a re-derivation of F-IMG). No scope creep found.

VERDICT: REVISE
