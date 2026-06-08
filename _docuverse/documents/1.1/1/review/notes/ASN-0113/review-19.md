# Review of ASN-0113

This note carries the `review-mode.anti-bloat` classifier. The mathematical content is sound — I checked W4/W10 (T5 prefix-confinement, correct), W5 (forward construction at the run's actual minimum via T0(a)+S8-fin+T5, converse via order-convexity, both correct), W9 (S3★-aux + SC-NEQ, correct), W11 (SC-NEQ on first component, correct), and W20 (wp partition, correct). The findings below are accreted meta-prose and duplication, which is what this review mode targets.

## REVISE

### Issue 1: The allocated-empty vs unallocated distinction is stated twice
**ASN-0113, W-pre and W0**: W-pre already establishes the distinction in full — "An *allocated empty* document (`d ∈ dom(M)`, `M(d) = ∅`) legitimately yields the empty span-set `⟨⟩` ... An *unallocated* identity (`d ∉ dom(M)`) is *outside the operation's domain*" plus the "Gregory's back end confirms the separation" aside. W0 then restates it: "This `⟨⟩` is the report of an *allocated but empty* document; it is *not* the behavior on an unallocated identity, which W-pre places outside the operation's domain (and which the implementation answers with the failure marker, not `⟨⟩`)."
**Problem**: Two paragraphs say the same thing; W0's version adds nothing beyond a back-reference to W-pre and a second implementation aside. This is the "two paragraphs in the same document say the same thing in different words" pattern.
**Required**: Make the distinction once (in W-pre, where the precondition lives) and have W0 simply state its result type without re-litigating the unallocated case.

### Issue 2: W15 pre-empts an objection the claim does not need
**ASN-0113, W15 (Independence)**: After establishing the substantive point (each count is read off the disjoint sets `V_{s_C}(d)`, `V_{s_L}(d)`, by SC-NEQ), the claim spends a paragraph raising and disarming a hypothetical: "The extension transitions happen to be single-subspace ... but contraction is not. ASN-0047's K.μ⁻ selects a per-subspace retention count `n'_S` for *each* `S` ... so it is false that every V-position transition acts within one subspace. Independence survives this anyway ..."
**Problem**: The independence claim is about *counts read off disjoint data*, which the opening sentences already settle. The K.μ⁻ both-contracting digression imagines a transition-level case the count-level argument never relied on, then defends against it. This is reviser drift — defensive prose anticipating an objection that the claim's own framing excludes.
**Required**: State independence as a property of the counts (disjoint position sets) and the single-subspace-edit conditional; drop the K.μ⁻ rebuttal.

### Issue 3: The consumer "absent-equals-zero" point is deferred and then duplicated
**ASN-0113, W14 and Open Questions #2**: W14 carries a forward deferral — "separate from how a *consumer* recovers `n_S = 0` from a span-set whose empty member is absent — that absent-equals-zero reading is a consumer-side convention this note does not rely on and flags as not obviously safe (see Open Questions)." Open Question #2 then restates the same concern: "comparison treats an absent subspace as the value zero (W14), how must a *consumer* interpret an omitted member ...".
**Problem**: The same consumer-convention caveat appears in two slots with a "see X below" pointer between them. W14's job is to establish that `n_S` is a total function (which it does in one sentence); the consumer-side hedge is the Open Question's content, not the claim's.
**Required**: Keep the total-function fact in W14, move the consumer-interpretation caveat entirely to the Open Question, and drop the forward pointer.

### Issue 4: W12's reachability witness re-derives foundation coupling mechanics
**ASN-0113, W12 (ProfileIrreducibility)**: The forward construction inventories the ASN-0047 transition vocabulary at length — "each text position is a *coupled K.α + K.μ⁺ + K.ρ composite* — a K.α step ... (discharging J0), and a K.ρ step recording `(a, d) ∈ R'` (discharging J1★ and J1'★) ... each link position is a *coupled K.λ + K.μ⁺_L composite* ..." and flags "(this is the mechanism behind W15, Independence, below)."
**Problem**: A reachability existential needs a witness, but the prose re-explains *which step discharges which coupling obligation* — a use-site inventory of foundation semantics — and forward-points to W15, whose single-subspace-extension explanation it duplicates. The witness can cite the composite vocabulary without narrating each coupling discharge.
**Required**: Compress to the witness sequence and its effect on the two counts; cite ValidComposite★ rather than re-deriving J0/J1★/J1'★ at each step, and remove the W15 forward pointer (the overlap is the duplication, not a dependency).

## OUT_OF_SCOPE

### Topic 1: Non-contiguous reporting policy
**Why out of scope**: W5 correctly establishes the *fact* that no single span is exact over a non-contiguous `V_S(d)`; the *design decision* (fragment vs. bounding span) is properly left to Open Question #1 and a future ASN. No action needed — flagging only to confirm W5's fact-level treatment is not itself a scope violation.

META: 

VERDICT: REVISE
