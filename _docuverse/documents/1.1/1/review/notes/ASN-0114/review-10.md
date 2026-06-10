# Review of ASN-0114

The mathematics is sound. F0–F8 hold; the edge cases that matter (empty end, invalid selector, disconnected coverage, ghost / non-T4-valid covered addresses, infinite region-coverage, cross-document coverage) are addressed; the worked example correctly discharges F2 and F7; a non-trivial wp (`R = ⟨⟩`) is computed alongside the trivial domain wp; and every cross-ASN reference is to a foundation (ASN-0034, -0043, -0053, -0093, -0098). The F2 convexity argument and the F5 derivation via LP13 both check out. The remaining items are prose accretion and one rigor gap — consistent with the `review-mode.anti-bloat` signal — not correctness defects.

## REVISE

### Issue 1: Forward-reference scaffolding in "Status of the result"
**ASN-0114, "The selector and its domain" → bolded paragraph after F0**: "What F0 does *not* assert is uniqueness: F3 below shows the result is pinned only at the level of coverage, so distinct F1-witnesses may differ as span-sets." … "The one case in which the witness is forced to a unique span-set is the empty end, treated in F7."
**Problem**: The one fact that advances the argument here is the witness-exhibition — the recorded endset `Σ.L(a).eᵢ ∈ 𝒫_fin(Span)` is itself an F1-witness, so F0/F1 is satisfiable. That is genuine rigor and earns its place. Around it the paragraph wraps meta-commentary about "what F0 does *not* assert" and forward-pointers to F3 and F7 before either claim is stated — precisely the forward-reference meta-prose the anti-bloat pass targets. A reader must skip the scaffolding to reach the satisfiability point.
**Required**: Keep the witness-exhibition and a single sentence on coverage-determinacy. Drop the "what F0 does not assert" framing and the forward pointers; if the relation reading must lean on coverage-determinacy, place F3 before this paragraph so the dependency runs backward, not forward.

### Issue 2: S2-uniqueness re-derived at the wp site
**ASN-0114, "The empty end versus the invalid selector" → wp paragraph**: "since `⟨⟩` is the *unique* span-set of empty coverage (ASN-0053, S2), `R = ⟨⟩ ⟺ coverage(Σ.L(a).eᵢ) = ∅`. S2 then collapses that coverage condition to an endset condition…"
**Problem**: F7's own prose already establishes both halves of this — that `⟨⟩` is the only span-set of empty coverage, and that `coverage(eᵢ) = ∅ ⟺ eᵢ = ∅`. The wp paragraph re-runs the S2 argument from scratch rather than invoking F7's conclusion, and the worked example then makes a third pass ("by the uniqueness argument of the previous section"). The fact is load-bearing once; restating its derivation is accretion.
**Required**: Derive the S2 collapse once (in F7) and cite that conclusion at the wp site rather than re-deriving it.

### Issue 3: F6 grounded in implementation evidence rather than derived from F1
**ASN-0114, "Confinement: one end tells nothing of the others"**: "Gregory's evidence makes the confinement structural rather than incidental… We lift this to an abstract independence claim: **F6 (SlotConfinement).**"
**Problem**: F6's formal statement — equal slot-`i` coverage with arbitrary contents at `j ≠ i` yields equal results — is a one-step corollary of F1: `coverage(followlink(a,i)) = coverage(eᵢ) = coverage(eᵢ') = coverage(followlink(a',i))`. It is therefore forced for any F1-satisfying implementation, not a property "lifted" from Gregory's slot-bounded query (Q12, Q18). The note grounds F6 in the implementation and only gestures at the real source afterward ("Confinement is the dual of exactness"). Per the depth standard, a corollary should show its step, and showing it strengthens the claim (implementation-independence).
**Required**: Derive F6 from F1 in one line, and present the implementation evidence as corroboration of an F1-forced property rather than as its grounding.

## OUT_OF_SCOPE

The note fences the genuinely-future topics correctly: resolution of the recorded endset into a document's arrangement (and the resulting shrinkage), a canonical normal form for the returned span-set, protocol-boundary re-encoding of the `⟨⟩`/`⊥` distinction, and multi-document reporting are all deferred to open questions rather than claimed. Nothing to add here, and no in-scope claim strays into the OUT-OF-SCOPE list (READLINK, RETRIEVEENDSETS, V-position resolution, MAKELINK, etc.).

VERDICT: REVISE
