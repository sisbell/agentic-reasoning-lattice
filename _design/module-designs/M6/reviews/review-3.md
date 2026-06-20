I worked through each of the seven operations against M1–M5 as given and the source notes. Six build cleanly; the seventh is mis-diagnosed. Here is what a reviser should change.

## Revision list

**1. [DEFECT] SHOWDELETIONS is buildable in M6 from the upstream interfaces *as given* — remove the invented `m5.cross_deletions` call and the demanded M5 amendment; build the cross-document combine here.**

The design's central claim — "SHOWDELETIONS is the *only* M6 operation not buildable against the upstream interfaces as given… blocked on a required M5 amendment" — is false, and it rests on an oversight the design itself exposes. The reasoning rejects the SpanSet-*intersection* route (correctly: `intersect_sets`/`normalize` fault on mixed-length covers) and the in-M6-authoritative-state route (correctly), but never tries the membership route — even though it **explicitly lists `denotes` among M1's SpanSet methods** in Conflicts-resolved-1. The combine needs membership-testing, not set algebra:

```
a_with_b = { a ∈ content_image(d_B) : DELETED(a, d_A) }
```

- enumerate `content_image(d_B)` exactly as `retrieve_v` already does — `m5.content_runs(d_b)` → per-position `run_addr(run.i_start, k)` (both in M5/M6 as given);
- test `DELETED(a, d_A)` with `m5.deletions(d_a).denotes(a.tumbler())` (`deletions` is in M5's interface; `denotes` is in M1's, faults on nothing, and is exact on real content addresses since no content address is a strict prefix of another — origins are distinct `zeros=2` documents);
- symmetric for `b_with_a` over `content_runs(d_a)` against `deletions(d_b)`;
- all reads off the one bound `&Snapshot`, so `(M,R)` is one consistent boundary (no torn read).

This is exactly the division of labor **M5's interface already states**: `deletions` is labeled "SHOWDELETIONS primitive… **M6 reads it straight off**; M5 does the per-level-class difference." The reviewed design contradicts that seam — it declares `deletions` "insufficient" and pushes the *whole* combine into a new M5 method. The cross-document combine is a pure per-query read that the decomposition assigns to M6 ("deletion classification (SHOWDELETIONS)"); the design's Lampson appeal ("hint belongs with the store") conflates the R *index* (`docs_containing`, rightly M5) with this *combine* (rightly M6).

Fix: implement `show_deletions` with the construction above; **delete** the `cross_deletions` amendment block, the "blocked"/"required M5 amendment" framing (Purpose, Build-status, Conflicts-resolved-1, the Dependencies "M6 calls no `content_runs`/`deletions`" note, and the M10 seam caveat). Also **change the output to address sets** — `Deletions { a_with_b: Vec<Address>, b_with_a: Vec<Address> }`, deduped and T1/Tumbler-ordered — which the construction yields directly and which is faithful to ASN-0075 D-IDENT ("the returned reference is precisely the I-address `a`") / D-ORD; this dissolves Conflicts-resolved-9 (the SpanSet-coverage "lossless only under a pinned exact-cover contract" rationalization was a consequence of the wrong delegation). If `deletions` exactness is a worry, the exactness-independent variant tests `DELETED(a,d_A) ≡ ever_placed(d_a).denotes(a) ∧ a ∉ content_image(d_a)`, using `ever_placed` + `content_runs(d_a)` — both in M5 as given.

**2. [SHARPENING] Tighten `gate_vspec` from `#start < 2` to `#start != 2`.** The design collapses `m_S(d) ≡ 2` (Conflicts-resolved-3), so depth-2 is the exact admissible depth. As written, a degenerate depth-3 ordinal-level span slips the gate and is rejected only later in `show_origin_v` as `RangeNotPresent` (a WF_V(vi) code) — a misattributed reason, and silently empty (not rejected) in `retrieve_v`/`compare`. A `#start == 2` check rejects it precisely and uniformly at the gate across all three resolve-based ops, matching the `m_S ≡ 2` ruling.

**3. [SHARPENING] Resolve `fold_adjacent`.** It is referenced by `canonicalize` but given only as prose, and the prose ("both feet advance by one") reads oddly against the already-wide pairs `interval_join` emits. Since the design states finer-than-maximal output conforms (X12 R4 not required), either supply the merge body or state explicitly that the identity (no folding) is a conforming implementation — so the reference does not read as an unimplemented gap.

**4. [SHARPENING] State `run_addr`'s 2-component element-field assumption.** `ElemPos { doc, subspace, ordinal }` faithfully reconstructs `i_start` only because content/link I-addresses have a 2-component element field `[subspace, ordinal]` (M3 mints them so). A longer element field would silently drop components. The invariant holds, but `run_addr` is load-bearing in four ops; note the assumption.

**5. [SHARPENING] Settle the SHOWORIGIN_I de-scope's M10 contingency.** The de-scope is sound — the I-arity genuinely needs an I-ordered `dom(C)` enumeration that M4 *deliberately* forbids and no upstream provides, so it correctly belongs to a new index, not an M6 internal. But the design leaves "sound only if M10 promises clients no SHOWORIGIN-over-I" as an open builder check. Resolve it (confirm M10's FEBE surface) so the decomposition amendment is settled rather than conditionally-defect.

**6. [SHARPENING] Note COMPARE's overlapping-specs redundancy.** Overlapping windows within one spec-set (ASN-0122 X12 permits them) make `resolve_blocks` double-cover V-positions, so `interval_join` emits redundant pairs. This is denotationally conforming (`⟦Γ⟧` is a set-union; the stable `sort_by` keeps it deterministic for R3), but say so — or dedupe the region — so a builder doesn't read the redundancy as a completeness/determinism bug.

VERDICT: REVISE
