# Review of ASN-0076

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Supersession chain invariants and cycles
**Why out of scope**: The ASN's own Open Questions list this; it requires a downstream ASN to address (e.g., whether the supersession relation can be acyclic, and what would enforce it).

### Topic 2: Supersession-type address convention
**Why out of scope**: Acknowledged in Open Questions. EDITLINK correctly leaves `τ_sup` open and structural; pinning a recognizable type-address registry belongs in a future type-endset conventions ASN.

### Topic 3: Multi-source/multi-target supersession (1→N and N→1)
**Why out of scope**: Acknowledged in Open Questions. Standard-triple EDITLINK already covers the central case; n-way generalizations belong downstream.

### Topic 4: Retraction/contradiction of supersession claims
**Why out of scope**: Acknowledged in Open Questions. The ASN's design (counter-claims via further link allocation) is consistent; the formal treatment of resolution policy belongs to a reader-policy ASN.

### Topic 5: Discovery operations interacting with edited links
**Why out of scope**: Acknowledged in Open Questions. E7 establishes the structural witness; the operational discovery layer is downstream.

### Topic 6: Authorization model for who may invoke EDITLINK on which `d_new`
**Why out of scope**: E6's informal discussion correctly disclaims this — no executor/capability model exists in any cited foundation, and the discussion of "Alice/Bob/Carol" is properly framed as motivation rather than formal claim.

VERDICT: CONVERGED

The ASN is rigorous and Dijkstra-conformant. Every claim E0–E10 is proved without "by similarly" gaps. Boundary cases (first-emission vs subsequent-emission, k=0 base case, τ_sup inside/outside `dom(C) ∪ dom(L)`, prior emissions in `A_L(d_new)`) are explicitly handled. The depth-bound induction (#E ≥ 2 preserved under inc(·, 0)) is fully expanded via TA5(b), TA5(c), TA5-SigValid, T4, T0 closure. ValidComposite★ is discharged with all three couplings (J0, J1★, J1'★) shown vacuous. The worked example traces concrete tumblers through E0–E10. Foundation citations stay within the verified set (ASN-0034, 0036, 0043, 0047, 0098); no improper cross-ASN references. The Open Questions section properly defers further work without contaminating the present claims.
