# Review of ASN-0130

I worked through the proofs in depth. The technical core holds: PR2's acyclicity (the `e₁(r) < e₁(D)` embedding, including the self-reference and re-registration cases), PR3a's substitution induction, the PR0/PR5a weakest-precondition partitions, the born-nullified/ever-registration handling, and the ST⁺ soundness ground are all sound, and the worked composition (esp. the `H` capture contrast) is a genuine verification, not a checkmark. The findings below are precision and accreted-prose issues, which is where this note (carrying the anti-bloat classifier) is most exposed.

## REVISE

### Issue 1: PR5's threshold extension is phrased to over-reach, then walled off by a digression
**ASN-0130, PR5 (DynamicsCertification)**: "The parameter reading extends that threshold position from 'ℕ literal' to any *bound* ℕ value, the parameter included" … "The phrasing's apparent reach would matter only for a bound ℕ value whose fixity is *not* given — a value read through PC2's binder guard … No such value can occupy a classified threshold: PD0's grammar admits no binder-guard rule … The bound ℕ values that can reach a classified aggregate threshold in an ST⁺-classifiable term are therefore exactly the environment-bound parameters and the ℕ literals — both fixed across every step".

**Problem**: The rule is stated broadly ("any *bound* ℕ value"), and then a full paragraph entertains and dismisses binder-guard-bound and quantifier-bound ℕ values — cases PD0's grammar *already* excludes from classification. This is exactly the "imagines a case the carrier already excludes" pattern: the defensive prose exists only because the phrasing over-reaches, and the note itself concludes the safe set is "exactly the environment-bound parameters and the ℕ literals." Beyond bloat, the broad phrasing makes ST⁺'s soundness *contingent* on a PD0 grammar accident — if a future PD0 revision ever classified a binder-guard or an ℕ-binding form, "any bound ℕ value" would silently admit a non-fixed threshold and break soundness, whereas the proof currently leans on "PD0's grammar admits no binder-guard rule" to forbid it.

**Required**: State the threshold extension directly as the two fixed cases the note proves are the only reachable ones — "an ℕ literal or an environment-bound parameter." This covers the motivating `count(L_W) ≥ x` example, discharges soundness unconditionally (both cases are fixed across a step, the only property PD0's argument consumes), and deletes the binder-guard/quantifier digression entirely.

### Issue 2: PR3a's capture-freeness justification is false for the sequential intermediates it invokes
**ASN-0130, PR3a (ExpansionWellTyping), Substitute step**: "Discharge by `k` applications of WT's PC2 plain-composition rule, last parameter first … No step captures — the term being substituted into has only expansion-name binders, chosen fresh for every `Eⱼ`".

**Problem**: The proof explicitly works at the *sequential* level (`k` applications of PC2 on `u[y_k:=E_k]…[y_{j+1}:=E_{j+1}]`). After the first substitution the term being substituted into contains the inserted `E_{j+1},…,E_k`, whose binders include author names — an argument `eⱼ` may itself bind variables (e.g. `count({z ∈ A_K : …})`), and `expand(eⱼ)` retains those author binders since expansion renames only *referents'* binders, not the host's. So "the term being substituted into has only expansion-name binders" is literally false for every step after the first. The *conclusion* (no capture, well-typing preserved) is correct — each `yⱼ` occurs only within `u` at positions scoped by expansion-name binders alone, and the already-inserted `Eᵢ` sit in disjoint subtrees whose author binders never scope a remaining `yⱼ` — but the stated reason does not hold of the intermediate terms the PC2 chain actually operates on.

**Required**: Justify capture-freeness at the level where it holds — either (a) note that each `yⱼ` occurs only in `u` (all of whose binders are expansion names) at parameter positions disjoint from the `E_{>j}` insertion sites, so no inserted author binder scopes any `yⱼ`; or (b) argue capture-freeness for the *simultaneous* substitution into `u` directly (where "`u`'s binders are all expansion names" is true), then cite `yⱼ ∉ Eᵢ` only for the sequential-equals-simultaneous step.

### Issue 3: PR5a restates the idem-⊤ hit/miss dynamics PR0 already spells
**ASN-0130, PR5a (CertificationSurface)**: "a *hit* — an active certificate already denoting `a` — returns the incumbent's address, no step taken, `d` unread; a *miss* with `d ∈ dom(Σ.M)` deposits … at the frontier address `a_emit(Σ, d)`; a miss with `d ∉ dom(Σ.M)` is rejected."

**Problem**: This is a near-verbatim restatement of PR0's "a *hit* … returns the incumbent's address, no step taken, `d` unread; a *miss* with `d ∈ dom(Σ.M)` deposits …; a miss with `d ∉ dom(Σ.M)` is rejected." Both are just I1/I6's idem-⊤ branch contract (ASN-0128). PR5a defers cleanly everywhere else it parallels PR0 ("The wp mirrors PR0's", "the partition is PR0's", "PR1's analogue, same proof shape") — the hit/miss block is the one place it duplicates instead of deferring.

**Required**: Replace the hit/miss spelling with a deferral to I1's idem-⊤ contract as PR0 invokes it, retaining only the Unary-specific note (`G = ∅`).

## OUT_OF_SCOPE

### Topic 1: Validated supersession for version lineages
**Why out of scope**: PR4 leans on the shipped generic S2 "without addition," so nothing enforces that a `supersedes` edge connects two *registered* definitions. A buggy or adversarial edge can make `tip(a)` resolve to a sink address that is not an ever-registered definition, on which `evaluate` then fails its precondition — a case PR4's "follows `tip` and handles ⊥" guidance does not cover (⊥ is only the branch/cycle verdict, not a non-definition sink). A future ASN could add a definition-aware `supersede_pred` surface that validates both endpoints, as `register_pred` validates references; that is new territory, not a defect in this note's deliberate use of generic S2.

### Topic 2: Authorization of registration
**Why out of scope**: `register_pred(d, A_def)` places the classifier tuple's home at the caller's `d` with no required relation to `origin(A_def)`, so a builder may register a `pdef` over content owned by another document (consistent with L4 endset generality). Whether registration should be ownership-gated is an authorization-model question the corpus does not yet address.

VERDICT: REVISE
