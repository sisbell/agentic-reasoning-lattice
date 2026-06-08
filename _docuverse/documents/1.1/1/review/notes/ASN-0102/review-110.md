# Review of ASN-0102

I checked the COPY definition, the three-class arrangement rewrite, the X16 tiling, the S3★ weakest-precondition reduction, the provenance routing (SL/RR/J1★/J1'★), and every worked example. The core construction is sound: the unmoved/copied/displaced classes tile `[1, n_S+W]` without gap or overlap, the displacement is non-destructive even when displaced images land on pre-existing keys, and S2/D-CTG★/D-SEQ★/S3★ are correctly re-established. The findings below are one rigor gap in the P4a discharge plus residual prose accretion (the note carries the anti-bloat classifier).

## REVISE

### Issue 1: P4a discharge overclaims that all traces to Σ′ factor through Σ
**ASN-0102, X17 (P4a TraceWitnessing)**: "Any valid transition trace reaching Σ' factors as a valid trace reaching Σ followed by this COPY composite, so its trace states are `{Σ_init, …, Σ, Σ'}`."
**Problem**: P4a quantifies over *all* valid traces reaching `Σ'`. The state value `Σ'` may in principle be reached by traces whose final transition is not this COPY, or whose penultimate state is not this `Σ`. The quoted sentence asserts every trace to `Σ'` passes through this particular `Σ`, which is not justified — it conflates "the trace this COPY produces" with "every trace to the state value `Σ'`."
**Required**: Frame the discharge parametrically, the way operation-preservation lemmas actually compose: for any invariant-satisfying pre-state `Σ` and any COPY producing `Σ'`, the COPY-terminated trace `(trace to Σ) ⌢ COPY` witnesses every pair in `R'` (old pairs in the reaching prefix by IH, new pairs at `Σ'` itself). The universal-over-traces P4a then follows from the reachability induction, where each trace's final transition is handled by *its* preservation lemma — not from the false claim that all traces to `Σ'` share this `Σ`.

### Issue 2: X15 carries residual rationale that states a modeling choice rather than a guarantee
**ASN-0102, X15 (Atomicity)**: "Whether this atomicity is *forced* or merely *chosen* depends on the case, and we separate them honestly." … "We adopt the elementary-transition model uniformly across all cases, but only the displacing case compels it."
**Problem**: The forced-case argument (intermediate `s_C` gap violates D-CTG★/D-SEQ★ forward; lost binding violates X7 reverse) is object-level and belongs. But the surrounding framing — "we separate them honestly," and the closing sentence justifying *why we adopt* the uniform model — is rationale for an authorial decision, not a system guarantee. This is essay content in a claim slot.
**Required**: Keep the forced-case proof. Reduce the non-displacing "atomicity is a choice" discussion to the bare structural fact (append/empty-subspace COPY is a contiguous extension expressible as a valid composite) and drop the meta-framing sentences.

### Issue 3: Intro restates foundation vocabulary as a use-site inventory
**ASN-0102, opening section**: "The tumbler vocabulary — the order `<`, displacement `⊕`/`⊖`, the shift `shift(t, k)` …, the subspace projector `subspace(v)`, the home-document projector `origin(a) = N(a).0.U(a).0.D(a)` (ASN-0036, S7) — follows the foundations. Mapping blocks `(v, a, n)` … follow ASN-0058."
**Problem**: This enumerates and restates foundation operators (including re-stating `origin`'s formula) that may be used without restatement. It is a use-site inventory that advances no reasoning.
**Required**: Cite the foundations once and use the symbols directly; drop the operator-by-operator restatement.

### Issue 4: "Same arrangement, differing only as representations" framing repeated across X17
**ASN-0102, X17**: the phrase "composite-boundary reading" is invoked three times ("Composite-boundary reading. Although COPY is a single elementary transition…"; "Under the composite-boundary reading above, with initial boundary…"; "Under the composite-boundary reading above, `ExtendedReachableStateInvariants` further demands…").
**Problem**: Three deferrals to the same framing paragraph is back-reference accretion — the reader is bounced to one location repeatedly rather than the setup being stated once and consumed.
**Required**: State the singleton-composite framing once at the head of X17 and let the subsequent P4★/P4a/P7a discharges rely on it without re-announcing "under the composite-boundary reading above."

## OUT_OF_SCOPE

### Topic 1: Re-displacement, containment-chain provenance, time-varying views, unreachable allocator
**Why out of scope**: These are the ASN's own Open Questions and concern operations and guarantees beyond COPY's single transition (subsequent INSERT/DELETE displacement, multi-hop containment recording, temporal view divergence, allocator unreachability) — future-ASN territory, correctly left as questions rather than claimed.

VERDICT: REVISE
