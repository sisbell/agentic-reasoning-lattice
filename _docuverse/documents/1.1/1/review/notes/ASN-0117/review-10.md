# Review of ASN-0117

I checked the central split that the last revision introduced (R=∅ as a lone K.μ⁻, R≠∅ as the K.μ⁻+K.μ⁺ composite), the displacement clauses against the ASN-0082 foundation, the coupling/frame obligations, the well-formedness package, the wp analysis, and the worked examples. All citations are to foundation ASNs (0034, 0036, 0043, 0047, 0082, 0093, 0098) and are used rather than reinvented.

Verification highlights:
- **Composite counts are consistent.** K.μ⁻ retains `n'_{s_C}=J−1`; K.μ⁺ re-places `N−c−(J−1)` survivors. Strict-extension `≥1` ⟺ `J+c≤N` ⟺ `R≠∅`. The R=∅ branch (`J−1=N−c`, no survivor shifts) correctly degenerates to a lone K.μ⁻, and the would-be empty K.μ⁺ is correctly excluded.
- **Coupling vacuity (J0/J1★/J1'★) is sound.** No allocation (J0), no range-new content since every re-placed image was already in `ran(M(d))|_{s_C}` (J1★), no new provenance (J1'★).
- **Range derivation `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` checks out**, including the link-subspace carry-through and the `A_del`-disjoint-from-`s_L`-images step.
- **wp is the genuine weakest precondition**: shrink-only direction is automatic; equality reduces to the per-link existential implication, with the last-witness escape branch correctly identified and DEL-LIMM correctly load-bearing.
- **Edge cases covered**: entire-document delete, suffix delete (R=∅), within-document sharing (count vs per-pair in DEL-REMOVE), cross-document transclusion isolation, well-definedness of the left-shift via OrdinalExceedsDisplacement.
- **DEL-REMOVE's count-based statement** (rather than per-pair absence) is the correct robust form given S5/M13 sharing — a subtle point handled correctly.

The operation specifies abstract state guarantees (P0–P5, frames), not implementation mechanics; it has not drifted. No correctness, missing-case, or derivation-depth defects found.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Backtrack reconstructibility and the state beyond the content store it requires
**Why out of scope**: Correctly deferred to an Open Question; exact prior-arrangement reconstruction needs version/history machinery not introduced here.

### Topic 2: Deletion spans beginning before the document origin / concurrent unserialized edits
**Why out of scope**: The precondition (`J≥1`, containment) excludes the underflow case, and the well-definedness remark flags it; both are appropriately listed as Open Questions for future ASNs.

VERDICT: CONVERGED
