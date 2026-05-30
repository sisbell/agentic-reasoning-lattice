# Review of ASN-0042

## REVISE

### Issue 1: O15's delegation-admission conditions do not guarantee O17b/O18 realizability

**ASN-0042, O15 condition (i) vs. O17b + O18**: O15(i) requires only `pfx(π) ≺ pfx(π')`; O18 requires `pfx(π') ∈ Σ'.B ∖ Σ.B` in the single introducing transition; O17b requires that same single transition add exactly `next(Σ.B, p, d)` for some B6-valid `(p, d)`.

**Problem**: Combining O18 and O17b forces `pfx(π') = next(Σ.B, p, d)`. By ASN-0040's `next`/B1, that address is the `(hwm+1)`-th sibling of a stream `S(p, d)` and is reachable only when its stream-predecessors (`c₁ … c_hwm`) are already in `Σ.B`. But O15(i) admits *any* strictly-extending prefix with `zeros ≤ 1`. A delegation of, e.g., `pfx(π') = pfx(π_d).3.5` (or `[1,0,2,3]` from node `[1]`) satisfies O15(i)–(vii) yet cannot be realized as a single `next` baptism when the intervening stream positions were never baptized — so the axioms are not jointly satisfiable for every O15-admitted delegation. The worked example tacitly confirms the hidden requirement: the bootstrap table deliberately seeds `[1, 0, 1]` *precisely* so that `[1, 0, 2] = next(Σ₀.B, [1], 2)` is reachable. That precondition is load-bearing but appears nowhere in O15.

**Required**: Add to O15 (and to O7(c)'s recursive right) the condition that `pfx(π')` be `next`-reachable — i.e., `pfx(π') = next(Σ.B, p, d)` for some B6-valid `(p, d)`, equivalently that `pfx(π')`'s stream-predecessors are in `Σ.B`. Without it, the admission gate over-permits relative to the registry coupling, and O7(c)'s "`π'` may delegate any sub-prefix `p''` with `pfx(π') ≺ p''`" overclaims.

### Issue 2: O7(c) recursive-delegation right omits the contiguity precondition

**ASN-0042, O7(c)**: "`π'` may delegate a sub-prefix `p''` with `pfx(π') ≺ p''` … whenever `delegated` is satisfiable … in particular conditions (ii), (vi), and (vii) re-checked there."

**Problem**: The proof discharges (i), (ii), (vi) at `Σ'` and defers (vii) freshness, but never addresses that `p''` must also be a `next`-sibling of a baptized stream for O18/O17b to materialize it (Issue 1). The recursive chain witness (`π_k → π_{k+1}` appending one user-field component) happens to be next-reachable, which masks the gap — but the general statement quantifies over arbitrary `p''` with `pfx(π') ≺ p''`.

**Required**: State the next-reachability/contiguity obligation on `p''` alongside conditions (ii), (vi), (vii), or restrict the claimed right to single-step stream extensions as the witness actually constructs.

### Issue 3: Forward-reference accretion and use-site inventory in O17b

**ASN-0042, O17b**: "Consequently every registry reachable under the ownership transition relation `→` is reachable under ASN-0040's baptismal transition relation, so ASN-0040's registry results transfer to every ownership-reachable `Σ`: the invariants B0 …, B1 …, B10 …, and B_fin … hold, and the derived functions `hwm` and `next` have their preconditions … discharged at every use site by this coupling. O18's material baptism of a delegate's prefix is the instance of this axiom in which `(p,d)` opens the delegate's namespace."

**Problem**: The flagged anti-bloat patterns are present: a use-site inventory ("preconditions … discharged at every use site"), an enumeration of downstream consumers (B0/B1/B10/B_fin/hwm/next), and a forward-reference essay sentence pointing to O18. None of this advances the axiom's content; the axiom *is* the disjunction formula stated mid-paragraph.

**Required**: Reduce O17b to the axiom statement (the disjunction) plus, at most, one sentence naming the transferred ASN-0040 facts. Move "which preconditions hold where" to the use sites that actually need them. Delete the O18 forward-reference sentence.

### Issue 4: Organizational meta-prose in structural slots (State Axioms preamble)

**ASN-0042, "State Axioms" opening + "Notation" + "Reachability convention"**: The section opens with a paragraph describing which axioms govern which regime ("The transition-discipline axioms below constrain … the initial state `Σ₀` is governed by O14 … O5 and O16 apply to transition-induced allocations only …").

**Problem**: This is document-organization prose explaining axiom placement rather than stating system content — the kind of meta-prose the precise reader must skip past. The scoping it describes is already encoded in each axiom's quantifier (`a ∈ Σ'.B ∖ Σ.B`).

**Required**: Delete the regime-description paragraph; the per-axiom quantifiers already carry the scoping. Keep only the genuinely-needed `Σ.B` notation note.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The first Open Question (transfer divergence between provenance O6 and effective owner O2) is correctly deferred — the system as specified has no transfer mechanism, so this is new territory, not an error here.

### Topic 2: Cross-node identity federation
O9 establishes node-locality; the invariants a federation must satisfy (fifth Open Question) belong to a future ASN introducing federation, not to this one.

VERDICT: REVISE
