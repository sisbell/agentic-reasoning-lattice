# Review of ASN-0126

## REVISE

No REVISE items. This is an anti-bloat pass on a mature note, so I verified the load-bearing arguments line by line rather than skimming; the following were checked and found sound.

**The two hardest arguments hold.** The R-Scope transfer in *Retraction as an attributed Binary* is the riskiest claim in the note (it imports an ASN-0086 transition result through a value the result was never proven for). Its three-move structure is airtight: the wrapper's underlying step `π(Σ) → π(Σ')` and the empty-from Nullify `π(Σ) → Ψ` both invoke `a_emit` on the *same* `(π(Σ), d_retr)`, and since `a_emit` is F-blind they deposit at the identical fresh address, giving `dom(π(Σ').L) = dom(Ψ.L)` and hence `A_rel^{π(Σ')} = A_rel^{Ψ}`; the two post-states differ only in the F-slot value, which neither `A_rel` nor the fixed target subtree `{t : a ≼ t}` reads. The substitution to `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` then follows, with B1 sharing the L-component. The projection bridge's B1/B2 scope discipline is correctly observed — the note applies R-Scope *natively* at `π(Σ) → Ψ` (not via B2, since `Ψ` is not `→_sh`-reachable) and explicitly excludes existence-of-successor results from B2 (a genuine statement of what the lemma does *not* do, not meta-prose).

**The wp analysis is non-trivial and the conjunct accounting is complete.** The derivation correctly uses the *un-simplified* ASN-0086 wp Case 2 (with C3 live), not the disciplined-domain simplification — exactly right, because `→_sh` does not enforce the unit-depth retraction discipline. The omission of (0) (forced by the arity-3 slice / Emit_K's always-arity-3 effect), L3 (each clause discharged by (0), input typing, and RegisteredAdmissible), and `K ∈ T_admissible` (absorbed by "K registered") all check out. The finding that C3 is *the* newly-live conjunct under `→_sh` is the real content of the section, not filler.

**The worked illustration verifies a real postcondition against concrete addresses.** I re-derived the born-nullified scenario: `a_R = inc(ℓ₂,0) = …2.3 ∉ coverage(G_rng) = [..2.4, ..2.7)` so the retractor lands active; then the citation lands at `a_emit(Σ₁,d) = inc(a_R,0) = …2.4 = g`, the lower endpoint of `G_rng`, so C3 fails and the tuple is born nullified. The ghost-root example (`a = 1.1.0.1.0.1.0.2`, `zeros=3`, `#E=1`, P-tgt-failing) correctly demonstrates the second gap the gate cannot see.

**Boundary cases are covered:** empty-from (`|F|=0`, no `→_sh` image), arity `> 3` (precondition (0), → OQ6), ghost addresses (L4/L9 inherited), empty registry (degenerate but consistent — no link can ever be created). P1–P6 are each derived (no proof-by-checkmark); P6's induction correctly carries the three-conjunct predicate and discharges persistence via L12, P1, and P4 separately rather than by "similar reasoning." Foundation usage is clean — only ASN-0043 and ASN-0086 are cited by number.

I looked specifically for the anti-bloat patterns the classifier targets. The strongest candidate — the "Existence-of-successor results are excluded" paragraph — is a statement of what B2 does *not* do, which the guidance explicitly exempts; it prevents a real misapplication (transferring R0 via B2) and earns its place. The P5 forward-references are functional citations forced by a genuine dependency (`P5 → RegisteredAdmissible`, which lives in the wp section), not gratuitous deferral.

## OUT_OF_SCOPE

### Topic 1: Staged / dynamic type registration (registry growth across states)
**Why out of scope**: P1 commits the registry to permanent immutability, so a substrate can never learn a type after `Σ_init`. This is the note's deliberate central guarantee, not a gap. Whether a successor relaxes P1 to admit monotone registry growth (append-only registration, mirroring the L-store's own monotonicity) is a different design; OQ4 touches only how `Σ_init.registry` is *initially* composed, not post-init growth.

### Topic 2: Operational semantics over the shape catalog
**Why out of scope**: idempotence-at-emit, the behavior catalog, default predicates, and predicate composition are correctly deferred (OQ1–5). This note establishes only the static well-formedness layer (gate + registry + conformance), which is the right foundation to settle first.

### Topic 3: Richer source/arity (`|F| > 1`, `N > 3`)
**Why out of scope**: the single-source commitment and arity-exactly-3 gate are deliberate scoping, with the extension path explicitly routed to OQ6.

VERDICT: CONVERGED
