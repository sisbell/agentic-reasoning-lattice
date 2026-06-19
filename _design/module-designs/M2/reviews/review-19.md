## Review: M2 — Transaction, Journal & Concurrency Kernel

I worked the buildability bar hardest on the two intricate cores — the durable-before-visible commit ordering with its truncate-or-poison failure path (§1/§3), and the two-pass recovery classifier (§7) — and on faithfulness to the MIC clauses (ASN-0134) and the seven-primitive composite model (ASN-0047). The module is **buildable from this document alone**: the `transact` flow, frame/marker/segment formats, recovery passes, and checkpoint mechanism are all concrete enough to implement, the interface is fully generic over `W` with no concrete `World`/`Record` leak (matching the Engine Composition Contract), every owned key component is present, and all three ASN-0047↔ASN-0134 conflicts (composite-vs-batch atomicity, single-writer-vs-per-home, visible-vs-durable) are resolved soundly. The factual claims I spot-checked against A1/A5/A7/V2/SAFE/MIC-6/MIC-7 and ASN-0047's K.μ~/J0 are faithful. The recovery is sound under the default (`Fsync`+`Rollback`), with the lone gap — post-commit bit-rot of the *last* committed txn — honestly flagged and correctly scoped out (the notes don't mandate it).

Findings are all non-load-bearing:

1. **[SHARPENING]** In §6, pin the checkpoint-trigger counters' synchronization. As written ("counters … reset at each checkpoint" + "`checkpoint()` … never takes the applier lock"), the increment runs under the applier lock while the reset runs inside `checkpoint()` under only the checkpoint mutex — a race. Specify that the counters live in the applier-locked state and are **reset by the triggering `transact` under the applier lock** (when the policy is crossed, before releasing and invoking `checkpoint()`), so `checkpoint()` never touches them. Worst realistic outcome today is benign cadence imprecision (with atomics), but it should be deterministic.

2. **[SHARPENING]** In §7, note that the inferred-`Seq`-max classifier (`≈ next_intact − 1`) is an **upper bound** that, under `BurnedSeqPolicy::TolerateGap`, can overestimate a corrupt run's true max when a burned-`Seq` gap immediately follows the run — so a run actually entirely `≤ S_load` may be conservatively halted as `Corruption{at}` (a recoverable kernel refused). State this as the deliberate cost of the never-silently-drop posture, and that under the default `Rollback` (no gaps) the classifier is exact. The design implies precision; it is precise only under `Rollback`.

3. **[SHARPENING]** In `open`/§7, state the implicit caller contract that `genesis` must be **byte-stable across opens** — recovery folds journal records onto the caller-supplied `genesis` (and falls back to it on `BadCheckpoint`), never onto a journaled root, so an inconsistent genesis silently mis-recovers. ASN-0047's fixed Σ₀ (`n₀ = [1]`) satisfies this, but the kernel depends on it.

4. **[SHARPENING]** Extend the M7 seam sketch (Dependencies & seams) to show the **link-seating push** (M5's `ArrRec` for K.μ⁺_L, lifted via `.into()`) alongside `LinkRec::Emit`, so the `M7 → M5` no-return-edge composition is illustrated as concretely as the `M5 → M4` content placement. The prose states it; the code shows only the emit/dedup path.

5. **[SHARPENING]** Give M1's `inc` its real arity in the M3/M5/M7 sketches (`inc(max, 0)` per ASN-0034's `inc(t, k)`), or annotate `inc(max)` as shorthand, so the neighbor-call examples don't read as contradicting M1's signature.

6. **[SHARPENING]** Consolidate the marker-as-ack + truncate-or-poison discipline — currently restated nearly in full across §1, §3, §7, Invariants, Conflicts #3, and Open build decisions — into one canonical statement (§1) plus cross-references, to remove the wording-drift risk across six copies.

VERDICT: CONVERGED
