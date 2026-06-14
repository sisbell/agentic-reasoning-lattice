# Review of ASN-0134

This is an unusually careful note: A4's no-torn-step argument, H0's frontier case analysis, the H2 first-emission/interior split, the step-vs-operation confluence seam in §4, and the soundness-vs-durability split in §8 are all handled with real rigor. The proofs hold under adversarial probing. Two items remain — both precision/grounding, not correctness.

## REVISE

### Issue 1: The headline claim — quiescence-verdict soundness — is never grounded in a concrete scenario
**ASN-0134, §8 (V0/V1/V2) vs §7**: The abstract promises "the snapshot is the only honest referent for a verdict," and §8 opens "We come to the sharpest of the questions." Yet the entire verdict apparatus — the multi-read realization `Q = g(Observe_{K₁}(Σ_{r₁}), …, Observe_{K_p}(Σ_{r_p}))`, the `Q`-affecting-step definition, and V2's central failure ("a tuple of per-type views that held at no single index") — is stated only abstractly. By contrast §7 grounds the *allocation* half (H1/H2/W4) in explicit tumblers (`a_4 = [1.0.1.0.1.0.1.4]`, the `a_5` intrusion).

**Problem**: The note's most subtle and most novel postcondition (multi-read verdict soundness, V2) is the one with no worked instance. "Sound about a single state" and "states that never coexisted" are precisely the claims a concrete trace makes checkable. The reader must take V2's strict-implication chain on faith for the realistic (multi-type) case.

**Required**: Add a worked multi-read scenario in §7's style, exhibiting the V2 error. E.g. `Q ≡ A_{K₁} = ∅ ∧ A_{K₂} = ∅`: at `r₁`, `Observe_{K₁}(oper) = ∅` while one active `K₂`-tuple `T₂` exists; between the reads a writer emits a `K₁`-tuple (changes already-read `K₁`, *not* `Q`-affecting) and nullifies `T₂` (changes not-yet-read `K₂`, the lone `Q`-affecting step); at `r₂`, `Observe_{K₂}(oper) = ∅`. The verdict `g(∅,∅)` reports "quiescent," yet the system was quiescent at neither `r₁` (where `K₂ ≠ ∅`) nor `r₂` (where `K₁ ≠ ∅`) nor any state between. Then show the same trace under clause 7 (reads pinned to one index) yielding a sound verdict. This verifies V2 against an instance rather than asserting it.

### Issue 2: A1's realization model is incomplete and imprecise against ASN-0128's full operation surface
**ASN-0134, §1 / A1**: "A state-changing operation is realized as *exactly one* atomic step… this happens in four ways: an `Observe`; an idempotent `Emit_K` hit; the hit branch of a `Nullify_Binary`; and a *rejected* call." The supporting justification ("read straight off ASN-0128") covers only `Emit_K`, `Nullify_Binary`, `Observe_K`.

**Problem**: Two parts of ASN-0128's surface escape this enumeration, and §8 then relies on them.
- (a) The behavioral *read* queries — `members`, `is_K`, `targets_of`, `succs`, `chain`, `tip`, `sources_to`, `target_of`, `targets_keyed`, `age`, `stale`, `is_filtered` (D1–D4, BH1–BH4) — are zero-step reads, but A1's "four ways" names only "an `Observe`." §8 explicitly counts them as the read surface ("only the per-type `Observe_K` (ASN-0086; ASN-0128 D1–D4 / BH1–BH4)"), so the verdict machinery depends on a zero-step status A1 never assigns.
- (b) `retract_stale` (BH4) is a *state-changing operation* realized as **many** steps — "a sequence of wrapper steps, not an atomic operation" (your own A5 quote). Read literally, A1's "a state-changing operation is realized as exactly one atomic step" is false for it.

**Required**: Make A1's enumeration exhaustive and consistent with the surface §8 uses: either define "an `Observe`" to mean *any* read-only query (listing D1–D4/BH1–BH4 reads as instances) or add a fifth zero-step way; and scope the one-step claim to *single (non-batch)* operations, delegating batch operations (`retract_stale`, a definition's content run) explicitly to A5. As written, "four ways" is presented as complete while omitting the read surface the note's own §8 requires.

## OUT_OF_SCOPE

### Topic 1: Batch read-atomicity (strictly stronger than W4)
**Why out of scope**: The note correctly isolates W4 as the *writer-side* half (run contiguity) and defers reader-visible all-or-nothing batch atomicity to Open Q 3/4. That is new territory, not a defect here.

### Topic 2: Cross-server composition of per-home orders
**Why out of scope**: G1's per-home independence is named as the seam for a future multi-server note (Open Q 6). Correctly future work.

VERDICT: REVISE
