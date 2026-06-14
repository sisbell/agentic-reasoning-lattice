# Review of ASN-0134

This is a meticulous note. The conflict analysis (H0–H3), the step/operation seam (G1 vs. the two families), the literal-vs-operative reading of I1a behind clause 8, and the worked traces in §7–§8 are all carefully done and, where I checked them against the foundations, correct. The central thesis — per-home suffices for *allocation*, but reader-side verdicts (clause 7) and `idem=⊤` de-duplication (clause 8) demand non-per-home discipline — holds. I found one load-bearing classification that does not.

## REVISE

### Issue 1: single-home `stale` is classified as a single bounded access, but active-membership requires a cross-home retraction read

**ASN-0134, §1 (A1)**: "the single bounded access over `d`'s link subspace that enumerates `d`'s active type-`K` members already carries the one frontier `f_d^Σ` from which every constituent `age` is computed — one index, clause-4-sound, like `age` itself." (Propagated to V0, MIC clause 4, and M1(d), which all lump single-home `stale` with `age` as a single-bounded-access read.)

**Problem**: This sentence conflates two reads. `f_d` *is* recoverable in one descent of `d`'s link subspace — that is what makes `age(a) = f_d − 1 − j` genuinely single-index, and the `age` classification is sound. But `stale(h) = {a ∈ A_K^Σ : age(a) > h}` additionally filters to the **active** subset `A_K = L_K ∖ nullified`, and active-membership is *not* determinable from `d`'s link subspace:

- `nullified(Σ) = {a : ∃(b,F',G') ∈ L_R^Σ : a ∈ coverage(G')}` (ASN-0086).
- By `Nullify_Binary(Σ, d_retr, a)` the retractor's home `d_retr` is unconstrained relative to `home(a)` (ASN-0128, P0 requires only `d_retr ∈ dom(Σ.M)`). Indeed §4's own *target-residence race* (family 2) turns on `d_retr ≠ home(target)`.
- So a tuple homed at `d` may be nullified by a retraction emitter homed at any `d' ≠ d`, and that emitter lives in `A_L(d')`, **not** in `d`'s link subspace.

Hence a descent of `d`'s link subspace yields `d`'s type-`K` tuples and `f_d`, but **not which of them are active**. Enumerating `d`'s *active* type-`K` members requires a second access — the global retraction consultation the note bundles into `Observe_K`-grade reads elsewhere. By the note's own access-count discriminator ("one bounded access ⟹ single-index; several ⟹ §8 multi-read"), single-home `stale` is therefore a **multi-read**, not a single bounded access. The note's §4 family-2 analysis (retractions are cross-home) directly undercuts the A1 claim that single-home `stale`'s active members are enumerable from one read over `d`'s subspace.

The soundness consequence is exactly the one the note warns of: if the member/frontier read (index `k₁`) and the active-filter read (index `k₂ > k₁`) drift across an interleaved nullify, the result is `members(k₁) ∖ nullified(k₂)` — a configuration matching no single committed state (the V0/V2 "states that never coexisted" error). So a single-home staleness verdict is **not** sound for free under clause 4; it needs clause 7's one-index pin, just as multi-home `stale` does.

**Required**: Either (a) reclassify single-home `stale` as a multi-read governed by clause 7 — throughout A1, V0, clause 4, and M1(d) — keeping only `Observe_K`, `age`, and the per-type `Observe_K`-grade reads under clause 4 (this *strengthens* the reader-side-needs-global-pinning thesis and is the surgical fix); or (b) argue explicitly that the active-membership consultation **and** the home frontier descent are fused into one atomic access at one committed index (a stronger claim than the `Observe_K` convention supplies, since that convention covers an active-view read but not a co-pinned frontier read), and correct the "single bounded access over `d`'s link subspace" phrasing, which silently drops the retraction read that active-ness requires.

## OUT_OF_SCOPE

### Topic 1: Arrangement-layer (document-editing) concurrency

The note commits (§1) to the ASN-0093 allocation stack, where M2 forces `M(d)=∅` — trivial arrangements — and its operation surface is `Emit_K`/`Nullify_Binary`/`Observe_K`. MIC is thereby the concurrency contract for the *type/relation substrate*, not for arrangement-mutating operations (INSERT, DELETE, REARRANGE) over a non-trivial Vstream/POOM, where A6's "no boundary-only invariant class" no longer holds (the J0/J1-style provenance/arrangement coupling of a richer state reappears). The note even cites Gregory's INSERT/DELETEVSPAN/REARRANGE as A7 evidence while not modeling them.

**Why out of scope**: This is a future ASN over a different (arrangement-bearing) stack, not an error here — the note is explicit about its stack choice and the exclusion is principled. It is worth marking only so a reader does not mistake MIC for the *whole* concurrency story.

META: (none — the note specifies a contract any faithful implementation must satisfy and invariants of state under concurrency, staying at the system-guarantee level and deferring all mechanisms to Open Questions; it has not drifted into implementation mechanics.)

VERDICT: REVISE
