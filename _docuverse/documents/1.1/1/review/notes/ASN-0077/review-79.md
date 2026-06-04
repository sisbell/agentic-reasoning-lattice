# Review of ASN-0077

I verified the proof chain end-to-end: the pointwise projection (O0/O3), its lifts to I-spans and V-spans, permanence (O5/O5★), monotonicity (O6/O6★/O8/O12), the operation-specific preservation results (O7, O11, O11', O11★★ with O11.1 and SDP), the negative claims (O13/O14), and the worked example. I checked citations against the foundation set (ASN-0034/0036/0047/0053/0058/0098) — all references resolve to foundations, no non-foundation cross-references, no reinvented notation.

Specific checks that passed:

- **O0(b) for dom(L)** is non-circular: L1c roots the chain at the structural projection `origin(ℓ) = t₀`, L0 routes it through `A_L(t₀)`, and the Allocator hierarchy's `origin = d` on `A_L(d)` outputs closes the loop. SubAllocatorBundle disjointness makes the attribution unambiguous.
- **Singleton I-span proof** (in the edge-case block) is fully discharged across all three length cases: `#b < #a` excluded by a T1 case-(i) divergence at the prefix-copy region; `#b = #a` by T3; `#b > #a` by the zero-count balance argument (a's three zeros within 1..#a, b agrees there, `zeros(b)=3` forces no trailing zeros, so the document-element separator coincides positionally). The NAT-discrete squeeze at position `#a` is correctly instantiated.
- **O2 block uniformity** correctly discharges *both* conjuncts of M16a's precondition (`aⱼ ∈ dom(C)` via the `i=0` instance) and splits content/link blocks via S3★-aux exhaustiveness, using CL-OWN for the link case where M16a does not apply.
- **O11/O11'** avoid "by similar reasoning" — each gives a full impossibility analysis of the new-V-position case, correctly using ContentSubspaceRestriction (s_C-only) for K.μ⁺ and the s_L V-position precondition for K.μ⁺_L, with C0a/SC-NEQ excluding cross-subspace positions and SDP+precondition (vi) excluding same-subspace ones.
- **O11★★** sub-case (iii) is a sound complement: only the four K.μ transitions modify `M(d)`, and the hypothesis excludes K.μ⁻/K.μ~ on `d`, so non-extension steps fall to O7.
- **Negative claims O13/O14** are existentials whose concrete witnesses are exhibited and labeled in the worked example (σ_{1..7} contraction for O13; the [1,1,3]↔[1,1,7] swap for O14). The swap is verified admissible (length/subspace-preserving, non-trivial), and the `{d₁} ⊄ {d₃}` incomparability is genuine.
- **Anti-bloat scan**: no use-site inventories, no document-ordering justifications, no "why the axiom is needed" prose (no axioms are introduced), no duplicated paragraphs, no chained deferrals. The block-decomposition apparatus (C1a, O2) is expository for the worked example but O2 is a proved claim, not meta-prose, and the formal definition (F1) stands independently.

The Nelson quotations and the [Q17] `find_documents_containing` contrast sit in motivational/scope slots, not in proof slots, and the operation specifies abstract postconditions over `(C, L, E, M, R)` — system guarantees, not implementation mechanics. No drift.

## OUT_OF_SCOPE

### Topic 1: Unified content+link I-span origin operation
The first open question (an I-span operation reporting both content and link origins) is correctly deferred — the current I-span lift deliberately intersects with `dom(C)` only, and the cross-subspace edge case documents this choice.

### Topic 2: Transclusion-chain surfacing and historical containment
The remaining open questions (intermediate-chain surfacing, native-vs-transcluded distinction, `Σ.R`-based historical containment) are new operations, not gaps in SHOWORIGIN. The "What SHOWORIGIN does not promise" section correctly fences them off.

VERDICT: CONVERGED
