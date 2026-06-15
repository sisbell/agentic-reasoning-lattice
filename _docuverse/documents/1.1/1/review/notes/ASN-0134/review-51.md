# Review of ASN-0134

This is a careful, technically dense note. The conflict lemmas (H0–H3), the schedule/confluence result (G1), the verdict-soundness chain (V0/V1/V2), and the invariant partition (W0–W4) are mostly sound, and the worked scenarios (§7, §8) verify the key claims against explicit addresses. The §4 operation-level analyses (instances (i)/(ii), the target-residence race, G2) are genuinely sharp. The findings below are one rigor gap and three instances of the meta-prose/forward-reference accretion this note is tracked for.

## REVISE

### Issue 1: G0's "not sequentially consistent" is asserted, not derived — and rests on a reordering that is SC-benign as stated
**ASN-0134, §3 / G0**: "SC would require the order to additionally preserve each agent's program order, which §4's cross-home liberation deliberately abandons" and "an agent's operations into *distinct* homes are `≺`-incomparable (§4), and the linearization resolves them without regard to which the agent issued first" — concluding "an execution is linearizable yet not SC."

**Problem**: The cited witness for non-SC is the reordering of an agent's *distinct-home* operations. But distinct-home allocations **commute** (H1, and G1(ii) confluence): reordering two commuting writes is observationally benign — the program-order serialization reaches the same state, so *that* execution is sequentially consistent. Textbook SC is "∃ *a* serial order respecting program order and matching observations," not "*the realized* 𝔼 respects program order." The note's phrasing — "the order/the serial order to preserve program order" — conflates the two, and under the standard reading, "𝔼 reorders commuting cross-home ops" does **not** entail not-SC. The genuine not-SC witness requires a *third-party observer* reading a distinguishing intermediate state (a store-buffer cycle: agent writes home A then B; observer reads B then A, sees B but not A; no A-before-B serialization matches). That witness is never exhibited. The note even gestures at the correct reason once ("pipelining makes program order ⊄ real-time order") but does not turn it into a construction, and the surrounding "preserves none" argument remains the operative justification. So the conclusion is defensible but the derivation skips exactly the step that makes the reorder SC-violating.

**Required**: Either (a) exhibit the observer-based execution — write A→B, observer reads B (present) then A (absent), and show no program-order serialization is consistent — so "linearizable yet not SC" is witnessed, or (b) restate the SC characterization as "the substrate neither tracks nor enforces program order" (what the cross-home commutation actually shows) and reserve "not SC" for the witnessed claim. As written, the H1/G1 commutation results undercut the stated argument rather than support it.

### Issue 2: the soundness/durability distinction is articulated four times
**ASN-0134, §8 (V1 + the two bullets + the closing paragraph) and §9 (SAFE(d))**: V1 already states the verdict is "retrospective… Extending a verdict from 'held at r' to 'holds through r'' requires an *additional* hypothesis." The two bullets immediately after V1 ("*Soundness*… *secured* by having the observer's reads all sit at one index r"; "*Durability*… needs that no writer linearizes a falsifying step after r") recap V0/V2 (soundness) and V1 (durability) with no new reasoning. The §8 closing paragraph ("The substrate's contribution is exactly and only the snapshot…") restates it a third time, and SAFE(d) ("This is *soundness* of the verdict about Σ_r; its *durability* past r remains V1's separate hypothesis") a fourth.

**Problem**: This is the flagged "two paragraphs say the same thing in different words," compounded. V0, V1, V2 already carry the distinction; the post-V1 bullets are a pure recap of claims stated immediately above and beside them.

**Required**: Keep the distinction in V1 (and the soundness side in V0/V2); cut the two recap bullets, and let SAFE(d) cite rather than re-derive. One articulation, referenced where needed.

### Issue 3: chain-contiguity preservation is forward-deferred to W1 from two separate sections, with "not re-argued here" narration each time
**ASN-0134, §2 (A6) and §4 (G1 proof)**: A6 (§2) writes "their *preservation* under any interleaving is W1's induction, deferred there and not re-argued here." G1's proof (§4) writes "The split this rests on — contiguity model-intrinsic and free (W1), uniqueness serialization-borne — is §5's, not re-argued here." Both lean on the same downstream result (W1's contiguity-preservation), proven two sections later in §5.

**Problem**: This is precisely the flagged pattern — "multiple paragraphs in different sections defer to the same downstream location" — with the deferral narrated ("deferred there and not re-argued here," "is §5's, not re-argued here") rather than the argument made. W1 is *model-intrinsic* (it needs only A0 and the `inc(max,·)` allocator), so nothing forces it to follow its two consumers. A reader cannot complete A6 or G1(i) without jumping forward. (This sits inside a broader density of forward scaffolding — "A6 will lean on this," "§4 leans on this," "the seed of §8's V1" — that compounds the same friction.)

**Required**: Establish W1's contiguity-preservation once, ahead of its consumers (it is the earliest model-intrinsic result), and have A6/G1 cite it without the repeated "not re-argued here" deferral narration.

### Issue 4: W3 defends a definitional coherence against a non-threat, then disclaims needing the defense
**ASN-0134, §5 (W3 and the paragraph following it)**: "At 'audit/active-slice coincidence' one might fear a read could see a tuple that is both present and absent. It cannot." The paragraph then runs the P-tgt three-case analysis (normal/self/declined) before conceding "W3 itself needs only the slice coherence, which holds under either resolution of it."

**Problem**: `A_K = L_K ∖ nullified` is coherent at every Σ_k *by construction* — both sides are pure functions of one state (A3), so there is no "present and absent" hazard to fear and the P-tgt residence case-analysis does not advance the coherence claim. The "one might fear… It cannot" is the flagged defensive-justification pattern, and the closing "W3 itself needs only the slice coherence" is a self-disclaimer that the preceding elaboration was not load-bearing.

**Required**: State W3 as the one-line definitional fact (both sets derived from the single Σ_k, hence mutually consistent at every state). Drop the fear-and-rebut framing; if the P-tgt residence point is worth keeping, attach it where it does work (the target-residence race, §4), not as support for a definitional coherence.

## OUT_OF_SCOPE

### Topic 1: operation-level non-confluence left open (§4 instance (ii); target-residence-race losing order)
**Why out of scope**: The note documents these as residual order-dependencies not closed by any MIC clause (instance (ii) survives both emit-before-retract and clause 7), and frames them as acknowledged limitations rather than defects. Whether a confluence-restoring discipline beyond clause 7 / emit-before-retract is warranted is future-layer work, correctly deferred via the Open Questions.

META: (none — the note specifies abstract system guarantees, MIC being explicitly "no lock, no transaction, no scheduler… only obligations any mechanism must meet," and stays in invariant/contract territory throughout.)

VERDICT: REVISE
