# Review of ASN-0115

## REVISE

### Issue 1: R11's weakest-precondition claim omits depth-compatibility

**ASN-0115, §"What governs the material: permanence of the source" (R11)**: "The weakest precondition for delivery to include the value at `a` is therefore a *single* live condition: (i) the consulted arrangement binds some named content position to `a`. There is no independent store-membership conjunct to add."

**Problem**: This ASN's own `act`-override makes depth-compatibility a *second* live condition — independently falsifiable by editing — that (i) does not entail. The note carefully distinguishes "named" (`v ∈ ⟦σ⟧`) from "active" (`v ∈ act`) everywhere (R6: "A named position the consulted arrangement does not make active — one outside `act(ρⱼ, Σ)`"), and the two diverge exactly when the override fires. Counterexample built entirely from this ASN's machinery plus the ASN-0047 re-pinning that §"What a spec-set is" itself cites: let `(d, σ)` be a depth-2 spec, `σ = ([1,2], δ(1,2))`, so `reach = [1,3]`, minted while `m_{s_C}(d) = 2`. Later the content subspace is fully cleared (K.μ⁻ to `n' = 0`) and re-pinned at depth 3 ("the next insertion re-pins `m_S(d)` from scratch at any value `≥ 2`"), and content `a` is rebound at `[1,2,1]`. Then `[1,2] ≼ [1,2,1] < [1,3]`, so `[1,2,1] ∈ ⟦σ⟧`: (i) holds — a named content position is bound to `a`. But `depthcompat((d,σ), Σ)` fails (`#s = 2 ≠ 3 = m_{s_C}(d)`), so `act = ∅` and the value is **not** delivered. Hence (i) is not the weakest precondition for the fixed spec `(d, σ)` to deliver `a`'s value — the ASN's own override falsifies it. R11's actual store-membership point is correct; the "single live condition" framing overlooks the depth condition the override makes operative.

**Required**: Either restate (i) in terms of `act` — "binds some *active* content position to `a`" (`v ∈ act`) — which folds in depth-compatibility while keeping R11's real point intact (store membership rides along by S3★, no separate conjunct); or reframe the claim as *deliverability* (matching the headline "remains deliverable") and exhibit the witness explicitly minted depth-compatibly — a unit-width span rooted at the bound position, `s = v`, `#s = #v = m_{s_C}(d)` — so depth-compatibility is satisfiable and (i) is the sole obstruction. The worked instance has the same gap: it asserts `act((d',σ'),Σ') ∋ v'` without verifying depth-compatibility of `σ'`, the very condition the override makes load-bearing.

### Issue 2: Use-site inventory appended to the `act` definition

**ASN-0115, §"What a spec-set is, and what delivery is"**: "This case-split is the single operative definition of `act`; every later use — R0's `deliver`, `item` totality, R3, R6, R7 — reads it, the override included."

**Problem**: A definition's introduction enumerating its downstream consumers does not advance the definition's meaning — it is a maintenance index that goes stale as claims are renamed or added, and the reader must skip past it to follow the definition. This is the forward-reference accretion the review mode is meant to catch.

**Required**: Delete the sentence. The definition stands on its own; downstream claims cite `act` where they use it.

### Issue 3: Duplicated "delivers nothing / request still succeeds" rationale

**ASN-0115, §"What a spec-set is, and what delivery is"**: the depth-compatibility paragraph ends "so a stale spec delivers nothing and the request still succeeds rather than failing the whole," and the `act`-definition paragraph repeats it near-verbatim — "the spec then delivers nothing and the request still succeeds rather than failing the whole."

**Problem**: The same outcome is asserted twice in the same section in slightly different words (then a third time as R6 and its proof). The override's effect needs stating once.

**Required**: Collapse the two prose copies in the definition section to one. Keep the single substantive piece of rationale ("lest a now-too-shallow start capture deeper content the citation never named"); R6 may restate the outcome as its formal content. Drop the duplicated outcome-sentence.

## OUT_OF_SCOPE

### Channel faithfulness and single-span subspace straddling
**Why out of scope**: Both are correctly deferred — the transmission-channel disclaimer (§"Faithfulness") and the boundary-crossing single span (§"What a spec-set is" / Open Questions) match the scope note's exclusions and are handled by composing per-subspace ordinal spans rather than one straddling span. No action needed; flagged only to record that the scope boundary was checked.

VERDICT: REVISE
