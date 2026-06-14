# Review of ASN-0134

This is a strong, unusually careful note. The conflict theory (H0–H2), the per-home confluence result (G1) with its registration lift (H3), the invariant partition (W0–W6), and the quiescence analysis (V0/V2/V1) are all properly proved, the boundary cases that matter for *this* stack are hit (first-emission collision in H2 and §7), and §7/§8 ground the abstractions in explicit addresses. Two issues remain — one of them load-bearing for the freshly-added clause 8.

## REVISE

### Issue 1: The "not K-surface-emitted" claim — on which clause 8's necessity rests — contradicts ASN-0128's literal definition and is left unreconciled

**ASN-0134, §4 (instance (i)) and §9 M1(b)(ii)**: "The resulting execution is a valid →_sh execution but is not K-surface-emitted, so ASN-0128 I1a's single-survivor does not reach it (§9 clause 8 restores it)."

**Problem**: ASN-0128 defines a derivation as *K-surface-emitted* iff "every `L_K`-growing step along it … is the deposit branch of an `Emit_K` invocation." In the both-miss derivation, *each* deposit (X's and Y's) is the deposit branch of an `Emit_K` invocation — X's and Y's respectively. So under the foundation's **literal** definition the both-miss derivation **is** K-surface-emitted, hence I1a **does** apply and yields ≤1 active tuple per coverage class — i.e. *no duplicate*, and *clause 8 is unnecessary*. That is the exact inverse of ASN-0134's conclusion.

The actual reconciliation is that I1a's *proof* ("the deposit branch … fires only on a miss: at the pre-state its I0-class had no active member") silently requires each deposit to be a miss **at that step's own pre-state** — automatic in ASN-0128's sequential model, where the operation's input state *is* the step's pre-state, but broken here: Y's deposit pre-state is `Σ ∪ {T_X}`, at which Y "would be a hit" (your words) and would take no step. So Y's deposit is not a genuine surface miss-deposit, I1a's induction breaks at it, and the derivation is not K-surface-emitted *in I1a's operative sense*. ASN-0134 supplies the premise ("where it would be a hit") but never draws the inference, and never flags that the literal definition appears to say the opposite. Since clause 8 is the headline of this revision and its necessity argument is precisely "drop clause 8 ⟹ not K-surface-emitted ⟹ I1a fails ⟹ duplicate," this gap leaves the central new contribution resting on an unstated reinterpretation.

**Required**: State explicitly that "K-surface-emitted" is operative only when each `L_K`-growing deposit is a miss evaluated at *that step's own pre-state* (guaranteed by the sequential operation→step identification, breakable by a concurrent realization whose dedup-read and deposit pre-state diverge); show the both-miss derivation fails this at Y's deposit; and note that ASN-0128's literal "deposit branch of an `Emit_K`" would, naively read, classify it as K-surface-emitted. Then clause 8 — forcing the dedup-read to the deposit's own pre-state — restores genuine K-surface-emittedness, I1a applies, and the duplicate is suppressed.

### Issue 2: The batch taxonomy omits the empty (m=0) and singleton (m=1) boundaries, while asserting exhaustiveness and non-atomicity

**ASN-0134, A1**: "this happens in four ways" (read-only query / idem-hit / nullify-hit / rejected call). **A5**: "A multi-step batch (`m ≥ 2`) is not atomic." **What this note commits**: "A fire/batch (a `retract_stale`, a definition's content run) is many steps and is **not** atomic."

**Problem**: A `retract_stale` over an empty stale set is a fire with `m = 0` — zero steps, vacuously atomic — and a `retract_stale` with exactly one stale event (or a one-atom definition run) is `m = 1` — a single step, atomic. Neither is one of A1's "four ways" of being zero-step (so the exhaustiveness claim is false at `m=0`), neither is a "single state-changing operation … not issued as a batch" (A1's one-step subject), and A5/the commitment's blanket "a batch is not atomic" is false for both. A quiescence or termination layer reasoning "a `retract_stale` is never atomic" from the commitment would err exactly at the empty/singleton boundary — the mandatory "empty structure" case.

**Required**: Scope the non-atomicity claim to `m ≥ 2` and state the degenerate boundaries — an `m=0` fire is zero steps (vacuously atomic), an `m=1` fire is one step (atomic and behaving as a single operation) — so A1's "four ways" and A5/the commitments are correct at the boundary.

## OUT_OF_SCOPE

### Topic 1: Batch read-atomicity (making a multi-step batch appear all-or-nothing to a reader)
**Why out of scope**: A5/§6 correctly establish that contiguity (W4) is the writer-side half only, and the reader gap is explicitly deferred to Open Question 5. This is new territory (a stronger contract than MIC), not an error in MIC.

### Topic 2: Cross-server composition of per-home orders
**Why out of scope**: G1's per-home independence is offered as the seam, and the multi-server consistency model is deferred to Open Question 7 and "What this note does not cover" (BEBE). Correctly future work, consistent with the stated Scope.

META: (none — the note defines observable state, the operation-realization grain, and an implementation-independent contract of guarantees; it stays in specification territory and explicitly refuses to name a mechanism.)

VERDICT: REVISE
