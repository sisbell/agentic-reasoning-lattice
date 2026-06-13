# Review of ASN-0123

This is an unusually rigorous ASN. The derivation-from-guarantees structure (G1/G2/G3), the local apparatus (SA, VN-B1, the registry-coverage derivation in PS), the severance theorem (V9), and the link carry-through characterization (V10) all hold up under scrutiny. The address arithmetic checks out, the empty-source (n=0) boundary is handled throughout, and the cross-ASN citations are accurate (all referenced ASNs are foundations). I found one substantive proof defect.

## REVISE

### Issue 1: V9w's first conjunct over-claims P4★-independence; the monotonicity argument fails at the interior start states it claims to cover

**ASN-0123, V9w (SharedContentWitness)**: "The first conjunct holds at Σ ... not by any boundary property of Σ itself: each a ∈ A is arranged by d_src in its content subspace at Σ, so it became range-new there in an earlier composite, whose terminal boundary recorded (a, d_src) ∈ R by J1★; P2 then carries that row forward to Σ. The argument leans only on the monotonicity of R, so it stands whether or not Σ is itself a composite boundary — the gap the composite-boundary property P4★ would otherwise leave at an interior start state does not arise."

**Problem**: The load-bearing premise — that a's entry into d_src's content range was recorded "in an *earlier* composite, whose *terminal boundary* recorded (a, d_src) ∈ R" — fails at exactly the interior start states the passage claims to cover.

ASN-0047 separates per-state invariants from composite-boundary properties, with P4★ in the latter class; that separation is meaningful only because reachable states can be composite interiors that violate P4★. This ASN's own atomicity remark affirms such interiors exist ("a genuine interior state — after K.δ, before K.μ⁺") and explicitly **declines to assume composite isolation** ("nothing in the foundation forbids another composite from beginning there ... we do not lean on it").

Now take a reachable state Σ that is interior to a composite W which has executed K.μ⁺ extending d_src's content range with address a but has not yet executed its matching K.ρ — the content-without-provenance interior that the atomicity remark's own logic admits for any composite. At Σ: a ∈ ran(M(d_src)|content), so a ∈ A; but (a, d_src) ∉ R, because W's terminal boundary lies *after* Σ, not before it — W is the in-progress composite, not an "earlier" one. VERSION begun at Σ adds only (·, v) rows, so (a, d_src) ∉ R'. The first conjunct (a, d_src) ∈ R' is then **false**. The sentence "the gap ... at an interior start state does not arise" names precisely the gap where the argument breaks.

The monotonicity argument therefore silently requires that no in-progress composite has extended d_src's content range without recording provenance — i.e. that Σ is quiescent w.r.t. d_src. That is a composite-isolation assumption, which the ASN disclaims two paragraphs earlier. The sound route is the one the passage deliberately rejects: at a composite boundary, P4★ gives Contains_C(Σ) ⊆ R directly, hence (a, d_src) ∈ R for every a ∈ A — but this requires Σ to be a boundary, flatly contradicting "stands whether or not Σ is a composite boundary."

This same latent dependency sits under **V-WF**'s claim that the post-state Σ' satisfies the composite-boundary properties (P4★ ∧ P4a ∧ P7a): if VERSION is begun at the bad interior above, then at Σ' we have (a, d_src) ∈ Contains_C(Σ') but (a, d_src) ∉ R', so P4★ fails at Σ'. V-WF's P4★ claim is sound only when Σ is itself a clean boundary — the same condition V9w's argument needs but denies needing.

**Required**: Withdraw the "stands whether or not Σ is a composite boundary" claim. Either (a) make explicit that VERSION's start state Σ is a composite boundary — a defensible precondition, consistent with the atomicity remark's boundary-level framing and the implementation's whole-request serialization — and derive the first conjunct from P4★ (this also discharges V-WF's composite-boundary-property claim cleanly); or (b) add an explicit premise that no in-progress composite has extended d_src's content range without its provenance step, and reconcile that premise with the atomicity remark's refusal to assume composite isolation. The second conjunct (a, v) ∈ R', which rests on VERSION's own K.ρ steps via V13, is unaffected.

## OUT_OF_SCOPE

### The concurrency/composition model itself
The question of how composites serialize or interleave — and therefore whether reachable states can in practice be left interior to an unfinished composite — is correctly deferred to the ASN's open questions ("what serialization concurrent forks require"). Issue 1 is *not* a request to resolve that model; it is a request to fix an unsound proof step and an internal inconsistency that exist regardless of how the concurrency model eventually settles. The fix is local and editorial-logical.

VERDICT: REVISE
