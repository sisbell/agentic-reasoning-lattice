# Review of ASN-0077

## REVISE

### Issue 1: Closure argument scope in O0(b)

**ASN-0077, O0(b) derivation of semantic correspondence**: "every reachable transition `Σ → Σ'` belongs to the closed enumeration of elementary transitions fixed by ValidComposite★ (ASN-0047): K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ."

**Problem**: The closure cites ASN-0047's ValidComposite★ as the closed enumeration of 8 transitions. But foundation ASN-0098 — extensively cited by ASN-0077 — explicitly considers a larger working frame "ASN-0047 + ASN-0093" in its LP-Comp note, distinguishing K.σ (from ASN-0093) from K.δ-IsDocument. If ASN-0093's K.σ is part of the active vocabulary inherited transitively through ASN-0098, the closure enumeration is incomplete; if K.σ is intentionally excluded, the scope decision should be explicit and justified. The conclusion (only K.λ grows dom(L)) is preserved either way (K.σ modifies dom(M), not dom(L)), but downstream consumers of O0(b) need to know which transition vocabulary the closure has been verified against. The same exhaustiveness gap recurs implicitly elsewhere (e.g., in O5 and O11's invocations of P3, which inherit ASN-0098's broader frame).

**Required**: Either (a) state explicitly that ASN-0077's working scope is restricted to ASN-0047's ValidComposite★ (justifying exclusion of K.σ), or (b) extend the enumeration to include K.σ with a one-line note that it modifies dom(M) but not dom(L), preserving the conclusion.

### Issue 2: Multi-step versions of O5 and O6 not stated explicitly

**ASN-0077, O5 and O6**: Both claims are stated for single transitions `Σ → Σ'`.

**Problem**: Foundation ASN-0098 pairs each single-step claim with an explicit multi-step counterpart (LP2 with LP2★, LP3 with LP3★, LP13 unconditional across `Σ →* Σ'`) precisely because downstream uses need multi-step preservation. ASN-0077 has single-step O5 (origin permanence) and O6 (I-span monotonic growth) but no explicit multi-step versions. The worked example's "Verifying O5 and O6" section reasons across Σ₀ → Σ₁ → Σ₂ but each step is treated single-step; reasoning that requires composition is left implicit. Downstream ASNs invoking origin preservation across composite transitions must re-derive the induction themselves.

**Required**: State explicitly O5★ ("for every reachable state sequence `Σ →* Σ'` and every `a ∈ dom(Σ.C) ∪ dom(Σ.L)`: `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)` and `origin'(a) = origin(a)`") and O6★ ("for every reachable state sequence `Σ →* Σ'` and every I-span σ: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`"), each with a brief derivation by induction over the transition chain citing the single-step result.

### Issue 3: Worked example omits direct verification of O8, O11, O11'

**ASN-0077, "A worked example" section**: The example exhibits O1, O4, O5, O6, O7, O9, O10, and the K.μ~ failure mode.

**Problem**: O8 (I-span containment monotonicity), O11 (V-span preservation under K.μ⁺ — equality, not merely inclusion), and O11' (V-span preservation under K.μ⁺_L) are not exhibited concretely. O11 in particular asserts *equality* rather than inclusion, and the example's K.μ⁺ transition (Σ₀ → Σ₁) provides a natural setting in which to verify this on a sub-span that does not cross the extension boundary (e.g., origins_V over σ_{1..5} at Σ₀ and at Σ₁ both yielding {d₁}, demonstrating equality under K.μ⁺). The example does illustrate I-span monotonic growth via σ_{cover}, but inclusion-vs-equality is what makes O11 substantive.

**Required**: Extend the worked example with one concrete computation each of O8 (two nested I-spans with the smaller's origins shown to be a subset of the larger's), O11 (σ_{1..5} origins at Σ₀ and Σ₁, showing equality preservation under K.μ⁺), and O11' (a K.μ⁺_L step adding a link V-position outside a content-subspace σ, with origins_V unchanged). Or alternatively, augment the existing example's Σ₀ → Σ₁ transition with the σ_{1..5} comparison.

### Issue 4: O0(c) totality claim under-justified

**ASN-0077, O0(c) derivation**: "Totality is (a). Single-valuedness is T4b's functional definition of projections."

**Problem**: Claim (c) asserts "totality and single-valuedness" on the domain `dom(C) ∪ dom(L)`. The derivation's one-line discharge — "Totality is (a)" — is correct only if (a) establishes that `origin` is *defined* on every element of `dom(C) ∪ dom(L)`. Clause (a) shows T4b's projections are defined (because zeros = 3 in both branches), but the totality claim asserts further that the *constructed tumbler* `N(x).0.U(x).0.D(x)` actually inhabits `E_doc` for every `x ∈ dom(C) ∪ dom(L)` — i.e., is the tumbler of an *allocated* document, not merely a syntactically well-formed prefix. That second step is supplied by (b) (semantic correspondence), not (a). The derivation should either route totality through (b) explicitly, or weaken the codomain claim in (c) to "the structural construction is well-defined" and let (b) carry the `E_doc` membership.

**Required**: Restate (c)'s derivation as "Totality on `dom(C) ∪ dom(L)` is (a) combined with (b) — (a) discharges well-formedness of the projection, (b) discharges membership of the result in `E_doc`. Single-valuedness is T4b's functional definition."

## OUT_OF_SCOPE

The ASN's Open Questions list correctly identifies six topics deferred to future ASNs: cross-subspace I-span handling, transitive provenance chains, native-vs-transcluded distinction, unreachable home documents, historical containment via Σ.R, and multi-position intra-document sharing. These are appropriate scope deferrals; no additional OUT_OF_SCOPE items beyond those.

VERDICT: REVISE
