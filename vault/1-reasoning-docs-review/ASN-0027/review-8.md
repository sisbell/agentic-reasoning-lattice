# Review of ASN-0027

Based on Dafny verification — 35 properties, 34 clean, 1 divergence

## REVISE

No genuine spec issues.

## QUALITY

### File: RearrangeLength.dfy — SIMPLIFY

Dead abstraction. Defines `RearrangeV` taking a generic `sigmaInv` parameter, but no other module imports or uses it. The actual rearrange proofs use `PivotRearrangeV` and `SwapRearrangeV` from `RearrangeOps`, both of which already carry `ensures |v'| == |v|`. The A3.length property is proved by the Ops module, not by this function.

```dafny
function RearrangeV(v: seq<IAddr>, sigmaInv: nat -> nat): (v': seq<IAddr>)
  requires forall i :: 1 <= i <= |v| ==> 1 <= sigmaInv(i) <= |v|
  ensures |v'| == |v|
```

Fix: strip to a label-only module matching `CopyLength` and `DeleteLength` (comment-only, property established by `RearrangeOps` ensures clauses). Or delete the file entirely since the ensures clauses on `PivotRearrangeV`/`SwapRearrangeV` are the actual proofs.

### All other files — PASS

The proof suite is clean and well-structured:

- **Shared ops modules** (`DeleteOps`, `CopyOps`, `RearrangeOps`) factor V-space operations once; all property proofs delegate to them.
- **Empty lemma bodies** throughout (`CopyIdentitySharing`, `CopyLeftFrame`, `CopyRightShift`, `DeleteCompaction`, `DeleteLeftFrame`, `FullRestoration`, `RearrangePermutation`) — the solver handles these without hints. Correct sparse style.
- **Minimal hints** where needed: `IdentityRestoringCopy` has one assert expanding `InsertV`; `NonInvertibility` has a set-membership trigger; `RearrangeRangePreservation` has case-split assertions for inverse mapping. All justified.
- **ReferencePermanence** uses clean induction over a trace with a single recursive call. No over-proving.
- **ReachabilityNonPermanent** constructs a concrete witness with targeted assert blocks — necessary for the existential.

## SKIP

### Divergence: ReachabilityDecay (A9) — proof artifact

The Dafny proof constructs an empty-docs state to witness `exists s' :: !Reachable(a, s')`. The ASN's A9 claims the stronger result that Σ' is reachable from Σ via a finite sequence of DELETE operations (with an explicit construction in the proof sketch). The Dafny proof is weaker but the gap is operational trace formalization — encoding iterated A2 steps with per-document deletion sequences — not a spec deficiency. The ASN property and its proof sketch are correct; the Dafny model simply doesn't formalize multi-step operational traces. No spec change needed.

### 34 clean verifications — no divergences

All remaining properties verified without divergence. The proof structure faithfully mirrors the ASN's layered decomposition: operation specs (A2–A5) with frame conditions, composition lemmas (A6–A7), the inductive system-level guarantee (A8), and the accessibility boundary (A9–A10).

VERDICT: SIMPLIFY
