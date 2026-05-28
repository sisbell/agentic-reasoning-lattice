# Review of ASN-0100

I checked the three effects (allocation, placement, shift), every invariant conjunct claimed preserved, the edge cases (j=0 / interior / append / empty-document / empty-arrangement-with-non-fresh-allocator), the worked example's region and projection arithmetic, the wp analysis, and the atomicity/ordering argument.

## Findings

**Edge cases** — all four boundary positions covered with distinct precondition predicates (binary `ValidInsertionPosition` vs ternary `ValidFirstInsertionPosition`), and the n=1/n>1 cases exercised by the worked examples. Zero-width (n=0) explicitly excluded.

**Invariant coverage** — the ~28 Class (a) per-state invariants of ASN-0047 are each discharged, with the non-trivial ones (S4, L0's content clause, P6, P7) correctly identified as ranging over the *changed* `dom(C)` rather than dismissed by frame. The tiling invariants (D-CTG★/D-MIN★/D-SEQ★) are verified by explicit union computation `{1,…,N+n}`, not hand-waved.

**Proof depth** — the freshness argument routes through ChainEnumerationInjectivity + ChainMembershipForOrigin + Disjointness rather than asserting it; the disclaiming of I3-V/I3-CS/I3-CX (importing only I3's positive shift clause) is sound since those describe a shift-only model whose post-state is properly contained in INSERT's; the S2 disjointness uses TumblerAdd component arithmetic with last-component values computed; the S8★ text-subspace decomposition correctly identifies `inc(a_k,0) = shift(a_k,1)` for T4-valid same-length addresses to satisfy M7's I-adjacency.

**Concrete example** — verifies INS.M-{left,insert,shift}, INS.seq, INS.proj (including the K.μ⁻-retract/K.μ⁺-reintroduce cancellation), discoverability, and the J0/J1★/J1'★ discharge, plus a non-tight alternative trace.

**wp analysis** — non-trivial (discoverability-preservation collapsing to `discoverable_from(ℓ,d,Σ)` for tight endsets via LP19a) and genuinely weakest.

**Atomicity** — the composite-boundary vs per-state distinction is handled carefully; the separation of elementary-level atomicity (SequentialTransitionAxiom) from composite-level atomicity (an environmental precondition outside wp) is correct, and the forced/commuting ordering analysis is exhaustive.

All cross-references are to foundation ASNs (0034/0036/0047/0053/0058/0082/0093/0098). No reinvented notation. The ASN defines state effects, operations, and invariants abstractly; the substrate decomposition is in abstract K-vocabulary, and the Gregory "knife" appears only as an explicitly-labeled implementation aside — no drift.

I found no skipped cases, no proof-by-"similarly," no checkmark proofs, and no unaddressed invariant conjunct.

## OUT_OF_SCOPE

The ASN correctly bounds DELETE/COPY/REARRANGE/link-subspace-insertion/version-creation/replication to future ASNs, and its Open Questions (minimal atomicity machinery, link-subspace analog, self-composition closure, concurrency serialization) are appropriately deferred rather than treated as defects in this ASN.

VERDICT: CONVERGED
