# Review of ASN-0077

I checked the load-bearing proofs — O0 (origin extended to dom(L)), the singleton I-span proof, O2 (block uniformity), O5/O5★, O11/O11'/O11★/O11'★/O11★★, and the O13/O14 witnesses against the worked example — for skipped cases, incomplete case analysis, and unsupported "derived" steps.

## REVISE

(none)

Findings from the proof-check:

- **O0(b) for dom(L)** correctly grounds origin in L1c + Allocator hierarchy + SubAllocatorAxiom (e) without any K.λ-event closure; the totality argument (c) routes through P6 (dom(C)) and SubAllocatorAxiom-activation + P1 (dom(L)). Sound.
- **Singleton I-span proof** handles all three length cases (`#b < #a` excluded by T1 prefix-copy analysis; `#b = #a` by T3; `#b > #a` by zero-count balance + T4b parse). The squeeze closure via NAT-discrete is explicit, and the deliberate refusal to exclude `#b > #a` (avoiding a transition-vocabulary-closure assumption) is correct and honestly flagged.
- **O2** discharges the M-sub(a) precondition via S8a, splits exhaustively on subspace via S3★-aux, and uses M16a (content) / CL-OWN (link) with the `i = 0` instances properly supplied. Both branches close.
- **O11 Case (ii)** correctly proves the newly-added-position case impossible via cross-state depth identification (S8-depth anchoring on non-empty pre-state positions) and C0a subspace confinement. O11.1 lifts well-formedness across both extension kinds; O11★/O11'★/O11★★ induct cleanly with a binary modifies-/fixes-M(d) exhaustiveness that needs no vocabulary enumeration.
- **O13/O14** provide genuine witnesses (admissibility loss; incomparable origin sets under the π-swap), with K.μ~ admissibility obligations (a)(b)(c) individually discharged in the worked example.

The structural-derivation/typing distinction in O3 (computation reads only the supplied value; S3★ guarantees domain membership but is not consulted) is a legitimate separation, not a gap. References are confined to foundation ASNs; no improper cross-ASN citations. The operation is a read-only query with abstract guarantees — no drift into operation mechanics. Open questions defer the right topics (cross-subspace I-span origin, chain surfacing, native/transclusion distinction, historical containment).

## OUT_OF_SCOPE

(none requiring flags — the ASN defines no INSERT/DELETE/COPY/REARRANGE mechanics, link semantics, version-DAG, or replication claims.)

VERDICT: CONVERGED
