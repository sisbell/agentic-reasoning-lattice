# Review of ASN-0123

This is a careful, rigorous note. The derivations (G1–G3), the antichain lemma SA, the contiguity induction VN-B1, and the severance theorem V9 are all sound, and the empty-source (n = 0), iterated-fork, and node-tier-forker boundaries are genuinely handled rather than waved past. I found one proof defect that the author created by reaching for a generality the foundations do not support.

## REVISE

### Issue 1: V9w's first conjunct ((a, d_src) ∈ R') is unsupported for non-boundary invocations — and the proof claims exactly that robustness

**ASN-0123, V9w (SharedContentWitness)**: "The first conjunct holds at Σ … not by any boundary property of Σ itself: each a ∈ A is arranged by d_src in its content subspace at Σ, so it became range-new there in an earlier composite, whose terminal boundary recorded (a, d_src) ∈ R by J1★; P2 then carries that row forward to Σ. The argument leans only on the monotonicity of R, so it stands whether or not Σ is itself a composite boundary — the gap the composite-boundary property P4★ would otherwise leave at an interior start state does not arise."

**Problem**: The argument silently assumes a entered d_src's content range in a composite that **completed before Σ** ("an earlier composite, whose terminal boundary recorded (a, d_src)"). That assumption is exactly what fails at the states the robustness claim is asserted to cover.

Within one valid composite the couplings J1★/J1'★ are required only initial-to-final, and the order of the range-extending K.μ⁺ and the provenance-recording K.ρ is free. So a valid composite necessarily has interior states at which `a` is in `d_src`'s content range but `(a, d_src) ∉ R` — which is precisely why ASN-0047 makes `Contains_C(Σ) ⊆ R` (P4★) a *composite-boundary* property rather than a per-state invariant. The note's own atomicity remark admits that VERSION may begin at such interior states ("nothing in the foundation forbids another composite from beginning there"). At an interior Σ lying inside the very composite that just extended d_src's range, `(a, d_src) ∉ R`, hence `(a, d_src) ∉ R'` (VERSION adds only `(·, v)` rows, by V3/V13). V9w's first conjunct then fails, and "stands whether or not Σ is itself a composite boundary" is the precise overreach.

This is not idle: at such an interior start the post-state Σ' likewise carries `(a, d_src) ∈ Contains_C(Σ')` but `(a, d_src) ∉ R'`, so Σ' fails P4★ — consistent with Σ' being interior. V-WF is careful to claim only the per-state invariants for Σ' (not the composite-boundary properties), but V9w needs the boundary-dependent fact `(a, d_src) ∈ R` and tries to get it without a boundary.

**Required**: Get `(a, d_src) ∈ R` the clean way. VERSION is invoked at a composite boundary; there P4★ gives `Contains_C(Σ) ⊆ R` directly, and since `a = M(d_src)(u)` for `u ∈ V_{s_C}(d_src)` we have `(a, d_src) ∈ Contains_C(Σ) ⊆ R`. Then delete the "whether or not Σ is a composite boundary" sentence (it is false), or explicitly restrict V9w's source-side conjunct to composite-boundary invocations. If interior-start invocations are to remain admissible per the atomicity remark, V9w's first conjunct must be qualified: it holds only when the source's content range was last extended by a *completed* composite. (Note the J1★+P2 argument is itself sound *at a boundary* — every earlier range-entry composite has terminated and J1★ has fired; the defect is solely the claim that it survives interior starts.)

## OUT_OF_SCOPE

None to add. The note scopes itself well: editing, link creation, comparison, content delivery, and replication are touched only through frame conditions (V11) or foundation invariants (V10), and the genuinely new territory — concurrency serialization, location-fixed windowing, withdrawal semantics, derivation-direction recovery — is deferred to the Open Questions rather than half-specified. The implementation-evidence section reads as correspondence-and-deviation grounding, not as mechanics leaking into the spec, so no META.

VERDICT: REVISE
