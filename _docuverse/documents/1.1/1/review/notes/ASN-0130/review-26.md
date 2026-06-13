# Review of ASN-0130

The core machinery is sound, and I want to say so before the findings: I checked the load-bearing proofs in detail and they hold.

- **PR-SIG well-foundedness** — the induction on first-registration order is grounded, not circular: PR0 (iv) forces every referent active at the deposit pre-state, hence first-registered strictly earlier (PR2(a)), so `sig(r)` is already defined when `a`'s body is typed.
- **PR2 acyclicity** — both observations check out. (a) referent-precedence via (iv); (b) self-reference exclusion via the dedup-miss/I0-equality argument (at a deposit event no active tuple denotes the start, so (iv) has no self-witness). The embedding into the strict event order is clean, and "unconstructible" is correctly stronger than "banned."
- **PR3a substitution induction** — WT-α (fresh injective renaming), WT-W (weakening), and the `k`-fold PC2 lowering (last parameter first, interference- and capture-free because every introduced binder is a reserved expansion name) compose correctly; the rank IH is legitimately applied at strictly-lower-rank referents.
- **PR5 ST⁺ soundness** — the reduction to PD0's ground is correct: PD0's ground consumes only *fixity* of bound values across a step, and an `args`-bound parameter is fixed (same `args` on both sides), so the literal→bound-ℕ threshold extension is sound. The "coincide at `k=0`" claim survives scrutiny: PD0's rules bind no ℕ value internally (no `age`/PC2-guard rule), so the only non-literal ℕ threshold is a parameter, absent at `k=0`.
- **PR0 wp**, the **exact-coverage lemma** (distinct run-starts are ≼-incomparable: same-origin by sibling non-nesting, cross-origin by anchor incomparability), the `shift(x,1)=inc(x,0)` chain-segment identity, and the boundary cases (`n=1`, closed `k=0`, re-registration after de-registration, the frontier-ghost adversary in step 5) all hold.

The remaining items are the forward-reference accretion the `anti-bloat` classifier targets, plus one allocation question that belongs downstream.

## REVISE

### Issue 1: View handling is fragmented across forward deferrals to PR-VIEW
**ASN-0130, PR-ENC / PR3 / PR5**: PR-ENC — "no view component (deliberately: definitions are view-polymorphic, the view bound per evaluation, PR-VIEW)"; PR3's evaluation clause — "the view fixed at the top level per PC3, with what that fixing means for referents stated at PR-VIEW."
**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" pattern. PR3's clause "with what that fixing means for referents stated at PR-VIEW" carries zero local content — it is a pure pointer. PR-ENC pre-states the view rationale ("view-polymorphic, bound per evaluation") that PR-VIEW then establishes properly, so the same idea is told in three places before the section that owns it arrives.
**Required**: Delete the bare "stated at PR-VIEW" pointer in PR3 (the reader reaches PR-VIEW regardless). At PR-ENC, "no view component (PR-VIEW)" suffices; the polymorphism rationale belongs once, in PR-VIEW.

### Issue 2: Editorial design-rationale in operation slots
**ASN-0130, PR0**: "admitting an invalid registration would mint a durable classifier whose meaning (PR1) would be a lie."
**Problem**: The operation's behavior is already fully stated one clause earlier ("On any validation failure the call is rejected — no step, no tuple, no address"). The "would be a lie" gloss is defensive justification for the enforce-by-rejection choice, not a statement of what the operation does. PR5a (0) carries a similar elaboration ("though a well-formed, registrable, referenceable artifact, has no stability to assert … a term that was never a predicate at all") around what is mechanically just "reject when `sig(a)` is non-Boolean."
**Required**: Trim the rhetorical rationale; the enforce-by-rejection stance is already pinned by the cross-reference to ASN-0128's S3 and the explicit reject-with-no-tuple statement.

### Issue 3: "What this note commits" previews duplicate the body
**ASN-0130, "What this note commits"**: the seven bullets each restate a claim's full content (PR0's bullet is ~50 words covering validate/deposit/seal/born-nullified/wp), which the body then states again.
**Problem**: These are not a roadmap but a second copy of the claims, exactly the forward-reference inventory that compounds across cycles — every claim revision now has two sites to keep in sync, and the reader meets each commitment twice.
**Required**: Reduce to a bare roadmap (claim name + one phrase), or cut; let the body carry the content.

## OUT_OF_SCOPE

### Topic 1: Guaranteed contiguous-run allocation under concurrent same-document writers
PR-ENC/PR0 presuppose that a builder can obtain a contiguous `{shift(a,k)}` content run; the worked example flags the assumption ("with no other K.α scoped to `d_b` interleaved"). The foundation substrate (ASN-0093) provides only single-element K.α under sequential atomicity — no atomic multi-element insertion — so contiguity rests on an allocation discipline (single-writer-per-document, or a batch primitive) not formalized in the foundations.
**Why out of scope**: The note's guarantees (PR1–PR3) hold for any run that *is* contiguous; a split run simply fails PR0 (i) and is retried. Whether the substrate should expose an atomic multi-element content-insertion primitive is substrate-layer territory, not a defect in this ASN.

VERDICT: REVISE
