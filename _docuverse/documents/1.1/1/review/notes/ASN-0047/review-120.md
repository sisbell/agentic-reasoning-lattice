# Review of ASN-0047

After a careful pass over the elementary transitions, the per-state and composite-boundary invariants, the cross-layer invariants, and the worked examples, I found one substantive logical gap in the K.δ discharge. The ASN is otherwise quite rigorous — proofs include explicit case analyses, the verification matrix is comprehensive, the K.μ~ dependency chain is laid out non-circularly, and the worked examples trace invariants step-by-step.

## REVISE

### Issue 1: K.δ case (ii) k = 2 sub-case A discharge is incomplete for subsequent accounts

**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation*, sub-case A**:

> "the K.δ event that minted `t` was itself a K.δ case (ii) k = 2 event with operand `parent(t)` (necessarily a node, since `IsAccount(t)` requires `zeros(t) = 1`, and the structural identity `zeros(e) = zeros(t_op) + 1` at k = 2 fixes the operand's zero count at 0 — IsNode) ... in either case its T2 spawn step activated `A_account(parent(t))` with `t` as the first emission."

**Problem**: The claim that the minting event was K.δ k = 2 holds only for the *first* account under `parent(t)`. For *subsequent* accounts (siblings), `t = inc(t_prev, 0)` was minted by a K.δ case (ii) k = 0 event with operand a prior sibling account `t_prev`. The k = 0 structural identity `zeros(e) = zeros(t_op)` is also consistent with `zeros(t) = 1` (with `t_op` an account), so the discharge's elimination argument from `zeros(t) = 1` to "minted by k = 2 with node operand" is not exhaustive. The further claim "with `t` as the first emission" is then false: for subsequent accounts, the first emission of `A_account(parent(t))` is some earlier sibling, not `t`. The conclusion `t ∈ dom(A_account(parent(t)))` is correct in both cases, but the reasoning as written only discharges the first-account case.

The accompanying remark "Sub-case A makes no recursive appeal — sub-case A spawns documents from account operands, not accounts from account operands, so there is no chain of sub-case A events leading back to a base" is true about sub-case A itself, but it conceals that the discharge for subsequent accounts *does* require induction back through K.δ k = 0 events to the first account.

**Required**: Either case-split sub-case A explicitly:
- *Sub-case A1*: `t` is the first account under `parent(t)`. Minted by K.δ k = 2 (sub-case B or C) with operand `parent(t)`; that event placed `t` as the first emission of `A_account(parent(t))`.
- *Sub-case A2*: `t` is a subsequent account. Minted by K.δ k = 0 with operand `t_prev` (a prior sibling); the K.δ k = 0 event placed `t = inc(t_prev, 0)` on `A_account(parent(t_prev))`'s sibling chain, and `parent(t) = parent(t_prev)` by the k = 0 structural identity gives `t ∈ dom(A_account(parent(t)))`. The chain of K.δ k = 0 events terminates inductively at the first account, dispatched by Sub-case A1.

Or replace the discharge with a direct appeal to T10a's per-allocator-chain consistency: every emission of `A_account(N)` (whether placed by the activating T2 spawn or by subsequent T1 sibling-increments) inhabits its tracked domain, and `t ∈ E_account` with `parent(t) = N` forces `t` to be such an emission by T10a.6 (DomainDisjointness) — independent of which K.δ event placed it.

The compare-and-contrast with the K.δ k = 1 discharge ("the prior K.δ event that minted t supplies the T2 spawnPt premise") is instructive: that discharge correctly abstracts over the minting event's kind. Sub-case A should do likewise.

## OUT_OF_SCOPE

None beyond what the ASN already defers in its *Open Questions* section (concurrent-transition discipline, link-withdrawal/tombstoning reconciliation with D-CTG★, account-level depth-1 extension, node-allocation registry abstraction layer, link inheritance under forking).

VERDICT: REVISE
