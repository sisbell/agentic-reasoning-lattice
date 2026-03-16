# Review of ASN-0042

## REVISE

### Issue 1: `delegated` definition does not enforce O1a; O15 references only `delegated`

**ASN-0042, Delegation section**: "We write `delegated_Σ(π, π')` to mean that principal `π'` was introduced into `Π` by an act of `π` in state transition `Σ → Σ'`, subject to three structural constraints: (i) ... (ii) ... (iii) ..."

**Problem**: The `delegated` relation has three conditions — strict prefix extension, most-specific covering principal, and novelty — but none constrain `zeros(pfx(π'))`. O15 references `delegated` as the exclusive mechanism for post-bootstrap principal introduction: `(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ : delegated_Σ(π, π')))`. O7 separately adds `zeros(pfx(π')) ≤ 1` as a precondition for delegation grants, but this constraint is not part of the `delegated` definition that O15 invokes.

Following the formal chain strictly: a principal `π'` with `pfx(π') = [1, 0, 2, 0, 3]` (zeros = 2, document level) satisfies all three conditions of `delegated` when delegated from `π` at `[1]`. O15 admits it. O1a is violated. The ASN then enters an inconsistent state: O2 makes `π'` the effective owner of addresses in `dom(π')`, but O7 withholds allocation and delegation rights (zeros condition fails), so `dom(π')` becomes a dead zone — the most-specific covering principal exists but lacks authority.

The asymmetry is highlighted by the ASN's own proof approach: the delegation section proves that `delegated`'s three conditions suffice to preserve O1b (PrefixInjectivity), establishing a precedent that invariant preservation is argued from the `delegated` definition. No corresponding argument is given for O1a, because the `delegated` definition lacks the constraint needed to make such an argument.

**Required**: Either (a) add `zeros(pfx(π')) ≤ 1` as condition (iv) of the `delegated` definition, which makes O1a preservation follow immediately and parallels the O1b preservation proof, or (b) add an explicit O1a preservation argument after the delegation definition showing that `delegated` + O7's constraint jointly maintain O1a, and clarify in O15's prose that delegation must also satisfy O7. Option (a) is cleaner — it keeps the constraints co-located with the mechanism and makes O7's zeros clause derivable rather than load-bearing.

## OUT_OF_SCOPE

### Topic 1: Dynamic node creation
The bootstrap axiom O14 permits multiple initial node-level principals (e.g., `[1]` and `[2]`), but the model provides no mechanism for creating new top-level nodes post-bootstrap. A principal at `[1]` cannot delegate `[2]` — delegation requires strict prefix extension (condition (i)), and `[1]` is not a prefix of `[2]`. Any new node would require a principal whose prefix is a prefix of every possible node address — effectively the empty tumbler, which T4 excludes. If the docuverse is meant to grow new nodes over time, this requires machinery outside the current ownership model.

**Why out of scope**: Node namespace management is a separate concern from intra-node ownership. The ASN correctly focuses on ownership within a given set of bootstrap principals.

### Topic 2: Interaction between O10 (fork) and the content model
O10 establishes that non-ownership induces forking and specifies the ownership properties of the fork (conditions (a) and (b)), but deliberately defers the content relationship between the original address and the fork. The ASN notes this explicitly: "a relationship that belongs to the content model, not the ownership model." Whether the fork preserves transclusion identity, carries links, or maintains version lineage are content-model questions.

**Why out of scope**: O10's scope is correctly bounded to ownership consequences. Content identity under forking is a separate specification concern.

VERDICT: REVISE
