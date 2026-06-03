# Review of ASN-0075

I read this as a heavily-revised, late-stage ASN, and I checked each proof against its cases, boundaries, and cited foundations.

## REVISE

(none)

I attempted to break the following and could not:

- **D-EXH impossible-row exclusion.** The chain `a ∈ ran(M(d)) → v witness → L14 (a ∉ dom(L)) → S3★-aux → contrapositive of S3★ link clause → subspace(v) = s_C → (a,d) ∈ Contains_C(Σ) → P4★ → (a,d) ∈ R` is justified at every step, and the composite-boundary hypothesis that activates P4★ is discharged structurally by D-BOUND rather than left as a caller obligation. Mutual exclusion holds pairwise (CURRENT/DELETED differ on `a ∈ ran(M(d))`; DELETED/NEVER_INCLUDED differ on `(a,d) ∈ R`; CURRENT/NEVER_INCLUDED is the excluded row). Exhaustiveness is by cross-product totality. No "similarly."

- **D-DISCR.** Histories 1 and 2 are exhibited as valid composites (J0 bundling of K.α with K.μ⁺/K.ρ correctly justified; first-emission determinism pins the same `a`; content value `v_a` synchronized). The component-by-component table genuinely pins `(C,L,E,M)` identically while `R` differs on `(a,d)`, so a single counterexample pair refutes any `f(C,L,E,M)` discriminator. The necessity claim is correctly scoped to state-functional implementations (consistent with D-RECONS).

- **Worked example.** I recomputed all six classifications, both output halves `({b},{c})`, and the D-SYM swap `({c},{b})`; the K.μ~-then-K.μ⁻ ordering on `d_A` (needed to make `b` the trailing-position drop) is correct, and `d_B = inc(d_A,1)` is a valid version (`zeros = 2`).

- **D-ACT witness-run bijection.** The `±1`-walk intermediate-value argument establishing that `I_C` is a contiguous index range is sound; `shift(·,1) = inc(·,0)` agreement on valid emissions (via TA5-SigValid + TA5(c) + TumblerAdd) is correct; the index-minimum/T1-minimum coincidence via T9 is correct; right- and left-maximality are each verified by closure under I-adjacency rather than asserted. Distinctness of the `ℓ` reconstructed addresses is discharged by TA-strict + TS5. The omission of T1-consecutiveness in `dom(C)` is honestly flagged as unused.

- **D-SUBSP.** The witness-impossibility chain (L0 → `ℓ ∈ dom(L)`; both `subspace(v) = s_C` excluded via S3★+L14 and `subspace(v) = s_L` excluded via CL-OWN) is complete, making the content-subspace restriction structurally derived rather than assumed.

- **wp analysis** is non-trivial (Q1 non-emptiness, Q0 vacuity, plus the R-disjointness supplementary lemma), and the boundary hypothesis is correctly threaded through each P4★ use.

- **Edge cases** (`d_A = d_B`, both arrangements empty, no shared content, asymmetric population) are each handled with the correct reason, not by appeal to a single case.

All cross-ASN references are to foundation ASNs (0034, 0036, 0047, 0053, 0058); I found no reference to a non-foundation ASN and no reinvented notation.

## OUT_OF_SCOPE

The Open Questions (multi-document generalization, link-subspace deletion analysis, concurrency consistency, "deleted from both but current in a third") are correctly deferred as future territory rather than gaps in this ASN. No flag needed.

VERDICT: CONVERGED
