# Review of ASN-0115

I checked the substantive proofs (Confinement, R6 no-interior-hole, R7 repeatability, R8 transclusion vacuity, R11 orphan-deliverability) and the worked instances against the foundation contracts. The mathematics is sound — the Confinement lemma discharges correctly from T5, R6's bindable-slice argument is rigorous, R7 correctly identifies that comparability (not mere co-reachability) is the load-bearing hypothesis, and R8's CL-OWN/CL-UNIQ vacuity argument is valid. The two findings below concern the depth-compatibility prose, not the underlying logic.

## REVISE

### Issue 1: The `act` override-branch gloss mischaracterizes its own trigger condition
**ASN-0115, "What a spec-set is, and what delivery is" (the `act` definition)**: "In the override branch — a once-valid start gone too shallow for the subspace's current depth — the active set is forced empty, *overriding* the geometric `dom(Σ.M(d)) ∩ ⟦σ⟧` lest a now-too-shallow start capture deeper content the citation never named."

**Problem**: The override branch fires whenever `¬depthcompat(ρ,Σ)` — i.e. `V_S(d) ≠ ∅ ∧ #s ≠ m_S(d)`. The appositive "a once-valid start gone too shallow" captures one corner of that condition and silently excludes two sub-scenarios the branch equally covers:
- *Too-deep starts* (`#s > m_S(d)`, not too-shallow): reachable by minting against an empty subspace — where the well-formedness rule admits any `#s ≥ 2` — and later inserting shallower content, e.g. mint `#s = 7` with `V_S(d) = ∅`, then insert at depth 2 so `m_S(d) = 2 < 7`. Here the override is a vacuous no-op: by the Confinement lemma no bound position of depth `m_S(d) < #s` can agree with `s` on positions `1…#s−1`, so the geometric `dom(M(d)) ∩ ⟦σ⟧` is already `∅`. The override only *bites* (differs from the geometric value) in the too-shallow direction.
- *Never-matched starts*: a spec minted against an empty subspace was never depth-matched, so "once-valid" misdescribes how it entered the branch.

The override is *correct* in every case — but a reader given only "a once-valid start gone too shallow" cannot tell whether too-deep or never-matched stale specs reach this branch (they do).

**Required**: Characterize the branch by its actual trigger (any consulting-state mismatch `#s ≠ m_S(d)` with `V_S(d) ≠ ∅`), not the single once-matched-then-re-pinned-deeper corner. This is a tightening, not an expansion.

### Issue 2: The V-spec definition pre-explains `act`'s fail-soft semantics via forward reference
**ASN-0115, "What a spec-set is, and what delivery is" (the V-spec definition)**: "The definition of `act` below makes that state-relative failure operative — forcing an empty active set at any consulting state where the spec is depth-incompatible — so a stale spec delivers nothing and the request still succeeds rather than failing the whole."

**Problem**: Sited at the V-spec definition, this sentence explains the behavior of `act` (defined a paragraph later) and the fail-soft request semantics (R6) before either is in scope, through a forward reference ("below"). The same "depth-incompatible ⟹ `act = ∅` ⟹ delivers nothing without failing the whole" content is then carried by the `act` definition itself ("the active set is forced empty, overriding the geometric…") and again by R6 ("`act(ρⱼ, Σ) = ∅` and the whole span is filtered, still without failure"). The staleness/fail-soft story is thus told three times, the upstream telling premature — exactly the forward-reference accretion the review mode flags at source.

**Required**: At the V-spec definition keep only the fact a reader needs *there* — that the depth conjunct is re-evaluated at the consulting state rather than fixed at mint — and locate the operative behavior and its rationale at the `act` definition and its R6 consequence, where `act` exists. Per the guidance, this is a placement fix, not a deletion of content.

## OUT_OF_SCOPE

The future topics the ASN does not settle — inline provenance within delivered material, permissible outright-failure conditions, dangling references under relaxed S3★, delivery-channel faithfulness, and single-span subspace straddling — are appropriately deferred to the Open Questions rather than half-specified. No improper inclusions: R10 delivers link *references* and explicitly defers link-structure reading (READLINK/ASN-0111), and the worked instances cite Gregory's implementation only as realizability evidence, not as specified mechanics — the ASN stays at the state/operation/invariant level.

VERDICT: REVISE
