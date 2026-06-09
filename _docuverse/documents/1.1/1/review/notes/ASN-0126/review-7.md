# Review of ASN-0126

## REVISE

### Issue 1: P2/P3 well-definedness rests on registry well-formedness, which is neither cited in the derivation nor asserted as a commitment

**ASN-0126, Properties established (P2)**: "Corollary of P1: shape(K) reads only Σ.registry, which is invariant." (and P3, "Corollary of P1, by the same argument as P2")

**Problem**: "Well-defined" in P2/P3 carries two distinct obligations: (a) *state-independence* — the value doesn't change across states; and (b) *single-valuedness* — `shape(K)` is a function at all, i.e. lookup returns at most one entry. P1 (registry invariance) discharges only (a). Single-valuedness is supplied by a separate condition — coverage-class-key uniqueness — which the note itself identifies as "the load-bearing condition" in *Registration entries* ("it is coverage-class-key uniqueness that makes shape(K) and idem(K) single-valued"). The P2/P3 derivations in the Properties section attribute well-definedness entirely to P1 and omit this dependency.

Worse, the underlying condition is never asserted to *hold*. The note defines what a well-formed registry is, but the Properties are stated to hold "of every substrate satisfying its commitments," and registry well-formedness is not among the stated commitments. A substrate whose `Σ_init.registry` contains two `~`-equal keys with differing shapes — e.g. `{([K], "a", Unary, ⊤), ([K'], "b", Binary, ⊥)}` with `K ~ K'`, the note's own counterexample — satisfies every stated commitment (P1 still holds: the ill-formed registry is invariant) yet makes `shape(K)` multivalued and P2 false. P1's invariance freezes an ill-formed registry just as faithfully as a well-formed one.

**Required**: State `Σ_init.registry` well-formed (a partial function `T_admissible/~ ⇀ (name, shape, idem)`) as an explicit commitment of the framework, and have P2/P3 cite both premises: P1 for state-independence and registry well-formedness for single-valuedness. As written the derivation chain is "Corollary of P1" alone, which does not establish that `shape(·)` is a function.

## OUT_OF_SCOPE

### Topic 1: Multi-source (|F| ≥ 2) and higher-arity (N ≥ 3) relations

**Why out of scope**: The note deliberately narrows to `|F| = 1`, N = 3 and routes the multi-source / higher-arity case to direct link-store interaction (Single-source; Open questions #6). This is a scoping decision, not a gap — extending the catalog is correctly deferred to a supplemental note.

### Topic 2: Idem operational semantics

**Why out of scope**: The note commits only to the flag's structural presence and state-independence (P3); emit/nullify/re-emit semantics are explicitly deferred (Open questions #1). The structural commitment is self-contained.

VERDICT: REVISE
