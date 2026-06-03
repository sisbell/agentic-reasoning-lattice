# Review of ASN-0100

I reviewed this ASN as a verification of the INSERT operation specified as a substrate composite under ValidComposite★ (ASN-0047). I checked the three-effect derivation, every invariant discharge, the edge cases (empty document, beginning `j=0`, interior, append `j=N`), the atomicity argument, and the worked examples against the foundation lemmas.

## Verification notes (no defects found)

The following were checked closely and hold:

- **Region partition exhaustiveness and S2.** Left (last comp `< p_m`), Insertion (`{p_m,…,p_m+n−1}`), Shifted-right (`{p_m+n,…,N+n}`) are pairwise disjoint by the TumblerAdd component arithmetic, with the `k=0`/`k≥1` split correctly routed through OrdinalShiftBase vs. OrdinalShift. Shifted-right source uniqueness via TS2 has its equal-length precondition discharged by S8-depth. The union is `{1,…,N+n}`, cardinality `N+n`, no gaps/overlaps. INS.M-exhaustive closes the S2 argument as required.
- **INS.chain-shift.** The `inc(·,0) = shift(·,1)` identity is correctly grounded in T4-validity (ChainElementT4Validity → TA5-SigValid → `sig=#`), not asserted definitionally; iteration via TA5a + TS3 is sound. This is genuinely load-bearing for the S8★ run-collapse and the I-adjacency in M7.
- **I3 scope handling.** The disclaimer of I3-V/I3-CS/I3-CX/I3-C is precise — the conflict between I3-V and INS.M-insert is correctly localized to coinciding Insertion positions `shift(p,k)` with `p_m+k ≤ N`, and excluded in the append/empty cases. The pointwise content frame (S0/P0) vs. exact-equality I3-C distinction is correctly drawn.
- **D-CTG★ full-slice discharge.** The closed-interval form over the entire depth-`m_C` slice (not just the prefix family) is properly handled via the off-prefix divergence argument; `m_C ≥ 3` interior components forced to 1.
- **S8★ via C1a not M2/M12.** Correctly uses C1a (RestrictionDecomposition) rather than M2/M12, with the explicit justification that whole-arrangement M2 carries S3 (which fails when `V_{s_L}(d) ≠ ∅`, only S3★ holding). Preconditions discharged.
- **Atomicity stratification.** Per-state (Class a) vs. composite-boundary (Class b: P4★/P4a/P7a) invariants correctly separated; the allocated-but-unplaced interior window is legitimately exempt because J0 is a boundary coupling. The elementary-vs-composite atomicity distinction and its exclusion from the wp calculus are correctly reasoned.
- **The K.ρ/K.μ⁺ ordering argument.** The rejection of the "reorder R away" cross-composite argument by symmetry with the irreparable C-window is logically sound.
- **Worked examples and projection trace.** Interior/append/empty cases, the LP-Fin-Corollary tightness construction, the step-by-step LP6/LP10/LP9/LP14 projection trace, and the non-tight alternative (both failure modes a and b) all check out arithmetically.
- **No cross-ASN references** outside the foundation set; **in scope** (specifies abstract post-state and invariants of an operation, defers implementation mechanics). No META.

OUT_OF_SCOPE topics (DELETE, COPY, REARRANGE, link-subspace insertion, version creation, BEBE) are correctly deferred in §Bounding the Scope and the Open Questions, with no stray claims.

## REVISE

(none)

VERDICT: CONVERGED
