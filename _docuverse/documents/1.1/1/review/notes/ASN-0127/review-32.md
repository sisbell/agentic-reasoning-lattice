# Review of ASN-0127

This ASN is in strong shape: I verified every derivation (F-IMG-SWING's reindexing, F-IMG-TAX's four witnesses, F-UDIST through F-VDIST, E-CONS's two-direction anchor argument, D-CWP's bridge and biconditional) and every computation in the worked illustration (both D-CWP branches, the rise, both swings, the zeros), and they check out. The remaining defect is one genre of gap appearing at two sites: existence witnesses asserted over states that are never discharged as conforming states.

## REVISE

### Issue 1: F-IMG-TAX witness pre-states are not discharged as conforming states

**ASN-0127, Phase 1, F-IMG-TAX (Witness admissibility paragraph)**: "Each reorder witness below — injective, gain, loss, and four-position — is an admissible K.μ~ instance (ASN-0047): pin `vₖ = [1, k]` … and the shape invariants (i) — S8a, S8-depth, D-CTG★, D-MIN★, all properties of that unchanged domain — persist in the post-state; each witness's value assignment takes at least two distinct values (K.μ~'s precondition)…"

**Problem**: The paragraph discharges K.μ~'s admissibility clauses (i)–(v) and the two-distinct-values precondition, but it never places the witness *pre-states* inside the invariant package the ASN operates under. The images `a, b, c` are free symbols. Every pinned position `[1, k]` is a content-subspace V-position, so S3★ (ASN-0047) requires `Σ.M(d)(v) ∈ dom(Σ.C)` at any conforming state — and nothing in the witnesses asserts `a, b, c ∈ dom(Σ.C)`, nor their pairwise distinctness as allocated addresses. Clause (i)'s checked list is the arrangement-*shape* package only; the value-side invariant is silently skipped. The lemma's load-bearing words are "realizable" and "available," and as written they are proved only relative to states that may violate S3★ — states where K.μ~ never fires. The house standard for existence witnesses conditions the state explicitly (M13, ASN-0058: "(E Σ : Σ satisfies S0–S3 : …)"; L9/L11b, ASN-0043: "For any state Σ satisfying the state-local L- and S-invariants…"); this ASN's witnesses fall short of that standard.

**Required**: One clause pinning the images as pairwise-distinct allocated content addresses — e.g., successive emissions of `A_C(d)` (distinctness then grounded by ChainEnumerationInjectivity, ASN-0093, rather than stipulated) — together with the observation that K.μ~ preserves `ran(Σ.M(d))` (LP11, ASN-0098), so S3★ carries from the pre-state to the post-state. The shared-image arrangements of the gain/loss/four-position witnesses are then available because K.μ⁺'s precondition demands only `a ∈ dom(C)` per new mapping (sharing permitted, M13/M14, ASN-0058).

### Issue 2: D-ABSORB's insufficiency witness — same conformance gap, plus an unpinned "conforming triple"

**ASN-0127, Discovery anchoring, D-ABSORB**: "Insufficiency witness: with `Σ.M(d_q) : v₁ ↦ a, v₂ ↦ b` injective and `W = {v₁}` … let `dom(Σ.L)` hold the single link, a conforming triple, whose slot-1 endset is the two-span set `{(a, δ(1, #a)), (b, δ(1, #b))}` with coverage `subtree(a) ∪ subtree(b)`…"

**Problem**: Two gaps, the first inherited from Issue 1: `a, b` are not pinned as members of `dom(Σ.C)` (S3★), and the link is not pinned as satisfying the link-store invariants under which `dom(Σ.L)` can hold it at a conforming state (L0, L1, L1a, L1c). Second, "a conforming triple" gestures at L3's mandatory non-empty type endset without supplying it, and the argument's robustness to the type slot is left tacit. The conclusion does survive any choice of slot 3 — the store holds exactly one link and slot 1 witnesses the match at both states, so the discovery set is that singleton at both states regardless of what slot 3 covers — but that is an observation the proof must make, not one the reader should have to reconstruct. The worked illustration sets its own standard here: it pins `Θ = {a_θ}` explicitly and verifies slot 3's non-interference span by span; the D-ABSORB witness should meet the same bar.

**Required**: Either import the worked illustration's setup (where the stores are fully pinned and conforming) for this witness, or pin it locally: `a, b ∈ dom(Σ.C)` distinct, a type slot `Θ ≠ ∅` named, and the one-line note that the conclusion is independent of slot 3 because slot 1 alone witnesses the match at both states and the store is a singleton.

## OUT_OF_SCOPE

### Topic 1: Conjunctive slot-indexed query algebra (Q2)
**Why out of scope**: Which of F-UDIST/F-IMONO survive under per-slot filter sets is a genuinely different matching semantics (conjunctive over slots rather than existential); the ASN correctly declares it open rather than half-treating it.

### Topic 2: Uniform stability weakest precondition across the full K-vocabulary (Q3)
**Why out of scope**: D-CWP nails the contraction instance; a characterization uniform over extension, reorder, and off-document transitions is new derivation work, not a hole in D-CWP, and the `R = ∅` boundary correctly defers to it.

### Topic 3: Composition with content-keyed queries and ASN-0098's projection (Q1, Q4)
**Why out of scope**: `image()` is arrangement-mediated by design; the `Σ.C`-keyed variant and the project-then-query composition are adjacent operations belonging to a successor note.

VERDICT: REVISE
