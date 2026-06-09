# Review of ASN-0121

I read the ASN in full and verified each claim against the foundation contracts, then re-derived the worked traces.

## REVISE

(none)

I checked the load-bearing items and found them sound:

- **FL-DEF "answer is forced."** The uniqueness argument is clean: soundness (with the addressability conjunct) gives `R ⊆ {a : addressable ∧ sat}` and completeness gives the reverse, pinning `R` exactly. The `R_min`/`R_max` motivation for why addressability must sit inside *soundness* (not just `sat`) is correct and necessary — retraction is deliberately not one of the four criteria.
- **nullified monotonicity over the full ASN-0047 vocabulary.** The structural argument (`nullified` is a function of `Σ.L` alone, since `L_R^Σ ⊆ Σ.L` and `A_rel^Σ = dom(Σ.L)`) correctly avoids a per-operation enumeration gap; constancy across non-K.λ steps plus R6a across K.λ closes it for `→` and `→*`. This also makes FL-STB's single hypothesis `Σ'.L = Σ.L` genuinely sufficient (retraction-set preservation follows rather than being assumed).
- **FL-DIR witness.** `x=[1,0,1,0,1,0,1,5]`, `y=[1,0,1,0,1,0,1,9]`: both `zeros=3`, equal length, non-nesting ⇒ disjoint subtree coverages (PrefixSpanCoverage + T1). The reversed request `(∗,Y,X,∗)` flips `{a₁}↔{a₂}`. Asymmetry exhibited concretely, not asserted.
- **Worked instance.** Re-checked Traces 1–6 arithmetically. Home projections (`home(p)=home(a₁)=[1,0,1,0,1]=d`, `home(a₅)=[1,0,1,0,2]=d'`), subspace identifiers (`s_C=1`, `s_L=2`, type subspace 3), and the node-rooted `H_node=[1]` coverage all parse correctly. Trace 6 properly exercises the residence axis with endpoints held byte-for-byte fixed — the answer flips on `H` alone, witnessing FL-RES.
- **FL-REACH containment.** The restriction to *satisfying* links (not the bare, request-independent `discoverable_from` union) is correctly drawn, with the `q=(∗,∅,∗,∗)` counterexample showing why the naive superset claim fails, and strictness justified via satisfying orphans (LP17/LP18).
- **Foundation usage.** `nullified` reused from ASN-0086 rather than reinvented; `coverage`/`home`/PrefixSpanCoverage/T5 applied consistently. All ASN references (0034, 0036, 0043, 0047, 0053, 0086, 0098) are to foundation ASNs; non-foundation ASNs (0110/0111/0114/0120) appear only in the scope note.

## OUT_OF_SCOPE

The ASN correctly defers version/time-scoped retraction inquiry, the I-address↔V-spec correspondence invariant, and cross-store federation to its Open Questions rather than overclaiming. These are new territory, not defects here.

VERDICT: CONVERGED
