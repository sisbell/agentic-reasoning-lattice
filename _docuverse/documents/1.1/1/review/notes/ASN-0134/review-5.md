# Review of ASN-0134

This is a careful, self-aware note. The stack-choice reasoning in §1 (taking the non-coupling 0093/0086/0126/0128 stack precisely so A6's "every state fully canonical" holds with no boundary-only invariant class) is correct and load-bearing; the H0–H2 conflict theory is clean; §7 grounds it in concrete addresses; and the V0/V2/V1 quiescence treatment correctly separates soundness from durability. The transfer machinery in A6 (RP-a for ASN-0126's per-state claims, B2-then-RP for ASN-0093's store invariants) is telescoped but sound. One real gap, plus a supporting precision fix.

## REVISE

### Issue 1: "one caveat" undercounts operation-level non-confluence

**ASN-0134, "What this note commits" (linearization bullet) and §4 (the step/operation seam)**:
- Commit: "every linearization of a per-home-serial schedule of raw steps is valid and reaches the same committed state (**the operation level adds one caveat — concurrent idem=⊤ coverage-equal emissions** — in §4)."
- §4: "the operation→schedule realization is itself order-dependent **precisely when** two concurrent operations are idem = ⊤ with coverage-equal (F, G)." … "the operation-level realization is order-stable **only when** no two concurrent operations are idem = ⊤ with coverage-equal (F, G)."

**Problem**: There is a second, independent source of operation-level order-dependence: a `Nullify_Binary` (an `Emit_R`, hence `K.λ_sh`) racing the emission of its cross-home target. Whether it commits a step turns on `P-tgt` (target presence), which `Emit_R`'s `idem=⊤` dedup does not govern — `P-tgt` reads `A_rel = dom(L)`, not the active subset `A_K`.

Concrete trace. Homes `d ≠ d'`. Agent A: `Emit_K` at `d`, landing at the deterministic, hence predictable, `a = a_emit(Σ, d)`. Agent B: `Nullify_Binary(a)` at `d_retr = d'`. Both proposed against common `Σ`, cross-home, ≺-incomparable:
- Order (A, B): A deposits `t` at `a`; at B's state `a ∈ A_rel`, `P-tgt` holds, B fires `Emit_R`, **`a ∈ nullified`**.
- Order (B, A): at B's state `a ∉ dom(L)` and `a ≠ a_emit(Σ, d')` (≠ home), so `P-tgt` **fails** — B is rejected, no step (ASN-0128 S3: "a call failing P-tgt … takes no →_sh step"). A then deposits `t` at `a`; **`a` active**.

The committed final state differs (nullified vs. active) by cross-home order — operation-level non-confluence with no `idem=⊤` coverage-equal pair (A is type K, B is type R; their `(F,G)` are not coverage-equal). At the raw-step level a *fixed* `O = {A, B}` is confluent (B born-nullified), exactly as G1(ii) says — but B's operation is *in O or not* depending on order, which is the very phenomenon §4 names. So "precisely when," "only when," and "one caveat" each overclaim.

The note already knows this case: **W5** says "if a writer means to retract another's tuple, the coordination layer must order the retraction after the emission, or the substrate will (correctly) reject it," and **Open Question 8** asks about "an out-of-order retraction whose target has not yet been emitted at its linearization state." §4 is not reconciled with these.

**Required**: Correct §4 and the opening commit to record (at least) two operation-level order-dependence sources — `idem=⊤` dedup (hit/miss, reading `A_K`) and `Nullify`'s `P-tgt` (fire/reject, reading `dom(L)`). Either broaden the characterization, or explicitly scope "precisely when …" to "absent the coordination-layer emit-before-retract hypothesis (W5)" / "among emit-only operations," and cross-link W5/OQ8 so the note does not assert idem-dedup is the sole caveat while elsewhere treating the retraction-race as real.

### Issue 2: A1's zero-step enumeration omits rejection

**ASN-0134, A1 (Realization)**: "A non-state-changing operation — an Observe, an idempotent Emit_K hit, the hit branch of a Nullify_Binary — is realized as *zero* steps; it reads a state and returns."

**Problem**: A precondition-failing call — gate failure, `P0` failure, `P-tgt` failure (ASN-0128 S3, I6) — is also non-state-changing and realized as zero steps ("reads a state and returns" failure), yet is not among the three enumerated cases. This is not cosmetic: §4's confluence argument case-splits precisely on whether an operation is realized as a step, and rejection is an *order-dependent* way for an operation to be zero-step (Issue 1). A1 is the claim that fixes the realization count downstream reasoning relies on; if it silently excludes rejection, the blind spot in Issue 1 is inherited from here.

**Required**: Add rejection (gate/`P0`/`P-tgt` failure) as a zero-step realization outcome — or mark the list non-exhaustive — and note that whether a state-changing operation is realized as one step versus rejected to zero steps can itself depend on the linearization state, feeding §4.

## OUT_OF_SCOPE

### Topic 1: Document-registration (K.σ) concurrency
**Why out of scope**: §4 scopes `K.σ` out of the conflict analysis, treating document-address freshness as an assumed precondition supplied by the excluded entity-allocation layer (no document sub-allocator exists in this stack — `d` is caller-supplied). The same-`d` race the note acknowledges ("the substrate resolves it by rejecting the loser") belongs in a future note that extends H0–H2 to the entity layer's `A_doc`/`A_v` sub-allocators, where registration would acquire the same frontier structure as `K.α`/`K.λ_sh`. The deferral is principled and explicitly stated (M1(c), §4); this is correctly future territory, not a defect here.

META: (none — the note specifies an abstract isolation contract that any concurrent realization must satisfy, with no mechanism committed; it has not drifted into implementation mechanics.)

VERDICT: REVISE
