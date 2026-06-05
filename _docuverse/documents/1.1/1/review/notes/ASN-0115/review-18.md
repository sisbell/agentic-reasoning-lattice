# Review of ASN-0115

I checked R0–R11 against the foundation contracts, verified each worked instance arithmetically, and stress-tested the boundary cases (empty spec-set `p=0`, empty subspace `V_S(d)=∅`, terminal overrun vs. interior hole, deeper-than-`m_S` positions, transclusion, multi-origin, subspace crossing, orphaned content).

Findings:
- **R6 terminal-overrun**: the canonical-start derivation (`act ≠ ∅` forces `s = [S,1,…,1,s_{m_S}]` via T5 + D-SEQ★) is sound; deeper positions correctly filtered via S8-depth, not a T1-position claim. Worked instance (`s=[1,2]`, `ℓ=δ(5,2)`, `reach=[1,7]`, `act={[1,2],[1,3],[1,4]}`) checks out, including `[1,2,1] ∈ ⟦σ⟧` filtered by depth.
- **R7**: comparability requirement (`Σ →* Σ'`) is genuinely needed, not over-strong — divergent branches could rebind a fresh address; correctly justified, WLOG sound.
- **R8 link vacuity**: CL-OWN forces `d=d'`, CL-UNIQ forces `v=v'` — derivation complete.
- **R11 wp**: the single-live-condition decomposition (reference (i) live; `a ∈ dom(C)` automatic via S3★+S0) is a non-trivial wp on the orphaned-content case, correctly handled.
- Cross-ASN references: all to foundation ASNs (0034/0036/0043/0045/0047/0053/0058/0082/0086/0093/0098) — permitted.
- `item` totality on `act` discharged by S3★-aux + per-case S3★; subspace `S ∉ {s_C, s_L}` collapses to `act=∅` harmlessly.

No hand-waves, no proof-by-checkmark, no missing-case gaps, no reinvented foundation notation. Boundary-crossing spans, inline provenance, and unbound-reference cases are correctly deferred to Open Questions rather than half-specified.

## REVISE

(none)

## OUT_OF_SCOPE

(none beyond the ASN's own Open Questions, which appropriately defer single-span subspace straddling and channel faithfulness.)

VERDICT: CONVERGED
