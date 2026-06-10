# Review of ASN-0115

I worked the proofs. The mathematical core is sound: the Confinement lemma is correctly discharged from T5 + TumblerAdd; R6's gap analysis (the trichotomy `V_S(d) = ∅` / `act = ∅` / `act ≠ ∅`, the "canonical start forced by `act ≠ ∅`", and the terminal-overrun conclusion via D-SEQ★) is airtight; R7's WLOG and the divergent-branch justification are load-bearing and correct; R8's content/link dispatch (subspace-sharing via S3★+SD, link-vacuity via CL-OWN+CL-UNIQ) holds. The worked instances check out, including the deeper-tumbler `[1,2,1]` ordering. I found no proof-by-similarly and no missing-case in the claims that are stated. The findings below are a boundary the ASN defines but does not finish, one vacuous open question, and residual meta-prose (the anti-bloat classifier's target).

## REVISE

### Issue 1: Behavior on a depth-incompatible V-spec is unspecified
**ASN-0115, "What a spec-set is"**: "when `S` is already populated in `d` (`V_S(d) ≠ ∅`) the start must match that subspace's common depth, `#s = m_S(d)` … When `V_S(d) = ∅` the constraint is vacuous."
**Problem**: Depth-compatibility is imposed as a *well-formedness condition* on the V-spec, so a span whose start has `#s ≠ m_S(d)` is simply not a valid V-spec, and the operation's behavior on it is left undefined. But document subspace depth is mutable: ASN-0047's `m_S(d)` is re-pinned "from scratch at any value ≥ 2" after a subspace is fully cleared (K.μ⁻ to `n'_S = 0`, then K.μ⁺). So a permanent citation `(d, σ)` that was a valid V-spec at one reachable state can cease to be one at a *later* state of the **same** document `d`, with no specified outcome. This silent domain-exclusion sits uneasily beside R6's emphatic robustness ("deliver what can be delivered … never fail the whole") and R11's permanence of stale-but-referenced content: a depth-stale citation is the same flavour of stale reference as an unbound position or orphaned content, yet it is handled by exclusion rather than graceful filtering. The constraint is *not* cosmetic — dropping it would not uniformly yield empty: a shallow start (`#s < m_S`, e.g. `s = [1,1]` against `V_1(d) = {[1,1,k]}`) captures the whole subtree, so depth-compat does load-bearing work and cannot simply be relaxed.
**Required**: Specify what RETRIEVEV does with an otherwise-well-formed but depth-incompatible request — reject it, or treat its active set as empty — and reconcile that choice with R6. A single sentence settling the boundary suffices.

### Issue 2: Open Question 3 is vacuous under the standing S3★ invariant
**ASN-0115, Open Questions**: "What invariant must govern delivery when a spec-set's resolved references include an address with no entity bound in either store?"
**Problem**: Every reference RETRIEVEV resolves is `Σ.M(d)(v)` for an active position `v`, and the standing reachability precondition makes S3★ (ASN-0047) hold: `subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)` and `subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)`. A resolved reference therefore always has an entity bound in exactly one store (link items even carry `a ∈ dom(Σ.L)` directly). The posited scenario cannot arise from this operation's resolution; the question asks for an invariant governing an impossible situation.
**Required**: Remove the question, or reframe it explicitly as a model-extension scenario (e.g. "were S3★ relaxed…") so it does not read as a live gap in RETRIEVEV.

### Issue 3: Roadmap / preview meta-prose (anti-bloat)
**ASN-0115, "What a spec-set is" (after R0) and "The problem"**: "Everything that follows is an analysis of this object. We name `deliver` as R0; the named claims R1–R11 record the invariants any faithful realization must satisfy." and "We shall find that 'deliver the content' decomposes into a resolution step … and a fetch step …, and that the interesting content of the operation lives in the boundary conditions …"
**Problem**: These are navigational scaffolding that does not advance the argument — a meta-statement ("Everything that follows is an analysis"), a downstream inventory ("the named claims R1–R11 record…"), and a conclusion-preview ("We shall find that…"). The note carries the anti-bloat classifier; this is the residual meta-prose it targets. The same pattern recurs in section-sequencing phrases ("Now the first of the questions…", "The last revelation.").
**Required**: Delete the meta/roadmap sentences; let R0 and the claims stand. Concrete examples and statements of what the operation does or does not do are not the target — only the navigational prose.

## OUT_OF_SCOPE

### Topic 1: Sibling RETRIEVE-family operations and the genuinely-future open questions
**Why out of scope**: Per-subspace/overall extent (ASN-0113/0112), endset search (ASN-0110), link-structure reading (ASN-0111/0114), and the discovery/replication commands are correctly excluded. In particular, delivering a link as a reference `⟨ref, a⟩` rather than its endset structure (R10) *respects* that boundary and is not an under-specification — delivering the full link value would be the encroachment. The open questions on inline provenance, permitted failure modes, and transmission-channel faithfulness are genuine future territory, appropriately deferred (Q3 excepted — see REVISE).

VERDICT: REVISE
