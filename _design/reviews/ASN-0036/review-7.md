## Assessment

I went looking hard for a misread, an ungrounded Green claim, an altitude slip, or a missing load-bearing commitment. I did not find one. This digest is unusually disciplined where digests of this note most often fail:

- It **avoids the S4 trap** — it explicitly forbids content-addressed storage *as identity* and confines value-dedup to a layer beneath the authoritative address→value map. Correct.
- It **scopes contiguity correctly** — D-CTG/D-MIN/D-SEQ are presented as text-subspace-only (the note states them for `V_1(d)`), with non-text contiguity attributed to Green observation (Q5), not the note. A weaker digest over-generalizes here.
- It **handles canonicity precisely** — the maximal decomposition is recoverable as a unique mathematical object (S8), but stored form need not be canonical, grounded in Q3 (`levelpull` stubbed, `isanextensionnd` opportunistic coalescing, confluence at the query interface). It correctly carves out that run-*structure* queries must canonicalize-on-demand.
- It **gets S5 right at a level above the note** — distinguishing the formal consistency theorem (no cap entailed) from the design mandate (Nelson's transclusion intent), and hands the builder the right instruction ("build no cap").
- All source-level Green claims (`levelpull`, `isanextensionnd`, `acceptablevsa` stub, two-blade knife at `(N+1).1`, `findnextlinkvsa`/links-from-`2.1`, permascroll, POOM, spanfilade) are grounded in the evidence answers or documented Green structure.

Everything below is a sharpening; none is load-bearing.

## Revision list

1. **[SHARPENING] "Guarantees to uphold" — "canonicity is explicitly NOT guaranteed" reads, in isolation, against your own Forced claim that the canonical run structure is "always recoverable."** They are consistent (recoverable-on-demand ≠ materialized-as-state), but a reader scanning only this line could see tension with S8's *proven* uniqueness. Insert one word: "*stored/materialized* canonicity is explicitly NOT guaranteed." That nails it to the storage stance you actually mean.

2. **[SHARPENING] S5 bullet — "the *licence* that no cap is consistent with the formal core" is grammatically ambiguous** (parses as "every cap is inconsistent," the opposite of your intent). The parenthetical already disambiguates; align the lead clause to it: "S5 establishes that the *absence* of a cap is consistent with S0–S3 — and so is a cap, which is why bolting one on would betray Nelson's intent without violating the formal core."

3. **[SHARPENING] Content-typing — make the numbering subtlety land on the note's *formal* alignment definition.** You correctly flag that Green numbers text I-addresses under `doc.3.x` while the note's worked example numbers the element field with a leading `1` (`…1.3`). What you can add in one clause: the note's open-question *formalization* of alignment is `subspace(v) = v₁` **equal to** the I-address's first element-field component — which holds only when the two numberings coincide (the note's example) and is literally false under Green's (`1 ≠ 3`). So "alignment" is really a fixed V-subspace↔I-kind correspondence, not numeric equality. Your recommendation (read kind off the address) is sound either way; this just keeps a builder from trying to implement `v₁ == E(a)₁` under Green numbering.

4. **[SHARPENING] "Constrained but deferred" / "What must be built" — S8a's well-formedness is more than depth ≥ 2.** You state "depth ≥ 2 is forced (S8a)" but not the zero-free / all-components-positive half. It is subsumed by your recommended `[1,…,1,k]` (k ≥ 1) reconstruction, so nothing breaks — but one clause ("zero-free, all components positive, depth ≥ 2") fully states the V-position predicate, which matters for anyone choosing explicit absolute keys instead of the implicit run-list.

## Solid sections (no action)

The content store (append-only journal, index-as-rebuildable-hint, immutability-by-omission-not-by-guard, no-content-GC-ever, buffer-then-merge as the one surviving concurrency concern); the implicit-position run-list over a length-sum tree with its honestly-stated foreclosure (commits *every* subspace to contiguity, beyond what S8a alone requires); allocation/attribution as contention-free baptism + pure projection; the sharing-inverse and snapshot/recovery stances; and the model-it-as-precondition / discharge-by-blessed-paths-plus-boundary-check treatment of subspace alignment — all derive cleanly from the note and the evidence and need no change.

VERDICT: CONVERGED
