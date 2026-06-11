# Review of ASN-0120

The core machinery of this ASN is sound: the V→I conversion (ML1) is properly grounded in T5-confinement plus S3★, the recovery equation's `F`-trace is correctly motivated and derived (the frontier-leak argument is exactly right), the merge argument now handles shift-at-zero and TS3 composition carefully, and the ML9 weakest-precondition derivation discharges both the link-half of Fact (a) and the `d' = d` boundary of Fact (b) correctly. Three precision issues remain, all localized.

## REVISE

### Issue 1: "never exact equality" fails at the empty-resolution boundary
**ASN-0120, "What the endset arguments name, and what resolution recovers"**: "No admissible representation makes `coverage(e)` equal to `ρ(R, Σ)` itself: coverage is a union of order-convex intervals, while `ρ(R, Σ)` is a bare finite set, and ASN-0053 (S7, CoveringExistence) guarantees only *covering*, `coverage(e) ⊇ ρ(R, Σ)` …, never exact equality."
**Problem**: The universal claim is false at the boundary `ρ(R_j, Σ) = ∅`, which the operation admits for the from and to slots (only `R₃` carries the non-emptiness precondition, and `wf` does not require any spec to capture an active position — nor even `p ≥ 1`). When `ρ = ∅`, the postcondition's span-shape clause ("each of the form `(s, δ(n, #s))` with `s ∈ ρ(R_j, Σ)`") forces `e_j = ∅` as the *unique* admissible record, and then `coverage(∅) = ∅ = ρ(R_j, Σ)` — exact equality. The ASN's own first Open Question acknowledges that empty resolution can arise, so the case is in-model, not hypothetical.
**Required**: Qualify the claim to non-empty resolutions ("for `ρ(R, Σ) ≠ ∅`, no admissible representation…"), or alternatively add a precondition excluding empty resolution for slots 1–2 — but the latter would contradict Open Question 1, so the qualifier is the right fix. Either way, state the `ρ = ∅` / `e_j = ∅` boundary explicitly where the admissible records are characterized.

### Issue 2: ML4's coverage description contradicts the ASN's own coverage/store-trace distinction
**ASN-0120, "Residence, and its independence from what the link connects"**: "the address `a` extends `d`'s prefix, while each `coverage(e_j)` is an arbitrary subset of allocated I-addresses (ASN-0043, L4 EndsetGenerality)."
**Problem**: Two misstatements in one clause. First, `coverage(e_j)` is *not* a subset of allocated I-addresses: by the ASN's own covering-surplus analysis, coverage strictly exceeds its store trace whenever `ρ(R_j, Σ) ≠ ∅` — it contains the infinite non-store descendants of every resolved address. Second, it is not "arbitrary": the recovery equation pins it extensionally to subtree-unions over `ρ(R_j, Σ)`, and the restriction paragraph after ML6 explicitly disclaims L4's full generality for MAKELINK ("it creates neither a ghost type … nor any ghost or foreign endset … not the full generality of L4"). Citing L4's generality here is in direct tension with that paragraph. The point ML4 actually needs is only that nothing couples `d` to the *resolved sets*.
**Required**: Restate as a claim about `ρ(R_j, Σ)`: the resolved sets range over finite subsets of `dom(Σ.C)` with no constraint relating them to `d` (in particular, possibly disjoint from everything under `d`'s prefix). Drop or narrow the L4 citation so it does not assert generality the operation does not have.

### Issue 3: the degenerate one-sided-link sentence is incoherent and pre-empts Open Question 1
**ASN-0120, "Three endsets: directionality, typing, and relation versus connection"**: "The degenerate one-sided case is consistent — when there is no meaningful from, the first endset alone designates what is pointed at."
**Problem**: As written the sentence contradicts itself: if there is "no meaningful from," the first endset *is* the from slot, so it cannot simultaneously be the slot that "alone designates what is pointed at" — either the slot index or the role name is wrong. Moreover, the semantics of a one-sided link (an empty non-type endset) is precisely what the ASN's first Open Question declares undetermined; the body should not partially answer a question it defers. This is the imagining-a-deferred-case pattern the anti-bloat discipline targets.
**Required**: Delete the sentence, or replace it with a coherent statement that names which slot is populated and which is empty, and explicitly defers the connection-semantics of the empty slot to Open Question 1.

## OUT_OF_SCOPE

### Topic 1: Semantics of an empty from- or to-endset
**Why out of scope**: What an empty non-type endset *means* for the link's connection is genuinely new territory, already flagged in Open Questions. Issue 1 above asks only that the present universal claim not be falsified by the boundary; the meaning question itself belongs to a future ASN.

### Topic 2: Endset arguments reaching the link subspace, and direct I-address endset arguments
**Why out of scope**: Link-to-link endsets and the I-address argument shape that could produce ghost or foreign endsets (L4/L9 generality) are distinct argument forms the ASN correctly defers; the V-spec form specified here is complete on its own terms.

VERDICT: REVISE
