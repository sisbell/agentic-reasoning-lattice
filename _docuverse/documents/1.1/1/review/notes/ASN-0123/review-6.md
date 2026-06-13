# Review of ASN-0123

I worked through the apparatus (PS, SA, VN-B1, nextv) and the core invariants (V4, V8, V9 severance, V10, V13). Most of it is genuinely rigorous: the SA antichain proof, VN-B1's case analysis over K.δ, and the V9(a) severance argument all hold up under scrutiny. One internal inconsistency, introduced by the node-tier path, must be fixed.

## REVISE

### Issue 1: The node-tier cross-owner fork mints two entities, contradicting `E' = E ∪ {v}`, V0, and V1

**ASN-0123, V-WF vs. the Effect clause / V0 / V1**: V-WF discharges realizability for the cross-owner branch by stating that "a node-tier forker (`zeros(pfx(π)) = 0`, which O1a admits into `Π`) … reaches a fresh document only through an out-of-scope, possibly multi-step document-creation composite — baptizing an intermediate account before the document." Meanwhile the Effect clause asserts `E' = E ∪ {v}`, V0 asserts "exactly one identity is allocated," and V1 asserts "ΔE = {v} mints exactly one identity."

**Problem**: Baptizing the intermediate account is a K.δ step, and entities are permanent (P1 — no transition removes an entity), so for a node-tier cross-owner fork the registry grows by the account *and* the version: `E' = E ∪ {a_acct, v}`. This contradicts the unconditional `E' = E ∪ {v}`, V0, and V1, all stated without a case split.

The case is reachable, not pathological. The bootstrap principal `π₀` covers `n₀ = [1]`, so by PS(iii) `pfx(π₀) = [1]` is node-tier (`zeros = 0`, admitted by O1a). It may fork a document owned by an account principal. And there is genuinely no single-step escape: `inc` reaches only `k ≤ 2`, and `k = 2` from a node (`zeros = 0`) yields an account (`zeros = 1`), so a second descent — a second baptized entity — is structurally unavoidable to reach a document (`zeros = 2`).

The ripple reaches two more clauses:
- **`Π' = Π`** (Effect clause): if `a_acct` is registered as a principal via delegation, Π changes.
- **V9(b)** ("`ω'(v) = π`"): if `a_acct` is a principal, it is the maximal-length coverer of `v`, so `ω'(v) = a_acct ≠ π`, and V9(b)'s proof (which leans on `allocated_by(π, v)` and O5 maximality at π's tier) collapses. If `a_acct` is *not* registered as a principal, V9(b) survives — but then the entity-count claims (E', V0, V1) still fail.

V-WF's "Either way the produced `v` satisfies Document(v), v ∉ E, and O5's placement" attends only to what `v` satisfies; it never reconciles the net `E`-delta. The account-tier cross-owner case is clean (one K.δ from the account's document sub-allocator, `ω'(v) = π`, `E' = E ∪ {v}`) — the defect is confined to node-tier cross-owner forks, but the affected claims are stated universally.

**Required**: Reconcile the single-mint guarantees with the node-tier cross-owner path. Either —
- **(A) Restrict.** Confine the cross-owner clause (and, correspondingly, the Effect clause's `E' = E ∪ {v}`, V0, and V1) to forkers that already possess a document-creation namespace — e.g. `zeros(pfx(π)) = 1`, or π draws from an account already in Π — and state that a node-tier principal without an account must establish one first (outside this operation), so VERSION's single-mint guarantee does not cover that prior setup. This keeps "exactly one thing is minted: the identity" true as written. Or —
- **(B) Widen.** Case-split the Effect clause's `E`-delta, V0, and V1 — single-mint in the owned and account-tier cross-owner cases, `E' = E ∪ {a_acct, v}` in the node-tier case — and resolve `Π' = Π` and V9(b) explicitly against whether `a_acct` is registered as a principal.

## OUT_OF_SCOPE

### Topic 1: How a node-tier principal establishes a document namespace
**Why out of scope**: Document creation from scratch is ASN-0103 territory, and the ASN is right not to specify the account-baptism mechanics here. The fix for Issue 1 is *not* to specify that machinery — it is to ensure the in-scope claims (`E' = E ∪ {v}`, V0, V1, V9(b), `Π' = Π`) do not silently assert something that the deferred mechanics contradict.

VERDICT: REVISE
