# Review of ASN-0071

## REVISE

### Issue 1: The counterexample motivating `actionPoint(ℓ) ≥ 2` is inconsistent with the `actionPoint(ℓ) = #u` precondition

**ASN-0071, "The query"**: "Without it, the vspec preconditions admit displacements that perturb position 1 — for example, `u = [1, 5]` with `ℓ = [2, 0]` has `Pos(ℓ)` and `#ℓ = #u`, and its action point is `actionPoint(ℓ) = 1`"

And again in **"Resolution"**: "the counter-example `u = [1, 5]`, `ℓ = [2, 0]` exhibited above would silently include a link-subspace V-position ... Without the `actionPoint(ℓ) ≥ 2` precondition, position 1 could fall *at* or *beyond* the action point".

**Problem**: The vspec definition lists `actionPoint(ℓ) = #u` as a standing precondition. For `u = [1, 5]` we have `#u = 2`, but the example's `actionPoint(ℓ) = 1 ≠ 2`. So this displacement violates `actionPoint(ℓ) = #u` and is *already* rejected — removing only the `actionPoint(ℓ) ≥ 2` clause does not admit it. The text conflates T12's loose bound (`actionPoint ≤ #u`) with the vspec's tightened `actionPoint = #u`. Given `actionPoint(ℓ) = #u` together with `#ℓ = #u`, the only thing `actionPoint(ℓ) ≥ 2` actually adds is the floor `#u ≥ 2`; an `actionPoint = 1` displacement can only arise when `#u = 1`. The chosen example cannot exhibit the failure it claims to.

**Required**: Replace the counterexample with one consistent with `actionPoint(ℓ) = #u` — a depth-1 anchor, e.g. `u = [1]` (= `[s_C]`), `ℓ = [2]`, where `actionPoint(ℓ) = 1 = #u`, reach `[3]`, and `⟦σ⟧ = {t : [1] ≤ t < [3]}` straddles into the link subspace (`[2, …]`). Then state plainly that, under `actionPoint(ℓ) = #u ∧ #ℓ = #u`, the role of `actionPoint(ℓ) ≥ 2` is exactly to force `#u ≥ 2`, excluding depth-1 anchors. As written the two preconditions and their justification do not cohere.

### Issue 2: The cross-depth "prefix names subtree" semantics is never exercised by a concrete `find` result

**ASN-0071, "The query"**: "Reusing the depth-`3` source above, suppose the user submits a *shallow* vspec `u = [s_C, 1]`, `ℓ = δ(1, 2)` ... So `⟦σ⟧ ∩ dom(M(d_s))` is the *entire* depth-`3` subtree hanging under `[s_C, 1]` — `n` positions resolved from a span anchored at a single depth-`2` coordinate."

**Problem**: Cross-depth subtree capture (`#u < m`) is one of the operation's load-bearing design commitments — it is argued at length and explicitly distinguished from the forbidden interior-action-point over-collection. Yet the worked scenario is depth-2 throughout and, by the ASN's own admission, "the depth-2 worked scenarios below cannot exercise" the relevant cases. The cross-depth argument stops at "`⟦σ⟧ ∩ dom = n positions" and never runs the result through `iaddrs` and `find` to a concrete result set. A deliberately-chosen behavioral semantics asserted but not verified against a specific scenario is a depth gap (Standard 6).

**Required**: Add a concrete cross-depth worked computation: a depth-3 source, a shallow vspec, the resolved `iaddrs(Q)(Σ)`, and the resulting `find(Q)(Σ)`, confirming the subtree-capture intent. This is also the only setting where the `#u ≥ 3` interior-action-point rejection (`σ'` vs `σ''`) can be exhibited against an actual arrangement rather than in the abstract.

## OUT_OF_SCOPE

### Topic 1: Connecting `find`'s current-state result to a transition that contracts an arrangement
**Why out of scope**: The ASN correctly defers this to the Open Questions ("What invariant must connect FINDDOCSCONTAINING's result immediately before and after a transition that contracts an arrangement?"). A transition-relating invariant for `find` belongs in an operation-interaction ASN, not in this query specification.

### Topic 2: Provenance-based ("ever contained") query as a sibling operation
**Why out of scope**: The reconciliation section correctly identifies that recovering full historical containment requires a separate `R`-based mechanism. Specifying that operation is new territory, not a defect here.

VERDICT: REVISE
