# Channel Assignment — ASN-0123 review-7

**Date:** 2026-06-13 00:21

## Issue 1: Node-tier cross-owner fork — V9(b) ownership is asserted, not established
Reason: Neither channel — the fix is forced by reasoning already present. Single-mint (an established design constraint, derived in the Problem section and carried by V0/V1) plus the entity algebra's tier-respecting `k ≤ 2` increments — a node-tier prefix (`zeros = 0`) cannot reach a document (`zeros = 2`) in one K.δ without baptizing an intermediate account, a second permanent entity under P1 — together compel restricting the cross-owner branch to account-tier forkers (`zeros(pfx(π)) = 1`), after which `allocated_by(π, v)` and O5's maximality w.r.t. `π` hold cleanly. The current text already carries this argument; the design-intent backing (tier-respecting forking, [LM 4/17] in PS/V8) is also already cited.

## Issue 2: V9w's first conjunct cites a composite-boundary property at an unconstrained start state
Reason: Neither channel — this is a citation repair within the formal model. The reviewer supplies the salvage verbatim: replace the boundary-only P4★ appeal with the persistence route — `a` entered `d_src`'s content-subspace range at some prior transition whose boundary recorded `(a, d_src)` via J1★, preserved to Σ by P2 — or constrain the start state to a composite boundary. Both use only ASN-0047 foundation properties (J1★, P2, P4★, composite-boundary structure) already invoked elsewhere in the note.
