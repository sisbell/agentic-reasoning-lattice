# Review of ASN-0108

## REVISE

### Issue 1: W9a's "finite total tail inflow" is not sufficient for termination without a state-stable key

**ASN-0108, W9a (TerminationGuaranteed)**: "The genuinely sufficient condition is therefore *finite total tail inflow*: when only finitely many links are ever added ahead of the cursor, the total population the loop can consume … is a finite set; the cursor's key strictly advances on each non-empty call … no link is consumed twice, so this finite supply is exhausted in finitely many calls and a short window must eventually appear."

**Problem**: The proof's load-bearing step — "the cursor's key strictly advances on each non-empty call … no link is consumed twice" — holds only *instantaneously* per call (the next cursor is the ≺-max of the current window, hence ≻ links in *this* window evaluated at the current state). It does **not** give monotone advancement across the run unless the key is state-stable (W5). Under an unstable key, a previously delivered link's key can rise back above the current cursor and be re-delivered, breaking "no link consumed twice." A concrete counterexample, with **zero inflow** (finite, trivially satisfying the stated sufficient condition):

Content-position key (unstable), two links `a, b`, `N = 1`.
- Call 1 (`κ(a)=1, κ(b)=2`): deliver `a`, cursor `= a`.
- Call 2: `After(a)={b}`, deliver `b`, cursor `= b` (`κ=2`).
- Rearrange to `κ(a)=3, κ(b)=2`. Call 3: `After(b)={a}`, deliver `a` again, cursor `= a` (`κ=3`).
- Rearrange to `κ(a)=3, κ(b)=4`. Call 4: `After(a)={b}`, deliver `b` again…

Every window is full (`size 1 = N`), no short window ever appears, the loop runs forever — with **zero** total tail inflow. So "finite total tail inflow ⟹ termination" is false as stated. The W9a non-termination example tacitly used an allocation-monotone (effectively stable) key, which is exactly the hidden hypothesis the positive claim also needs.

**Required**: Condition the W9a termination sufficiency on a state-stable cursor key (W5) — under which the cursor's key is monotone across the run, delivered links never re-enter `After`, and the finite-supply exhaustion argument closes — and state explicitly that absent W5 even zero inflow does not guarantee termination (the rearrangement above being a W5 clause-2 violation).

### Issue 2: W9 conflates "recoverable cursor key" with "state-stable (W5)"

**ASN-0108, W9 (ExhaustionByShortWindow)**: "*Provided the cursor key is recoverable* — equivalently, provided the key is state-stable in the sense of W5, so that `κ(c)` still names the same cut-point …"

**Problem**: Recoverability and state-stability are not equivalent. W5 requires *two* preservations — the cursor's cut-point **and** the relative ≺-order among tail links. Recoverability of `κ(c)` is only the first (cut-point) clause for the single cursor. State-stable ⟹ recoverable, but not conversely. Moreover W9's own derivation ("`Window` returns `min(N, |After(c,Σ)|)`; if `< N` then `|After| < N` … new successor set empty") is a single-state argument that needs *only* recoverability of `κ(c)`, never tail-order preservation. So the "equivalently … state-stable in the sense of W5" both overclaims an equivalence and invokes a strictly stronger condition than the derivation requires.

**Required**: Drop the asserted equivalence; state W9's proviso as recoverability of `κ(c)` alone (the cut-point being preserved for the cursor), noting that this is *implied by* W5 but strictly weaker than it.

## OUT_OF_SCOPE

### Topic 1: Global ordering across multiple home documents
The behavior of the enumeration key when `Match` spans documents with independently-advancing link allocators (so no single allocation-monotone key orders the whole result) is correctly deferred to the Open Questions and is genuine future territory, not a defect here.

VERDICT: REVISE
