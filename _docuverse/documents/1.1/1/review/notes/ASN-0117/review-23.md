# Review of ASN-0117

The technical content is sound. I traced the K.μ⁻+K.μ⁺ composite against ASN-0082's displacement (D-SHIFT/D-L/D-SEP), verified the `R = ∅` lone-K.μ⁻ realisation and its count algebra (`N − c − (J−1) = 0`), checked the coupling discharges (J0/J1★/J1'★ vacuous), the range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}`, and the wp derivation. All hold. The remaining issues are presentation residue flagged by the anti-bloat classifier.

## REVISE

### Issue 1: Claim-label revision history embedded in the spec
**ASN-0117, "Claims Introduced"**: "*The claim labels run P0, P2, P4, P5. The arrangement-side removal fact once carried as a separate P1 (ArrangementContraction) now lives in DEL-REMOVE; an earlier address-permanence claim P3 was absorbed into P0.*"
**Problem**: This narrates the *history* of the label set — what claims used to be called and how they were merged — which is PR-description content that rots as the note evolves and adds nothing to the specification. A reader needs the current claims (P0, P2, P4, P5), not the path that produced them. The gap in numbering is self-evident from the table and requires no in-document apology.
**Required**: Delete the preamble paragraph. Keep the table.

### Issue 2: Raw LaTeX macros leaking into prose
**ASN-0117, "The document remains one coherent sequence" and the wp/P4 sections**: e.g. "`ran(M'(d)\!\restriction\!V_{s_C}(d)) ⊆ dom(C')`" and "`ran(M(d)\!\restriction\!V_{s_L})`".
**Problem**: `\!\restriction\!` is LaTeX (negative thin-spaces around a restriction symbol). These ASNs render in CommonMark/monospace, where the macros appear literally and obscure the restriction. The same notion is written cleanly elsewhere as `M(d)|_{V_S(d)}`.
**Required**: Replace `\!\restriction\!` with the `|`-restriction notation already used in the foundation citations (e.g. `M(d)|_{V_{s_C}(d)}`).

## OUT_OF_SCOPE

### Topic 1: Deletion beginning before the first arranged position
**Why out of scope**: The precondition fixes `p = q_J ∈ V_S(d)` with `J ≥ 1`; a span starting below the origin is excluded by construction and correctly deferred to the first Open Question.

### Topic 2: Backtrack / prior-arrangement reconstruction state
**Why out of scope**: DELETE's contract is content-non-destruction plus arrangement contraction; what additional state backtrack needs is genuinely new territory (the fourth Open Question), not a gap in this operation.

VERDICT: REVISE
